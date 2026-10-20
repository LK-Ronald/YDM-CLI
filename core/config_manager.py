"""
Gestor de configuración - Principio de Responsabilidad Única (SRP)
Maneja toda la lógica de lectura/escritura de configuración.
"""
import json
import os
from pathlib import Path


DEFAULT_CONFIG = {
    "download_dir": str(Path.home() / "Music" / "Downloads"),
    "converted_dir": str(Path.home() / "Music" / "Converted"),
    "default_format": "mp3",
    "bitrate": "320k",
    "socket_timeout": 30,
    "concurrent_fragment_downloads": 4,
}

SOCKET_TIMEOUT_MIN = 5
SOCKET_TIMEOUT_MAX = 120
CONCURRENT_FRAGMENT_DOWNLOADS_MIN = 1
CONCURRENT_FRAGMENT_DOWNLOADS_MAX = 8

CONFIG_FILE = Path.home() / ".ytdl_music_config.json"


class ConfigManager:
    """Gestiona la configuración persistente del programa."""

    def __init__(self):
        self._config: dict = {}
        self._load()

    def _load(self) -> None:
        """Carga la configuración desde archivo, usa defaults si no existe."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                self._config = {
                    **DEFAULT_CONFIG,
                    **loaded_config,
                } if isinstance(loaded_config, dict) else DEFAULT_CONFIG.copy()
            except (json.JSONDecodeError, IOError):
                self._config = DEFAULT_CONFIG.copy()
        else:
            self._config = DEFAULT_CONFIG.copy()

    def save(self) -> None:
        """Guarda la configuración actual en disco."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise RuntimeError(f"No se pudo guardar la configuración: {e}")

    def get(self, key: str, fallback=None):
        return self._config.get(key, fallback)

    def set(self, key: str, value) -> None:
        self._config[key] = value

    def get_all(self) -> dict:
        return self._config.copy()

    def ensure_dirs(self) -> None:
        """Crea los directorios configurados si no existen."""
        for key in ("download_dir", "converted_dir"):
            path = Path(self._config.get(key, ""))
            if path:
                path.mkdir(parents=True, exist_ok=True)
