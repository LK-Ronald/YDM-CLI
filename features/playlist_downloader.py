"""
Descargador de playlists y álbumes - SRP: descarga colecciones completas.
Soporta URLs de listas de reproducción y álbumes de YouTube y YouTube Music.
Organiza las pistas en una subcarpeta con numeración ordenada y reporte detallado.
"""
from pathlib import Path

from core.config_manager import ConfigManager
from utils.ui import UI
from utils.ytdlp_wrapper import YtDlpWrapper


class PlaylistDownloader:
    """Descarga playlists o álbumes completos desde YouTube y YouTube Music."""

    def __init__(self, config_manager: ConfigManager):
        self._config = config_manager
        self._ui = UI()
        self._wrapper = YtDlpWrapper(config_manager)

    def run(self) -> None:
        self._ui.section("Descargar playlist o álbum")
        url = input("  Ingresa el link de la playlist o álbum (YouTube / YouTube Music): ").strip()

        if not url:
            self._ui.error("No ingresaste ningún link.")
            input("\n  Presiona Enter para continuar...")
            return

        output_dir = self._config.get("download_dir")
        self._config.ensure_dirs()

        self._ui.info(f"Directorio base: {output_dir}")
        self._ui.info("Obteniendo información de la playlist o álbum...\n")

        try:
            success, info_or_error = self._wrapper.extract_info(url)
        except KeyboardInterrupt:
            self._ui.warning("\nObtención de información interrumpida por el usuario.")
            input("\n  Presiona Enter para continuar...")
            return
        if not success:
            self._ui.error(f"Error al obtener información: {info_or_error}")
            input("\n  Presiona Enter para continuar...")
            return

        info = info_or_error
        title = info.get("title") or "Playlist"
        raw_entries = info.get("entries")

        # Si el enlace resultó ser un video individual
        if raw_entries is None:
            self._ui.info("El enlace corresponde a una pista individual. Descargando canción...")
            try:
                ok, msg = self._wrapper.download(url, output_dir, noplaylist=True)
            except KeyboardInterrupt:
                self._ui.warning("\nDescarga interrumpida por el usuario.")
                input("\n  Presiona Enter para continuar...")
                return
            if ok:
                self._ui.success(f"Descarga completada: {msg}")
            else:
                self._ui.error(f"Error al descargar: {msg}")
            input("\n  Presiona Enter para continuar...")
            return

        entries = [e for e in raw_entries if e]
        total = len(entries)

        if total == 0:
            self._ui.error("La playlist o álbum no contiene canciones disponibles.")
            input("\n  Presiona Enter para continuar...")
            return

        # Sanitizar nombre de la subcarpeta para evitar caracteres ilegales en disco
        safe_folder_name = "".join(c for c in title if c not in '<>:"/\\|?*').strip() or "Playlist"
        target_dir = Path(output_dir) / safe_folder_name
        target_dir.mkdir(parents=True, exist_ok=True)

        self._ui.info(f"Colección detectada: {title}")
        self._ui.info(f"Total de canciones: {total}")
        self._ui.info(f"Carpeta destino: {target_dir}\n")

        failed: list[tuple[str, str]] = []

        try:
            for i, entry in enumerate(entries, 1):
                track_title = entry.get("title") or f"Pista {i}"
                video_id = entry.get("id")
                track_url = entry.get("url")

                if not track_url or not track_url.startswith("http"):
                    track_url = f"https://www.youtube.com/watch?v={video_id}" if video_id else None

                if not track_url:
                    self._ui.error(f"  [{i}/{total}] {track_title} → No se encontró URL válida.")
                    failed.append((track_title, "URL no disponible"))
                    continue

                self._ui.info(f"  [{i}/{total}] {track_title}")
                ok, msg = self._wrapper.download(
                    track_url,
                    str(target_dir),
                    noplaylist=True,
                )

                if ok:
                    self._ui.success(f"  ✓ Descargado: {msg}")
                else:
                    self._ui.error(f"  ✗ Falló: {msg}")
                    failed.append((track_title, msg))

            print()
            downloaded_count = total - len(failed)
            self._ui.info(f"Proceso completado. {downloaded_count}/{total} canciones descargadas.")
            self._ui.info(f"Guardadas en: {target_dir}")

            if failed:
                self._ui.warning("Las siguientes canciones no se pudieron descargar:")
                for item, reason in failed:
                    print(f"    • {item} → {reason}")

        except KeyboardInterrupt:
            self._ui.warning("\nDescarga interrumpida por el usuario.")

        input("\n  Presiona Enter para continuar...")
