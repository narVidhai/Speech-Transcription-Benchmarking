## Google Speech2Text Bulk Speech Transcribe - Python

### Steps

1. Setup Google Speech library locally and download Service account JSON. ([Reference](https://cloud.google.com/speech-to-text/docs/libraries#client-libraries-install-python))
2. Set the JSON path in the script `gAPI.py` in the line 4 `os.environ['GOOGLE_APPLICATION_CREDENTIALS']`
3. Set the input `wav_folder` (audios path) and destination `output_folder` (transcripts path) in the last line of the same script
4. To bulk transcribe: `python gAPI.py`
