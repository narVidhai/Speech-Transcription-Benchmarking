from tqdm import tqdm
from glob import glob
import os, sys

DEBUG_MODE = True
NUM_GPUS = 1
MODEL = 'librispeech.transformer.v1'
WAV_FOLDER = sys.argv[1]
wav_files = glob(os.path.join(WAV_FOLDER, '*.wav'))

ASR_COMMAND = 'recog_wav.sh --ngpu %d --models %s' % (NUM_GPUS, MODEL) + ' %s'
if not DEBUG_MODE:
    ASR_COMMAND += ' 2>&1 >/dev/null'

for wav in tqdm(wav_files):
    os.system(ASR_COMMAND % wav)
