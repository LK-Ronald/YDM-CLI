"""
Menú principal - Principio Abierto/Cerrado (OCP)
Coordina las opciones sin conocer detalles de implementación.
"""
from core.config_manager import ConfigManager
from features.downloader import Downloader
from features.batch_downloader import BatchDownloader
from features.converter import Converter
from features.configurator import Configurator
from utils.ui import UI


class Menu:
    """Menú interactivo principal del programa."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()
        self._downloader = Downloader(config_manager)
        self._batch = BatchDownloader(config_manager)
        self._converter = Converter(config_manager)
        self._configurator = Configurator(config_manager)

    def run(self) -> None:
        """Bucle principal del menú."""
        self._ui.print_banner()
        while True:
            self._ui.print_menu()
            choice = input("\n  Selecciona una opción: ").strip()
            self._dispatch(choice)

    def _dispatch(self, choice: str) -> None:
        options = {
            "1": self._downloader.run,
            "2": self._batch.run,
            "3": self._converter.run,
            "4": self._configurator.run,
            "5": self._exit,
        }
        action = options.get(choice)
        if action:
            action()
        else:
            self._ui.error("Opción no válida. Elige entre 1 y 5.")

    def _exit(self) -> None:
        self._ui.success("¡Hasta luego! 🎵")
        raise SystemExit(0)
