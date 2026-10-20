"""Download and locate the FFmpeg executable used by the application."""
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import zlib
from pathlib import Path, PurePosixPath
from urllib.error import URLError
from urllib.request import urlretrieve

from utils.ui import UI

FFMPEG_URL = (
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/"
    "latest/ffmpeg-master-latest-win64-gpl.zip"
)
APP_DATA_DIR = Path(os.environ.get("APPDATA", Path.home())) / "YDM-CLI"
FFMPEG_DIR = APP_DATA_DIR / "ffmpeg"
FFMPEG_EXE = FFMPEG_DIR / "ffmpeg.exe"


class FFmpegManager:
    """Ensure FFmpeg is available in the per-user application directory."""

    def __init__(self) -> None:
        self._ui = UI()

    def ensure(self) -> Path:
        """Return a working FFmpeg path, downloading it when necessary."""
        if self._is_usable(FFMPEG_EXE):
            return FFMPEG_EXE

        try:
            self._download()
        except (
            OSError,
            URLError,
            zipfile.BadZipFile,
            zlib.error,
            RuntimeError,
        ) as error:
            raise RuntimeError(
                f"No se pudo descargar FFmpeg: {error}\n"
                "Verifica tu conexión a internet e inténtalo de nuevo."
            ) from error

        if not self._is_usable(FFMPEG_EXE):
            raise RuntimeError(
                f"FFmpeg se descargó, pero no se pudo ejecutar: {FFMPEG_EXE}"
            )
        return FFMPEG_EXE

    @staticmethod
    def get_path() -> Path | None:
        """Return the cached executable path if it has already been installed."""
        return FFMPEG_EXE if FFMPEG_EXE.is_file() else None

    @staticmethod
    def _is_usable(path: Path) -> bool:
        if not path.is_file():
            return False
        try:
            result = subprocess.run(
                [str(path), "-version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0

    def _download(self) -> None:
        APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
        FFMPEG_DIR.mkdir(parents=True, exist_ok=True)
        self._ui.info("FFmpeg no encontrado. Descargando desde BtbN FFmpeg-Builds...")

        zip_path: Path | None = None
        executable_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix="ffmpeg-",
                suffix=".zip",
                dir=APP_DATA_DIR,
                delete=False,
            ) as temporary_zip:
                zip_path = Path(temporary_zip.name)

            urlretrieve(FFMPEG_URL, zip_path, reporthook=self._progress)
            print()
            self._ui.info("Extrayendo FFmpeg...")

            with zipfile.ZipFile(zip_path, "r") as archive:
                member = next(
                    (
                        name
                        for name in archive.namelist()
                        if not name.endswith("/")
                        and PurePosixPath(name).parts[-2:] == ("bin", "ffmpeg.exe")
                    ),
                    None,
                )
                if member is None:
                    raise RuntimeError("ffmpeg.exe no se encontró en el ZIP descargado.")

                with tempfile.NamedTemporaryFile(
                    prefix="ffmpeg-",
                    suffix=".exe",
                    dir=FFMPEG_DIR,
                    delete=False,
                ) as temporary_executable:
                    executable_path = Path(temporary_executable.name)
                    with archive.open(member) as source:
                        shutil.copyfileobj(source, temporary_executable)

            if not self._is_usable(executable_path):
                raise RuntimeError("El ejecutable de FFmpeg descargado no es válido.")

            executable_path.replace(FFMPEG_EXE)
            executable_path = None
            self._ui.success("FFmpeg listo.")
        finally:
            if zip_path is not None:
                zip_path.unlink(missing_ok=True)
            if executable_path is not None:
                executable_path.unlink(missing_ok=True)

    @staticmethod
    def _progress(block_num: int, block_size: int, total_size: int) -> None:
        if total_size <= 0:
            return
        downloaded = min(block_num * block_size, total_size)
        percentage = downloaded / total_size
        filled = int(30 * percentage)
        bar = "█" * filled + "░" * (30 - filled)
        downloaded_mb = downloaded / 1_048_576
        total_mb = total_size / 1_048_576
        sys.stdout.write(
            f"\r  [{bar}] {percentage * 100:5.1f}%  "
            f"{downloaded_mb:.1f}/{total_mb:.1f} MB   "
        )
        sys.stdout.flush()
