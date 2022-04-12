import subprocess
from application.config.config import config


def record(file, duration):
    subprocess.run([
        "arerecprd",
        "-vv",
        "--format=cd",
        "--duration", f"{duration}",
        f"{file}"
    ])


record(config.speaker_file, config.duration)
