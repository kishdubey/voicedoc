import os
import ast

from flask import Flask, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.edit import get_audio, concatenate
from application.voice.synthesis import synthesize
from application.voice.transcript import (
    get_timestamps,
    remove_words,
    transcribe,
    to_words,
    adjust_transcript_add
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.upload_folder
app.secret_key = "super secret key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        f = request.files["file"]
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        config.speaker_file = "audio/" + f.filename
        config.transcribe_file = os.path.abspath(f"{config.upload_folder}/{f.filename}")

        transcript = transcribe(config.transcribe_file)
    return render_template(
        "edit.html",
        audio_file=config.speaker_file,
        transcript=transcript,
        transcript_words=to_words(transcript),
    )


@app.route("/handle_data", methods=["GET", "POST"])
def handle_data():
    if request.method == "POST":
        valid_words = request.form["validWords"].split(",")
        unvalid_words = request.form["unvalidWords"].split(",")
        transcript_words = ast.literal_eval(request.form["transcriptWords"])
        transcript = ast.literal_eval(request.form["transcript"])

        # getting timestamps for unvalid words
        unvalid_word_timestamps = get_timestamps(unvalid_words, transcript)

        # removing unvalid words from transcript and audio
        transcript = remove_words(unvalid_word_timestamps, transcript)

        ptr_transcript = 0
        for i in range(len(valid_words)):
            if valid_words[i] != transcript[ptr_transcript]["word"]:
                synthesize(
                    valid_words[i],
                    config.model,
                    config.transcribe_file,
                    config.language,
                    config.synthesis_file,
                )

                synthesized_audio = get_audio(config.synthesis_file)

                # concat new synthesized audio to config.transcribe_file
                time_start = transcript[ptr_transcript]['start_ts']
                time = synthesized_audio.duration_seconds

                concatenate(config.transcribe_file, config.synthesis_file, time_start)

                # adjust transcript
                adjust_transcript_add(time, transcript)

            elif ptr_transcript < len(transcript) - 1:
                ptr_transcript += 1

    # sending edited file back
    filename = config.transcribe_file.split("/")[-1]
    return send_file(config.transcribe_file, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
