import os
import ast

from flask import Flask, current_app, redirect, render_template, request, flash, send_file, send_from_directory, url_for
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.transcribe import transcribe, to_words, find_word, delete_word, adjust_transcript
from application.voice.synthesis import synthesize
from application.voice.edit import trim

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


@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        valid_words = request.form['validWords'].split(',')
        unvalid_words = request.form['unvalidWords'].split(',')
        transcript_words = ast.literal_eval(request.form['transcriptWords'])
        transcript = ast.literal_eval(request.form['transcript'])

        # getting timestamps for unvalid words
        unvalid_word_timestamps = []
        for word in unvalid_words:
            unvalid_word_timestamps.append(find_word(word, transcript))
        unvalid_word_timestamps = list(filter(None, unvalid_word_timestamps))

        for word in unvalid_word_timestamps:
            time = word['end_ts'] - word['start_ts']
            time_start = word['start_ts'] - time * \
                2 if (word['start_ts'] - time*2) > 0 else 0
            time_end = word['end_ts'] + time

            # remove word from transcript audio from unvalid_word_timestamps
            trim(config.transcribe_file, time_start, time_end)

            # delete that word obj from unvalid_word_timestamps and transcript
            delete_word(word, transcript)
            delete_word(word, unvalid_word_timestamps)

            # adjust_transcript transcript and unvalid_word_timestamps
            adjust_transcript(time, transcript)
            adjust_transcript(time, unvalid_word_timestamps)

        # find word to add in betweeen two valid words
        # syntheizes that word
        # append in between end_ts and start_ts of words on left and right respectively

    # sending file 
    filename = config.transcribe_file.split('/')[-1]
    return send_file(config.transcribe_file, download_name=filename)

if __name__ == "__main__":
    app.run(debug=True)
