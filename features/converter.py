"""
Convertidor de formatos de audio - usa FFmpeg vía pydub/subprocess.
Soporta mp3, alac, flac, wav, ogg, aac, m4a.
Hace rollback del archivo de salida si la conversión falla.
"""
import shutil
import subprocess
from pathlib import Path

from core.config_manager import ConfigManager
from utils.ffmpeg_manager import FFmpegManager
from utils.ffmpeg_process import run_ffmpeg
from utils.ui import UI

SUPPORTED_FORMATS = ["mp3", "flac", "wav", "ogg", "aac", "m4a", "alac", "opus"]
AUDIO_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".aac", ".m4a", ".alac",
                    ".opus", ".wma", ".ape", ".webm", ".mp4"}


class Converter:
    """Convierte archivos de audio a un formato destino."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()
        ffmpeg_path = FFmpegManager.get_path()
        self._ffmpeg_executable = str(ffmpeg_path) if ffmpeg_path else "ffmpeg"

    def run(self) -> None:
        self._ui.section("Convertir archivos a otro formato")

        if not self._check_ffmpeg():
            self._ui.error("FFmpeg no está instalado o no está en el PATH.")
            self._ui.info("  Descárgalo desde: https://ffmpeg.org/download.html")
            input("\n  Presiona Enter para continuar...")
            return

        # Directorio fuente
        source_dir = input(
            f"  Directorio de origen\n"
            f"  (Enter para usar '{self._config.get('download_dir')}'): "
        ).strip() or self._config.get("download_dir")

        source_path = Path(source_dir)
        if not source_path.exists():
            self._ui.error(f"El directorio no existe: {source_dir}")
            input("\n  Presiona Enter para continuar...")
            return

        # Directorio destino
        dest_dir = input(
            f"  Directorio de destino\n"
            f"  (Enter para usar '{self._config.get('converted_dir')}'): "
        ).strip() or self._config.get("converted_dir")

        dest_path = Path(dest_dir)
        dest_path.mkdir(parents=True, exist_ok=True)

        # Formato destino
        print(f"\n  Formatos disponibles: {', '.join(SUPPORTED_FORMATS)}")
        target_format = input("  Formato de salida: ").strip().lower()
        if target_format not in SUPPORTED_FORMATS:
            self._ui.error(f"Formato no soportado: '{target_format}'")
            input("\n  Presiona Enter para continuar...")
            return

        # Eliminar originales
        delete_originals_str = input(
            "\n  ¿Eliminar archivos originales tras convertir? (s/N): "
        ).strip().lower()
        delete_originals = delete_originals_str in ("s", "si", "sí", "y", "yes")

        # Buscar archivos
        audio_files = [
            f for f in source_path.iterdir()
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
        ]

        if not audio_files:
            self._ui.warning("No se encontraron archivos de audio en el directorio.")
            input("\n  Presiona Enter para continuar...")
            return

        self._ui.info(f"\n  {len(audio_files)} archivo(s) encontrados.\n")

        failed = []
        converted = []
        interrupted = False
        conversion_in_progress = False

        out_file = None
        try:
            for i, audio_file in enumerate(audio_files, 1):
                out_file = dest_path / (audio_file.stem + f".{target_format}")
                self._ui.info(f"  [{i}/{len(audio_files)}] {audio_file.name} → {out_file.name}")

                conversion_in_progress = True
                success, error = self._convert(audio_file, out_file, target_format)
                conversion_in_progress = False
                if success:
                    self._ui.success(f"  ✓ Convertido")
                    converted.append((audio_file, out_file))
                    if delete_originals:
                        try:
                            audio_file.unlink()
                        except OSError as e:
                            self._ui.warning(f"  No se pudo eliminar original: {e}")
                else:
                    self._ui.error(f"  ✗ Error: {error}")
                    # Rollback: elimina el archivo de salida parcial si existe
                    if out_file.exists():
                        out_file.unlink()
                    failed.append((audio_file.name, error))
        except KeyboardInterrupt:
            interrupted = True
            if conversion_in_progress and out_file and out_file.exists():
                try:
                    out_file.unlink()
                except OSError as error:
                    self._ui.error(f"No se pudo eliminar el archivo parcial: {error}")
            self._ui.warning("\nConversión interrumpida por el usuario.")

        print()
        if interrupted:
            self._ui.info(
                f"  Proceso cancelado. {len(converted)}/{len(audio_files)} "
                "conversiones completadas."
            )
        else:
            self._ui.info(
                f"  Conversión completada. "
                f"{len(converted)}/{len(audio_files)} exitosas."
            )
        if failed:
            self._ui.warning("  Los siguientes archivos fallaron:")
            for name, reason in failed:
                print(f"    • {name} → {reason}")

        input("\n  Presiona Enter para continuar...")

    def _convert(self, src: Path, dst: Path, fmt: str) -> tuple[bool, str]:
        """Ejecuta FFmpeg para convertir un archivo."""
        codec_map = {
            "mp3": ["-codec:a", "libmp3lame", "-q:a", "0"],
            "flac": ["-codec:a", "flac"],
            "alac": ["-codec:a", "alac"],
            "wav": ["-codec:a", "pcm_s16le"],
            "ogg": ["-codec:a", "libvorbis", "-q:a", "6"],
            "aac": ["-codec:a", "aac", "-b:a", "256k"],
            "m4a": ["-codec:a", "aac", "-b:a", "256k"],
            "opus": ["-codec:a", "libopus", "-b:a", "192k"],
        }
        extra_args = codec_map.get(fmt, [])
        cmd = [
            self._ffmpeg_executable, "-y", "-i", str(src),
            *extra_args,
            str(dst)
        ]
        try:
            result = run_ffmpeg(cmd, timeout=300)
            if result.returncode == 0:
                return True, ""
            return False, result.stderr.splitlines()[-1] if result.stderr else "Error desconocido"
        except subprocess.TimeoutExpired:
            return False, "Tiempo de espera agotado"
        except FileNotFoundError:
            return False, "FFmpeg no encontrado en el sistema"

    def _check_ffmpeg(self) -> bool:
        try:
            run_ffmpeg([self._ffmpeg_executable, "-version"], timeout=5)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
