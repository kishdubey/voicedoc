# Silero STT

import torch
from application.config.config import config
from glob import glob
import random


def transcribe(input_file):
    '''
    example call
    transcribe(config.speaker_file)[0]
    '''
    device = torch.device('cpu')
    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_stt',
                                           jit_model='jit_xlarge',
                                           language='en',
                                           device=device)

    (read_batch, split_into_batches,
     read_audio, prepare_model_input) = utils

    test_files = glob(input_file)
    batches = split_into_batches(test_files, batch_size=10)
    batch = read_batch(random.sample(batches, k=1)[0])

    input = prepare_model_input(batch,
                                device=device)

    wav_len = input.shape[1] / 16000

    output = model(input)
    transcript = []

    for word in output:
        transcript.append(decoder(word.cpu(), wav_len, word_align=True)[-1])

    return transcript[0]


def to_words(transcript):
    '''
    Get just the the words from timestamped transcript object  
    '''
    transcript_words = []
    for script in transcript:
        transcript_words.append(script['word'])

    return transcript_words


def find_word(word, transcript):
    '''
    Find word within timestamped transcript. Returns first occurence of word.
    '''
    for script in transcript:
        if script['word'] == word:
            return script

    return None


def delete_word(word, transcript):
    '''
    Find word within timestamped transcript. Returns first occurence of word.
    '''
    for script in transcript:
        if script == word:
            transcript.remove(script)
            
    return transcript


def adjust_transcript(time, transcript):
    '''
    Adjusts rest of timestamped transcript to reflect deleted clipping of duration, time
    '''
    for script in transcript:
        script['start_ts'] -= time
        script['end_ts'] -= time

    return transcript
