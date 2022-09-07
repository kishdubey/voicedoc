from pydub import AudioSegment


def get_audio(filepath):
    return AudioSegment.from_wav(filepath)


def trim(audio_path, time_start, time_finish):
    '''
    Remove words from audio.
    '''
    audio = get_audio(audio_path)
    trim = audio[:_to_milliseconds(time_start)] + audio[_to_milliseconds(time_finish):]

    trim.export(audio_path, format="wav")


def concatenate(audio1, audio2, timestamp):
    '''
    Adding synthesized audio at duration to another audio
    '''
    pass


def slice(audio, duration, before=True):
    '''
    boolean: before
    first part of clipping unitl duration is returned if 'before' is True. 
    second part of clipping after duration is returned if 'before' is False.
    '''
    return audio[:_to_milliseconds(duration)] if before else audio[_to_milliseconds(duration):]


def _to_seconds(ms):
    return ms/1000


def _to_milliseconds(s):
    return s*1000