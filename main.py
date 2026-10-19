"""
YouTube Downloader Music - Punto de entrada principal
"""
import sys
from core.menu import Menu
from core.config_manager import ConfigManager


def main():
    config_manager = ConfigManager()
    menu = Menu(config_manager)
    menu.run()


if __name__ == "__main__":
    main()
