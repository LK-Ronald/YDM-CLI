"""
Utilidades de interfaz de usuario - colores ANSI y helpers de presentación.
Principio de Responsabilidad Única: solo se ocupa de mostrar texto en consola.
"""
import os
import platform


def _supports_color() -> bool:
    """Detecta si la terminal soporta colores ANSI."""
    if platform.system() == "Windows":
        # Windows 10+ con ANSI habilitado
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            # Habilitar VIRTUAL_TERMINAL_PROCESSING
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True


_COLOR = _supports_color()

# Códigos ANSI
RESET  = "\033[0m"  if _COLOR else ""
BOLD   = "\033[1m"  if _COLOR else ""
GREEN  = "\033[92m" if _COLOR else ""
YELLOW = "\033[93m" if _COLOR else ""
RED    = "\033[91m" if _COLOR else ""
CYAN   = "\033[96m" if _COLOR else ""
BLUE   = "\033[94m" if _COLOR else ""
MAGENTA= "\033[95m" if _COLOR else ""


class UI:
    """Métodos de presentación en consola."""

    def print_banner(self) -> None:
        os.system("cls" if platform.system() == "Windows" else "clear")
        banner = f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════════╗
  ║   🎵  YouTube Downloader Music  🎵               ║
  ║   Descarga y convierte música fácilmente         ║
  ╚══════════════════════════════════════════════════╝
{RESET}"""
        print(banner)

    def print_menu(self) -> None:
        print(f"\n{BOLD}  ── Menú Principal ──{RESET}")
        options = [
            ("1", "Descargar música"),
            ("2", "Descargar lista de músicas desde archivo"),
            ("3", "Descargar playlist o álbum"),
            ("4", "Convertir archivos a otro formato"),
            ("5", "Configuración"),
            ("6", "Salir"),
        ]
        for num, label in options:
            print(f"  {CYAN}[{num}]{RESET} {label}")

    def section(self, title: str) -> None:
        print(f"\n{BLUE}{BOLD}  ── {title} ──{RESET}\n")

    def info(self, message: str) -> None:
        print(f"{CYAN}ℹ{RESET}  {message}")

    def success(self, message: str) -> None:
        print(f"{GREEN}✔{RESET}  {message}")

    def error(self, message: str) -> None:
        print(f"{RED}✘{RESET}  {message}")

    def warning(self, message: str) -> None:
        print(f"{YELLOW}⚠{RESET}  {message}")
