import os, sys, io
from glob import glob
from tqdm import tqdm
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'GCP_SERVICE_ACCOUNT.json'

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

client = speech_v1.SpeechClient()

config = {
        "language_code": "en-IN",
        "sample_rate_hertz": 16000,
    }

def recognize_wav(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """
    
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        return result.alternatives[0].transcript
    return None

def recognize_bulk_wav(wav_folder, output_folder, overwrite=True):
    print('Running gAPI for audio files in:', wav_folder)
    os.makedirs(output_folder, exist_ok=True)
    audio_files = sorted(glob(os.path.join(wav_folder, '*.wav')))
    for audio_file in tqdm(audio_files, unit='transcript'):
        txt_file = os.path.join(output_folder, os.path.basename(audio_file).replace('.wav', '.txt'))
        if not overwrite and os.path.isfile(txt_file):
            continue
        
        transcript = recognize_wav(audio_file)
        if not transcript:
            print('Failed for:', audio_file)
            continue
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
    return

if __name__ == '__main__':
    recognize_bulk_wav('wav_folder', 'output_google')
