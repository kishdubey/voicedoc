# Change away from subprocess

import subprocess
from application.config import config


def synthesize(output_text, model, speaker_file, language, output_file):
    subprocess.run([
        "tts",
        "--text", f"{output_text}",
        "--model_name", f"{model}",
        "--speaker_wav", f"{speaker_file}",
        "--language_idx", f"{language}",
        "--out_path", f"{output_file}"
    ])


synthesize(config.OUTPUT_TEXT, config.MODEL, config.SPEAKER_FILE,
           config.LANGUAGE, config.SYNTHESIS_FILE)
