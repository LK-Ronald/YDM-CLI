"""
Wrapper de yt-dlp - abstrae la descarga y maneja la barra de progreso.
Resuelve los problemas de JS de YouTube mediante yt-dlp actualizado.
Descarga en la máxima calidad disponible y convierte a MP3 ≥ 128 kbps.
"""
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

from core.config_manager import (
    CONCURRENT_FRAGMENT_DOWNLOADS_MAX,
    CONCURRENT_FRAGMENT_DOWNLOADS_MIN,
    SOCKET_TIMEOUT_MAX,
    SOCKET_TIMEOUT_MIN,
    ConfigManager,
)
from utils.ffmpeg_process import run_ffmpeg
from utils.ffmpeg_manager import FFmpegManager

try:
    import yt_dlp
    from yt_dlp.postprocessor.common import PostProcessor
    from yt_dlp.postprocessor.embedthumbnail import EmbedThumbnailPP
    from yt_dlp.utils import PostProcessingError

    YTDLP_AVAILABLE = True
except ImportError:  # pragma: no cover
    yt_dlp = None
    PostProcessor = object
    EmbedThumbnailPP = None
    PostProcessingError = RuntimeError
    YTDLP_AVAILABLE = False


class SquareThumbnailPP(PostProcessor):
    """Recorta el thumbnail descargado a un cuadrado antes de embeberlo."""

    def __init__(self, downloader, ffmpeg_executable: str):
        super().__init__(downloader)
        self._ffmpeg_executable = ffmpeg_executable

    def run(self, info: dict) -> tuple[list[str], dict]:
        thumbnail = next(
            (
                item
                for item in reversed(info.get("thumbnails", []))
                if item.get("filepath")
            ),
            None,
        )
        if not thumbnail:
            self.report_warning("No hay thumbnail disponible para recortar.")
            return [], info

        thumbnail_path = Path(thumbnail["filepath"])
        if not thumbnail_path.is_file():
            self.report_warning("No se encontró el thumbnail descargado para recortarlo.")
            return [], info

        with tempfile.NamedTemporaryFile(
            prefix="thumbnail-square-",
            suffix=thumbnail_path.suffix,
            dir=thumbnail_path.parent,
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)

        try:
            command = [
                self._ffmpeg_executable,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(thumbnail_path),
                "-vf",
                r"crop=min(iw\,ih):min(iw\,ih)",
                "-frames:v",
                "1",
                str(temporary_path),
            ]
            result = run_ffmpeg(command, timeout=300)
            if result.returncode != 0:
                raise PostProcessingError(
                    result.stderr.strip() or "FFmpeg falló al recortar la portada."
                )
            temporary_path.replace(thumbnail_path)
        except FileNotFoundError as error:
            raise PostProcessingError(
                "FFmpeg no encontrado al recortar la portada."
            ) from error
        except subprocess.TimeoutExpired as error:
            raise PostProcessingError(
                "Se agotó el tiempo al recortar la portada con FFmpeg."
            ) from error
        except OSError as error:
            raise PostProcessingError(
                f"No se pudo recortar la portada: {error}"
            ) from error
        finally:
            temporary_path.unlink(missing_ok=True)

        self.to_screen(f"Thumbnail recortado a 1:1: {thumbnail_path.name}")
        return [], info


class YtDlpWrapper:
    """Envuelve yt-dlp para descargas de audio con barra de progreso."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        ffmpeg_path = FFmpegManager.get_path()
        self._ffmpeg_executable = str(ffmpeg_path) if ffmpeg_path else "ffmpeg"
        self._ffmpeg_location = str(ffmpeg_path.parent) if ffmpeg_path else None

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normaliza enlaces que contienen parámetros de lista (list=) para
        asegurar que se apunte al recurso completo de playlist o álbum.
        """
        clean_url = url.strip()
        try:
            parsed = urllib.parse.urlparse(clean_url)
            qs = urllib.parse.parse_qs(parsed.query)
            if "list" in qs and "playlist" not in parsed.path:
                list_id = qs["list"][0]
                domain = (
                    "music.youtube.com"
                    if "music.youtube" in parsed.netloc
                    else "www.youtube.com"
                )
                return f"https://{domain}/playlist?list={list_id}"
        except Exception:
            pass
        return clean_url

    def extract_info(self, url: str) -> tuple[bool, dict | str]:
        """
        Extrae la información de una URL (canción, playlist o álbum) sin descargarla.
        Retorna (éxito, info_dict_o_error).
        """
        if not YTDLP_AVAILABLE:
            return False, "yt-dlp no está instalado. Ejecuta: pip install yt-dlp"

        normalized_url = self.normalize_url(url)
        try:
            socket_timeout = self._bounded_config_value(
                "socket_timeout",
                SOCKET_TIMEOUT_MIN,
                SOCKET_TIMEOUT_MAX,
            )
        except ValueError as error:
            return False, str(error)

        ydl_opts = {
            "quiet": True,
            "socket_timeout": socket_timeout,
            "extract_flat": True,
            "noplaylist": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                }
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(normalized_url, download=False)
                if not info:
                    return False, "No se pudo obtener información del enlace."
                return True, info
        except yt_dlp.utils.DownloadError as e:
            return False, self._friendly_error(str(e))
        except Exception as e:
            return False, f"Error inesperado al extraer información: {e}"

    def download(
        self,
        url: str,
        output_dir: str,
        noplaylist: bool = True,
    ) -> tuple[bool, str]:
        """
        Descarga el audio de la URL indicada al directorio de salida.
        Retorna (éxito, mensaje).
        """
        if not YTDLP_AVAILABLE:
            return False, (
                "yt-dlp no está instalado. Ejecuta: pip install yt-dlp"
            )

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        bitrate = self._config.get("bitrate", "320k")
        bitrate_num = str(bitrate).replace("k", "")

        try:
            socket_timeout = self._bounded_config_value(
                "socket_timeout",
                SOCKET_TIMEOUT_MIN,
                SOCKET_TIMEOUT_MAX,
            )
            concurrent_fragments = self._bounded_config_value(
                "concurrent_fragment_downloads",
                CONCURRENT_FRAGMENT_DOWNLOADS_MIN,
                CONCURRENT_FRAGMENT_DOWNLOADS_MAX,
            )
        except ValueError as error:
            return False, str(error)

        output_template = str(output_path / "%(title)s.%(ext)s")
        temporary_files_before = self._snapshot_temporary_files(output_path)
        info: dict | None = None

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "noplaylist": noplaylist,
            "ffmpeg_location": self._ffmpeg_location,
            "socket_timeout": socket_timeout,
            "concurrent_fragment_downloads": concurrent_fragments,
            "progress_hooks": [self._progress_hook],
            "writethumbnail": True,
            "embedthumbnail": False,
            "addmetadata": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate_num,
                },
                {"key": "FFmpegMetadata"},
            ],
            "quiet": True,
            "no_warnings": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                }
            },
            "retries": 5,
            "fragment_retries": 5,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if EmbedThumbnailPP is not None:
                    ydl.add_post_processor(
                        SquareThumbnailPP(ydl, self._ffmpeg_executable)
                    )
                    ydl.add_post_processor(EmbedThumbnailPP(ydl))
                info = ydl.extract_info(url, download=True)
                title = info.get("title", url) if isinstance(info, dict) else url
            self._cleanup_thumbnail_files(output_path, info)
            print()
            return True, title
        except KeyboardInterrupt:
            cleanup_errors = self._cleanup_temporary_files(
                output_path,
                temporary_files_before,
            )
            print()
            if cleanup_errors:
                print(
                    "No se pudieron limpiar algunos archivos temporales: "
                    + "; ".join(cleanup_errors),
                    file=sys.stderr,
                )
            raise
        except yt_dlp.utils.DownloadError as e:
            cleanup_errors = self._cleanup_temporary_files(
                output_path,
                temporary_files_before,
            )
            print()
            message = self._friendly_error(str(e))
            if cleanup_errors:
                message += " No se pudieron limpiar: " + "; ".join(cleanup_errors)
            return False, message
        except Exception as e:
            cleanup_errors = self._cleanup_temporary_files(
                output_path,
                temporary_files_before,
            )
            print()
            message = f"Error inesperado: {e}"
            if cleanup_errors:
                message += " No se pudieron limpiar: " + "; ".join(cleanup_errors)
            return False, message

    def _bounded_config_value(self, key: str, minimum: int, maximum: int) -> int:
        value = self._config.get(key)
        try:
            parsed = int(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Configuración inválida para {key}: {value!r}") from error
        if not minimum <= parsed <= maximum:
            raise ValueError(
                f"Configuración inválida para {key}: debe estar entre "
                f"{minimum} y {maximum}."
            )
        return parsed

    @staticmethod
    def _snapshot_temporary_files(output_dir: Path) -> dict[Path, tuple[int, int]]:
        if not output_dir.exists():
            return {}
        snapshot: dict[Path, tuple[int, int]] = {}
        for path in output_dir.iterdir():
            if not path.is_file() or not YtDlpWrapper._is_temporary_file(path):
                continue
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            snapshot[path] = (stat.st_mtime_ns, stat.st_size)
        return snapshot

    @staticmethod
    def _is_temporary_file(path: Path) -> bool:
        return (
            path.suffix.lower() in {
                ".part",
                ".ytdl",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp",
                ".avif",
            }
            or ".part-" in path.name.lower()
        )

    @staticmethod
    def _cleanup_temporary_files(
        output_dir: Path,
        files_before: dict[Path, tuple[int, int]],
    ) -> list[str]:
        if not output_dir.exists():
            return []
        errors: list[str] = []
        for path in output_dir.iterdir():
            if not path.is_file() or not YtDlpWrapper._is_temporary_file(path):
                continue
            try:
                current = (path.stat().st_mtime_ns, path.stat().st_size)
                if path not in files_before or files_before[path] != current:
                    path.unlink(missing_ok=True)
            except OSError as error:
                errors.append(f"{path.name}: {error}")
        return errors

    @staticmethod
    def _cleanup_thumbnail_files(output_dir: Path, info: dict | None) -> None:
        """Elimina thumbnails temporales reportados por yt-dlp."""
        if not output_dir.exists():
            return

        output_root = output_dir.resolve()
        for thumbnail in (info or {}).get("thumbnails", []):
            filepath = thumbnail.get("filepath")
            if not filepath:
                continue

            thumbnail_path = Path(filepath).resolve()
            if thumbnail_path.parent == output_root:
                thumbnail_path.unlink(missing_ok=True)

    def _progress_hook(self, d: dict) -> None:
        """Dibuja una barra de progreso ASCII en la misma línea."""
        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()

            if total and total > 0:
                pct = downloaded / total
                bar_len = 30
                filled = int(bar_len * pct)
                bar = "█" * filled + "░" * (bar_len - filled)
                mb_done = downloaded / 1_048_576
                mb_total = total / 1_048_576
                line = (
                    f"\r  [{bar}] {pct*100:5.1f}%  "
                    f"{mb_done:.1f}/{mb_total:.1f} MB  "
                    f"{speed}  ETA {eta}   "
                )
            else:
                mb_done = downloaded / 1_048_576
                line = f"\r  Descargando...  {mb_done:.1f} MB  {speed}   "

            sys.stdout.write(line)
            sys.stdout.flush()
        elif status == "finished":
            sys.stdout.write(f"\r  {'█' * 30} 100%  Procesando audio...   ")
            sys.stdout.flush()

    @staticmethod
    def _friendly_error(raw: str) -> str:
        """Convierte mensajes de error técnicos en mensajes amigables."""
        raw_lower = raw.lower()
        if "video unavailable" in raw_lower:
            return "El video no está disponible (privado o eliminado)."
        if "private video" in raw_lower:
            return "El video es privado."
        if "age" in raw_lower and "restricted" in raw_lower:
            return "El video tiene restricción de edad."
        if "unable to extract" in raw_lower or "jsinterp" in raw_lower:
            return (
                "Error al procesar YouTube. "
                "Actualiza yt-dlp: pip install -U yt-dlp"
            )
        if "urlopen error" in raw_lower or "network" in raw_lower:
            return "Error de red. Verifica tu conexión a internet."
        if "ffmpeg" in raw_lower:
            return (
                "FFmpeg no encontrado. "
                "Instálalo y agrégalo al PATH del sistema."
            )
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        return lines[-1] if lines else raw
