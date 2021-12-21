# Code for Speech-To-Text Online APIs - Python Scripts

## Bulk Audio Transcription using Speech Transcription Services

### Initial Steps

0. Ensure you have Python 3
1. Clone this repo and `cd` into it.
2. Go into each folder for specific services and check the `README` files

### Supported Services

- [Google Speech-To-Text](Google-Speech2Text/)
- [AWS Transcribe](AWS-Transcribe/)
- [Microsoft Cognitive Service](Azure-Cognitive-Service/)
- [Rev.ai (Temi Speech) API](RevAI-Temi-API/)

Please feel free to contribute for other online speech transcriptions that you are aware of.

### Input format

Ensure you have a folder of audio files in `WAV` format. (For example, `wav_folder`)  

Example:
```
wav_folder
├───000561a49624c7c56625e6d8ccd230b15d3f129083b84c19846a9593.wav
├───0005680e7ac8826cff24f15022b67a2651acd691bf897bf3d3e44345.wav
├───000568340cb01e73daaa263d90765a5c213160a75201d642d899b4df.wav
├───00057062512f8dbc62d1691b97d0e6d997f350f41c908956fec02dbd.wav
├───00057091dd6ea751089e57358095034164067c180c4d1730254924ac.wav
├───000574e671847cbc40ef7fa325f39bfb6338a7f7781e09e773702b41.wav
...
```

### Output format

Each script will dump the transcriptions in the specified output folder in the following format:

Example:
```
output_txt_folder
├───000561a49624c7c56625e6d8ccd230b15d3f129083b84c19846a9593.txt
├───0005680e7ac8826cff24f15022b67a2651acd691bf897bf3d3e44345.txt
├───000568340cb01e73daaa263d90765a5c213160a75201d642d899b4df.txt
├───00057062512f8dbc62d1691b97d0e6d997f350f41c908956fec02dbd.txt
├───00057091dd6ea751089e57358095034164067c180c4d1730254924ac.txt
├───000574e671847cbc40ef7fa325f39bfb6338a7f7781e09e773702b41.txt
...
```

<hr/>

### Measuring quality

If you have ground truth in the same format as the output folder described above, you can calculate the `Word Error Rate` (WER)  as follows:

0. Prerequisite: `pip install jiwer==2.2.0`
1. Set the ground truth and prediction folders in the last line of `calc_wer.py`
2. Run `python calc_wer.py`

<hr/>

### DL Models

If say suppose you want to compare the online transcription output to the output of your deep learning models, it's easy!

**We follow the format of LibriSpeech dataset in this repo**.  
So ensure you dump the output in that format (same as this repo format) and use the `calc_wer.py` script to compare the quality.

For example purposes, we have supported the following DL models:
- [ESPnet](ESPNet-Model-Inference/)

Please feel free to contribute for other DL models that you are aware of.

Any pull requests or issues for bugs or fixes or new features are warmly welcomed. :-)

<hr/>

### Alternatives

You can also check the following Python Libraries for more services:

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
