# Silero STT

import torch
import zipfile
from glob import glob

device = torch.device('cpu')

model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en',
                                       device=device)
(read_batch, split_into_batches,
 read_audio, prepare_model_input) = utils

test_files = glob("audio/record.wav")
batches = split_into_batches(test_files, batch_size=10)
input = prepare_model_input(read_batch(batches[0]),
                            device=device)

output = model(input)
for example in output:
    print(decoder(example.cpu()))
