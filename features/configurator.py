"""
Configurador interactivo - permite al usuario personalizar los directorios y ajustes.
"""
from pathlib import Path
from core.config_manager import (
    CONCURRENT_FRAGMENT_DOWNLOADS_MAX,
    CONCURRENT_FRAGMENT_DOWNLOADS_MIN,
    SOCKET_TIMEOUT_MAX,
    SOCKET_TIMEOUT_MIN,
    ConfigManager,
)
from utils.ui import UI

BITRATE_OPTIONS = ["128k", "192k", "256k", "320k"]
FORMAT_OPTIONS = ["mp3", "flac", "wav", "aac", "m4a", "opus", "ogg"]


class Configurator:
    """Permite al usuario configurar el programa de forma interactiva."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()

    def run(self) -> None:
        self._ui.section("Configuración")
        self._show_current()

        print("\n  ¿Qué deseas configurar?")
        print("  [1] Directorio de descargas")
        print("  [2] Directorio de conversiones")
        print("  [3] Formato de descarga por defecto")
        print("  [4] Bitrate de descarga")
        print("  [5] Tiempo máximo de espera de conexión")
        print("  [6] Descargas simultáneas de fragmentos")
        print("  [7] Volver al menú principal")

        choice = input("\n  Selecciona: ").strip()

        if choice == "1":
            self._set_dir("download_dir", "Directorio de descargas")
        elif choice == "2":
            self._set_dir("converted_dir", "Directorio de conversiones")
        elif choice == "3":
            self._set_format()
        elif choice == "4":
            self._set_bitrate()
        elif choice == "5":
            self._set_integer(
                "socket_timeout",
                "Tiempo máximo de espera de conexión (segundos)",
                SOCKET_TIMEOUT_MIN,
                SOCKET_TIMEOUT_MAX,
            )
        elif choice == "6":
            self._set_integer(
                "concurrent_fragment_downloads",
                "Descargas simultáneas de fragmentos",
                CONCURRENT_FRAGMENT_DOWNLOADS_MIN,
                CONCURRENT_FRAGMENT_DOWNLOADS_MAX,
            )
        elif choice == "7":
            return
        else:
            self._ui.error("Opción no válida.")

        input("\n  Presiona Enter para continuar...")

    def _show_current(self) -> None:
        all_cfg = self._config.get_all()
        print("\n  Configuración actual:")
        print(f"    📁 Descargas    : {all_cfg.get('download_dir')}")
        print(f"    📁 Conversiones : {all_cfg.get('converted_dir')}")
        print(f"    🎵 Formato      : {all_cfg.get('default_format')}")
        print(f"    📻 Bitrate      : {all_cfg.get('bitrate')}")
        print(f"    ⏱️  Timeout      : {all_cfg.get('socket_timeout')} s")
        print(
            "    🔀 Fragmentos   : "
            f"{all_cfg.get('concurrent_fragment_downloads')} simultáneos"
        )

    def _set_dir(self, key: str, label: str) -> None:
        current = self._config.get(key)
        new_val = input(f"\n  {label} [{current}]: ").strip()
        if not new_val:
            self._ui.info("  Sin cambios.")
            return
        path = Path(new_val)
        try:
            path.mkdir(parents=True, exist_ok=True)
            self._config.set(key, str(path))
            self._config.save()
            self._ui.success(f"Guardado: {path}")
        except Exception as e:
            self._ui.error(f"No se pudo crear el directorio: {e}")

    def _set_format(self) -> None:
        current = self._config.get("default_format")
        print(f"\n  Formatos disponibles: {', '.join(FORMAT_OPTIONS)}")
        new_val = input(f"  Formato [{current}]: ").strip().lower()
        if not new_val:
            self._ui.info("  Sin cambios.")
            return
        if new_val not in FORMAT_OPTIONS:
            self._ui.error(f"Formato no reconocido: {new_val}")
            return
        self._config.set("default_format", new_val)
        self._config.save()
        self._ui.success(f"Formato actualizado a: {new_val}")

    def _set_bitrate(self) -> None:
        current = self._config.get("bitrate")
        print(f"\n  Bitrates disponibles: {', '.join(BITRATE_OPTIONS)}")
        new_val = input(f"  Bitrate [{current}]: ").strip().lower()
        if not new_val:
            self._ui.info("  Sin cambios.")
            return
        if new_val not in BITRATE_OPTIONS:
            self._ui.error(f"Bitrate no reconocido: {new_val}")
            return
        self._config.set("bitrate", new_val)
        self._config.save()
        self._ui.success(f"Bitrate actualizado a: {new_val}")

    def _set_integer(
        self,
        key: str,
        label: str,
        minimum: int,
        maximum: int,
    ) -> None:
        current = self._config.get(key)
        new_val = input(
            f"\n  {label} [{current}] ({minimum}-{maximum}): "
        ).strip()
        if not new_val:
            self._ui.info("  Sin cambios.")
            return
        try:
            value = int(new_val)
        except ValueError:
            self._ui.error("Ingresa un número entero.")
            return
        if not minimum <= value <= maximum:
            self._ui.error(f"El valor debe estar entre {minimum} y {maximum}.")
            return
        self._config.set(key, value)
        self._config.save()
        self._ui.success(f"{label} actualizado a: {value}")
