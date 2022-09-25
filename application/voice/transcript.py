import torch
from glob import glob
import random

from application.voice.synthesis import synthesize
from application.voice.edit import concatenate, get_audio, trim
from application.config.config import config


def transcribe(input_file):
    """
    example call
    transcribe(config.speaker_file)[0]
    """
    device = torch.device("cpu")
    model, decoder, utils = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_stt",
        jit_model="jit_xlarge",
        language="en",
        device=device,
    )

    (read_batch, split_into_batches, read_audio, prepare_model_input) = utils

    test_files = glob(input_file)
    batches = split_into_batches(test_files, batch_size=10)
    batch = read_batch(random.sample(batches, k=1)[0])

    input = prepare_model_input(batch, device=device)

    wav_len = input.shape[1] / 16000

    output = model(input)
    transcript = []

    for word in output:
        transcript.append(decoder(word.cpu(), wav_len, word_align=True)[-1])

    return transcript[0]


def to_words(transcript):
    """
    Get just the the words from timestamped transcript object
    """
    transcript_words = []
    for script in transcript:
        transcript_words.append(script["word"])

    return transcript_words


def find_word(word, transcript):
    """
    Find word within timestamped transcript. Returns first occurence of word.
    """
    for script in transcript:
        if script["word"] == word:
            return script

    return None


def delete_word(word, transcript):
    """
    Find word within timestamped transcript. Deletes first occurence of word.
    """
    for script in transcript:
        if script["word"] == word["word"]:
            transcript.remove(script)
            break

    return transcript


def adjust_transcript_delete(time, transcript):
    """
    Adjusts rest of timestamped transcript to reflect deleted clipping of duration, time
    """
    for script in transcript:
        script["start_ts"] = (
            round(script["start_ts"] - time, 3)
            if round(script["start_ts"] - time) > 0
            else 0
        )
        script["end_ts"] = (
            round(script["end_ts"] - time, 3)
            if round(script["end_ts"] - time) > 0
            else 0
        )

    return transcript


def adjust_transcript_add(time, transcript):
    """
    Adjusts rest of timestamped transcript to reflect added clipping of duration, time
    """
    for script in transcript:
        script["start_ts"] = round(script["start_ts"] + time, 3)
        script["end_ts"] = round(script["end_ts"] + time, 3)

    return transcript


def get_timestamps(words, transcript):
    """
    Get timestamps for transcript for list of words
    """
    word_timestamps = []
    for word in words:
        word_timestamps.append(find_word(word, transcript))
    return list(filter(None, word_timestamps))


def remove_words(word_timestamps, transcript):
    """
    Remove words from transcript and from audio
    """
    iterate_list = word_timestamps[:]
    for word in iterate_list:
        difference = (
            round(word["end_ts"] - word["start_ts"], 3)
            if (round(word["end_ts"] - word["start_ts"], 3)) > 0
            else 0
        )
        time_start = (
            round(word["start_ts"] - difference * 2, 3)
            if round(word["start_ts"] - difference * 2, 3) > 0
            else 0
        )
        time_end = word["end_ts"] + difference * 2
        time = (
            round(time_end - time_start, 3)
            if round(time_end - time_start, 3) > 0
            else 0
        )

        # remove word from audio and transcript and unvalid_word_timestamps
        trim(config.transcribe_file, time_start, time_end)

        delete_word(word, transcript)
        delete_word(word, word_timestamps)

        adjust_transcript_delete(time, transcript)
        adjust_transcript_delete(time, word_timestamps)


def add_words(words, transcript):
    """
    Add synthesizied speech to audio and adjust transcript
    """
    ptr_transcript = 0
    for i in range(len(words)):
        if words[i] != transcript[ptr_transcript]["word"]:
            synthesize(
                words[i],
                config.model,
                config.transcribe_file,
                config.language,
                config.synthesis_file,
            )

            synthesized_audio = get_audio(config.synthesis_file)
            time_start = transcript[ptr_transcript]["start_ts"]
            time = synthesized_audio.duration_seconds
            concatenate(config.transcribe_file, config.synthesis_file, time_start)

            adjust_transcript_add(time, transcript)

        elif ptr_transcript < len(transcript) - 1:
            ptr_transcript += 1
