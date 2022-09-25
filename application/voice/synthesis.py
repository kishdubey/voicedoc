import subprocess
from application.config.config import config


def synthesize(output_text, model, speaker_file, language, output_file):
    """
    example call
    synthesize(config.output_text, config.model, config.speaker_file,
           config.language, synthesis_file)
    """
    subprocess.run(
        [
            "tts",
            "--text",
            f"{output_text}",
            "--model_name",
            f"{model}",
            "--speaker_wav",
            f"{speaker_file}",
            "--language_idx",
            f"{language}",
            "--out_path",
            f"{output_file}",
        ]
    )
