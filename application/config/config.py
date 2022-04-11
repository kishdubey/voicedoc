import os

SPEAKER_FILE = os.path.abspath('application/audio/record.wav')
SYNTHESIS_FILE = os.path.abspath('application/audio/synthesis.wav')

RECORD_DURATION = 60

OUTPUT_TEXT = 'Hello World. Making sure this sounds human enough.'
MODEL = 'tts_models/multilingual/multi-dataset/your_tts'

LANGUAGE = 'en'