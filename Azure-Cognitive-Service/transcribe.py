# TODO: Use batch API instead of sending 1-by-1: https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python
import azure.cognitiveservices.speech as speechsdk
import os
from tqdm import tqdm
from glob import glob

SPEECH_CONFIG = speechsdk.SpeechConfig(subscription="<paste-speech-key-here>", region="<paste-speech-region-here>", speech_recognition_language="en-IN")

def recognize_wav(local_file_path):
    audio_input = speechsdk.AudioConfig(filename=local_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=SPEECH_CONFIG, audio_config=audio_input)
    result = speech_recognizer.recognize_once_async().get()
    return result.text

def recognize_bulk_wav(wav_folder, output_folder, overwrite=True):
    print('Running STT for audio files in:', wav_folder)
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
    recognize_bulk_wav('wav_folder', 'output_ms')
