# TODO: Use batch API instead of sending 1-by-1: https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python
import azure.cognitiveservices.speech as speechsdk
import os
from tqdm import tqdm
from glob import glob
import time

LANGUAGE = 'en-IN'
SPEECH_CONFIG = speechsdk.SpeechConfig(subscription="<paste-speech-key-here>", region="<paste-speech-region-here>", speech_recognition_language=LANGUAGE)

def log(text):
    # print(text)
    return

def recognize_single_utterance(local_file_path):
    audio_input = speechsdk.AudioConfig(filename=local_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=SPEECH_CONFIG, audio_config=audio_input, language=LANGUAGE)
    result = speech_recognizer.recognize_once()
    return result.text

def recognize_continuous(local_file_path):
    '''
    Modified from: https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/4f9ee79c2287a5a00dcd1a50112cd43694aa7286/samples/python/console/speech_sample.py#L321
    '''
    audio_config = speechsdk.audio.AudioConfig(filename=local_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=SPEECH_CONFIG, audio_config=audio_config, language=LANGUAGE)

    done = False
    transcript = ''

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        log('CLOSING on {}'.format(evt))
        nonlocal done
        done = True
    
    def recognized_cb(evt):
        """When recognizing phase is complete for a single instance, it returns a final utterance before proceeding next"""
        log('RECOGNIZED: {}'.format(evt))
        nonlocal transcript
        transcript += ' ' + evt.result.text

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: log('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: log('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: log('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: log('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    return transcript.strip()

def recognize_bulk_wav(wav_folder, output_folder, overwrite=True):
    print('Running STT for audio files in:', wav_folder)
    os.makedirs(output_folder, exist_ok=True)
    audio_files = sorted(glob(os.path.join(wav_folder, '*.wav')))
    for audio_file in tqdm(audio_files, unit='transcript'):
        txt_file = os.path.join(output_folder, os.path.basename(audio_file).replace('.wav', '.txt'))
        if not overwrite and os.path.isfile(txt_file):
            continue
        
        transcript = recognize_continuous(audio_file)
        if not transcript:
            print('Failed for:', audio_file)
            continue
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
    return

if __name__ == '__main__':
    recognize_bulk_wav('wav_folder', 'output_ms')
