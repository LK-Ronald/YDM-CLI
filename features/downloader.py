"""
Descargador individual - SRP: solo descarga una canción a la vez.
Usa yt-dlp con opciones optimizadas para máxima calidad de audio.
"""
import os
from pathlib import Path
from core.config_manager import ConfigManager
from utils.ui import UI
from utils.ytdlp_wrapper import YtDlpWrapper


class Downloader:
    """Descarga una sola canción desde un enlace de YouTube / YouTube Music."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()
        self._wrapper = YtDlpWrapper(config_manager)

    def run(self) -> None:
        self._ui.section("Descargar música")
        url = input("  Ingresa el link (YouTube / YouTube Music): ").strip()

        if not url:
            self._ui.error("No ingresaste ningún link.")
            return

        output_dir = self._config.get("download_dir")
        self._config.ensure_dirs()

        self._ui.info(f"  Directorio de descarga: {output_dir}")
        self._ui.info("  Iniciando descarga...\n")

        success, message = self._wrapper.download(url, output_dir)

        if success:
            self._ui.success(f"Descarga completada: {message}")
        else:
            self._ui.error(f"Error al descargar: {message}")

        input("\n  Presiona Enter para continuar...")
