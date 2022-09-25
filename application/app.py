import os
import ast

from flask import Flask, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.transcript import (
    add_words,
    get_timestamps,
    remove_words,
    transcribe,
    to_words
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
        transcript = ast.literal_eval(request.form["transcript"])

        valid_words = list(filter(lambda a: a != 'undefined', request.form["validWords"].split(",")))
        unvalid_words = request.form["unvalidWords"].split(",")
        unvalid_word_timestamps = get_timestamps(unvalid_words, transcript)

        remove_words(unvalid_word_timestamps, transcript)
        add_words(valid_words, transcript)

    filename = config.transcribe_file.split("/")[-1]
    return send_file(config.transcribe_file, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
