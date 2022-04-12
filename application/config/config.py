import os
from dataclasses import dataclass, field
from enum import Enum, auto


class Language(Enum):
    en = auto()
    fr = auto()
    ds = auto()


class Model(Enum):
    yourtts = 'tts_models/multilingual/multi-dataset/your_tts'


@dataclass
class Config:
    speaker_file:    str
    synthesis_file:  str
    duration:        int
    output_text:     str
    model:           Model
    language:        Language

    _speaker_file:   str = field(init=False, repr=False)
    _synthesis_file: str = field(init=False, repr=False)
    _duration:       int = field(init=False, repr=False)
    _output_text:    str = field(init=False, repr=False)
    _model:          Model = field(init=False, repr=False)
    _language:       Language = field(init=False, repr=False)

    '''speaker_file getters and setters'''
    @property
    def speaker_file(self) -> str:
        return self._speaker_file

    @speaker_file.setter
    def speaker_file(self, speaker_file: str):
        self._speaker_file = speaker_file

    '''synthesis_file getters and setters'''
    @property
    def synthesis_file(self) -> str:
        return self._synthesis_file

    @synthesis_file.setter
    def synthesis_file(self, synthesis_file: str):
        self._synthesis_file = synthesis_file

    '''duration getters and setters'''
    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, duration: int):
        self._duration = duration

    '''output_text getters and setters'''
    @property
    def output_text(self) -> str:
        return self._output_text

    @output_text.setter
    def output_text(self, output_text: str):
        self._output_text = output_text

    '''model getters and setters'''
    @property
    def model(self) -> Model:
        return self._model

    @model.setter
    def model(self, model: Model):
        self._model = model

    '''language getters and setters'''
    @property
    def language(self) -> Language:
        return self._language

    @language.setter
    def language(self, language: Language):
        self._language = language


config = Config(
    speaker_file    = os.path.abspath('application/audio/record.wav'),
    synthesis_file  = os.path.abspath('application/audio/synthesis.wav'),
    duration        = 60,
    output_text     = 'Hello World. Making sure this sounds human enough.',
    model           = Model.yourtts.value,
    language        = Language.en.name
)
