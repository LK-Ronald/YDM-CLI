"""Build the Windows console application as a single-file executable."""
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="ydm-pyinstaller-") as work_dir:
        temporary_build_dir = Path(work_dir)
        spec_dir = temporary_build_dir / "spec"
        spec_dir.mkdir()
        command = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "--console",
            "--noconfirm",
            "--clean",
            "--name",
            "YDM-CLI",
            "--specpath",
            str(spec_dir),
            "--workpath",
            str(temporary_build_dir / "work"),
            "--collect-all",
            "yt_dlp",
            "--collect-all",
            "mutagen",
            "--collect-all",
            "PIL",
            "main.py",
        ]
        subprocess.run(command, cwd=ROOT, check=True)
    print(f"\nCompilación completada: {ROOT / 'dist' / 'YDM-CLI.exe'}")


if __name__ == "__main__":
    main()
