"""
Descargador por lotes - Lee URLs desde un archivo .txt y descarga cada una.
Reporta errores sin detener la ejecución completa.
"""
from pathlib import Path
from core.config_manager import ConfigManager
from utils.ui import UI
from utils.ytdlp_wrapper import YtDlpWrapper


class BatchDownloader:
    """Descarga múltiples canciones desde un archivo de texto."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()
        self._wrapper = YtDlpWrapper(config_manager)

    def run(self) -> None:
        self._ui.section("Descargar lista de músicas desde archivo")

        file_path = input(
            "  Ruta del archivo canciones_lista.txt\n"
            "  (Enter para usar el directorio actual): "
        ).strip()

        if not file_path:
            file_path = "canciones_lista.txt"

        path = Path(file_path)
        if not path.exists():
            self._ui.error(f"No se encontró el archivo: {file_path}")
            input("\n  Presiona Enter para continuar...")
            return

        urls = self._read_urls(path)
        if not urls:
            self._ui.error("El archivo está vacío o no tiene URLs válidas.")
            input("\n  Presiona Enter para continuar...")
            return

        self._ui.info(f"  Se encontraron {len(urls)} canciones para descargar.\n")
        output_dir = self._config.get("download_dir")
        self._config.ensure_dirs()

        failed = []
        completed = 0
        interrupted = False
        try:
            for i, url in enumerate(urls, 1):
                self._ui.info(f"  [{i}/{len(urls)}] Descargando: {url}")
                success, message = self._wrapper.download(url, output_dir)
                completed += 1
                if success:
                    self._ui.success(f"  ✓ Completado: {message}")
                else:
                    self._ui.error(f"  ✗ Falló: {message}")
                    failed.append((url, message))
        except KeyboardInterrupt:
            interrupted = True
            self._ui.warning("\nDescarga interrumpida por el usuario.")

        print()
        if interrupted:
            self._ui.info(
                f"  Proceso cancelado. {completed - len(failed)}/{completed} "
                "descargadas antes de la interrupción."
            )
        else:
            self._ui.info(
                f"  Proceso completado. "
                f"{len(urls) - len(failed)}/{len(urls)} descargadas."
            )
        if failed:
            self._ui.warning("  Las siguientes canciones fallaron:")
            for url, reason in failed:
                print(f"    • {url} → {reason}")

        input("\n  Presiona Enter para continuar...")

    def _read_urls(self, path: Path) -> list[str]:
        """Lee y filtra líneas no vacías del archivo."""
        lines = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        lines.append(line)
        except IOError as e:
            self._ui.error(f"No se pudo leer el archivo: {e}")
        return lines
