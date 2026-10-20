"""
YouTube Downloader Music - Punto de entrada principal
"""
from core.menu import Menu
from core.config_manager import ConfigManager
from utils.ffmpeg_manager import FFmpegManager
from utils.ui import UI


def main():
    ui = UI()
    ui.print_banner()

    try:
        FFmpegManager().ensure()
    except RuntimeError as error:
        ui.error(str(error))
        input("\n  Presiona Enter para salir...")
        raise SystemExit(1) from error

    config_manager = ConfigManager()
    menu = Menu(config_manager)
    menu.run()


if __name__ == "__main__":
    main()
