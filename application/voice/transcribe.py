# Silero STT

import torch
from application.config import config
from glob import glob


def transcribe(input_file):
    device = torch.device('cpu')

    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_stt',
                                           language='en',
                                           device=device)

    (read_batch, split_into_batches,
     read_audio, prepare_model_input) = utils

    test_files = glob(input_file)
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    output_text = []
    for _ in output:
        output_text.append(decoder(_.cpu()))

    return ''.join(output_text)


print(transcribe(config.SPEAKER_FILE))
