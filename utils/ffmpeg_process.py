"""Helpers for running FFmpeg without leaving child processes on interruption."""
import subprocess


def run_ffmpeg(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        if process.poll() is None:
            process.kill()
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(
            command,
            timeout,
            output=stdout,
            stderr=stderr,
        ) from error
    except KeyboardInterrupt:
        if process.poll() is None:
            try:
                process.terminate()
            except OSError:
                pass
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            if process.poll() is None:
                try:
                    process.kill()
                except OSError:
                    pass
            process.communicate()
        raise

    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
