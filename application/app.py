from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from application.config.config import config
from application.voice.transcribe import transcribe
from application.voice.synthesis import synthesize
from application.voice import edit
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.upload_folder


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        config.speaker_file = f.filename
        return render_template("edit.html")


if __name__ == "__main__":
    app.run(debug=True)
