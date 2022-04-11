import subprocess
from application.config import config


def record(file, duration):
    subprocess.run([
        "arerecprd",
        "-vv",
        "--format=cd",
        "--duration", f"{duration}",
        f"{file}"
    ])


record(config.SPEAKER_FILE, config.RECORD_DURATION)
