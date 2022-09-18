import os
import ast

from flask import Flask, redirect, render_template, request, flash, url_for
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.transcribe import transcribe, to_words, find_word
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
    valid_words = request.form['validWords'].split(',')
    unvalid_words = request.form['unvalidWords'].split(',')
    transcript_words = ast.literal_eval(request.form['transcriptWords'])
    transcript = ast.literal_eval(request.form['transcript'])

    unvalid_word_timestamps = []  # getting timestamps for unvalid words
    for word in unvalid_words:
        word_timestamp = find_word(word, transcript)
        unvalid_word_timestamps.append(word_timestamp)

    # remove word from transcript from unvalid_word_timestamps
    # delete that words from unvalid_word_timestamps
    # adjust_transcript unvalid_word_timestamps and transcript
    # loop

    # find word to add in betweeen two valid words
    # syntheizes that word
    # append in between end_ts and start_ts of words on left and right respectively

    return request.form['validWords']


if __name__ == "__main__":
    app.run(debug=True)
