from pydub import AudioSegment


def get_audio(filepath):
    return AudioSegment.from_wav(filepath)


def trim(audio, duration, before=True):
    '''
    boolean: before
    first part of clipping unitl duration is returned if 'before' is True. 
    second part of clipping after duration is returned if 'before' is False.
    '''
    return audio[:_to_milliseconds(duration)] if before else audio[_to_milliseconds(duration):]


def concatenate(audio1, audio2):
    return audio1 + audio2


def to_wav(audio):
    '''
    convert audio to wav format
    '''
    pass


def _to_seconds(ms):
    return ms/1000


def _to_milliseconds(s):
    return s*1000
