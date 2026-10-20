import zipfile
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

from utils import ffmpeg_manager
from utils.ffmpeg_manager import FFmpegManager


class FFmpegManagerTests(unittest.TestCase):
    def test_ensure_reuses_a_working_cached_ffmpeg(self):
        with TemporaryDirectory() as temporary_dir:
            executable = Path(temporary_dir) / "ffmpeg.exe"
            executable.write_bytes(b"ffmpeg")
            manager = FFmpegManager()

            with (
                patch.object(ffmpeg_manager, "FFMPEG_EXE", executable),
                patch.object(FFmpegManager, "_is_usable", return_value=True),
                patch.object(manager, "_download") as download,
            ):
                self.assertEqual(manager.ensure(), executable)

            download.assert_not_called()

    def test_download_extracts_only_ffmpeg_and_cleans_temporary_zip(self):
        with TemporaryDirectory() as temporary_dir:
            app_data = Path(temporary_dir) / "app-data"
            ffmpeg_dir = app_data / "ffmpeg"
            executable = ffmpeg_dir / "ffmpeg.exe"
            manager = FFmpegManager()

            def create_release_zip(_url, filename, reporthook=None):
                with zipfile.ZipFile(filename, "w") as archive:
                    archive.writestr("release/bin/ffmpeg.exe", b"ffmpeg-binary")
                    archive.writestr("release/bin/ffprobe.exe", b"ffprobe-binary")

            with (
                patch.object(ffmpeg_manager, "APP_DATA_DIR", app_data),
                patch.object(ffmpeg_manager, "FFMPEG_DIR", ffmpeg_dir),
                patch.object(ffmpeg_manager, "FFMPEG_EXE", executable),
                patch.object(
                    ffmpeg_manager, "urlretrieve", side_effect=create_release_zip
                ),
                patch.object(
                    FFmpegManager, "_is_usable", side_effect=[False, True, True]
                ),
                patch.object(manager, "_ui"),
            ):
                self.assertEqual(manager.ensure(), executable)

            self.assertEqual(executable.read_bytes(), b"ffmpeg-binary")
            self.assertEqual(list(app_data.glob("ffmpeg-*.zip")), [])
            self.assertEqual(list(ffmpeg_dir.glob("ffmpeg-*.exe")), [])

    def test_download_rejects_release_without_ffmpeg_and_cleans_files(self):
        with TemporaryDirectory() as temporary_dir:
            app_data = Path(temporary_dir) / "app-data"
            ffmpeg_dir = app_data / "ffmpeg"
            executable = ffmpeg_dir / "ffmpeg.exe"
            manager = FFmpegManager()

            def create_release_zip(_url, filename, reporthook=None):
                with zipfile.ZipFile(filename, "w") as archive:
                    archive.writestr("release/bin/ffprobe.exe", b"ffprobe-binary")

            with (
                patch.object(ffmpeg_manager, "APP_DATA_DIR", app_data),
                patch.object(ffmpeg_manager, "FFMPEG_DIR", ffmpeg_dir),
                patch.object(ffmpeg_manager, "FFMPEG_EXE", executable),
                patch.object(
                    ffmpeg_manager, "urlretrieve", side_effect=create_release_zip
                ),
                patch.object(manager, "_ui"),
            ):
                with self.assertRaisesRegex(
                    RuntimeError, "ffmpeg.exe no se encontró"
                ):
                    manager.ensure()

            self.assertFalse(executable.exists())
            self.assertEqual(list(app_data.glob("ffmpeg-*.zip")), [])
            self.assertEqual(list(ffmpeg_dir.glob("ffmpeg-*.exe")), [])


if __name__ == "__main__":
    unittest.main()
