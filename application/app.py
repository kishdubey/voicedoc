import os

from flask import Flask, redirect, render_template, request, flash, url_for
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.transcribe import transcribe, to_words
from application.voice.synthesis import synthesize
from application.voice import edit

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.upload_folder
app.secret_key = "super secret key"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        config.speaker_file = 'audio/' + f.filename
        config.transcribe_file = os.path.abspath(
            f"{config.upload_folder}/{f.filename}")

        transcript = transcribe(config.transcribe_file)
    return render_template("edit.html", audio_file=config.speaker_file, transcript=transcript, transcript_words=to_words(transcript))
    return redirect(url_for('index'))


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # updatedTranscript, transcript, transcriptWords
    return request.form['transcriptWords']


if __name__ == "__main__":
    app.run(debug=True)
