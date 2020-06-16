## ESPnet Model Bulk Speech Transcribe - Python

### Steps

1. Install ESPnet as instructed [here](https://espnet.github.io/espnet/installation.html).
2. From the espnet root directory, run `cd egs/librispeech/asr1 && . ./path.sh`
3. To run bulk inference: `python bulk_inference.py wav_folder` (Will dump JSONs in `decode` folder)
4. To get `txt` transcripts, set output folder in `esp2txt.py` and run `python esp2txt.py`

### Reference

- [ASR Demo](https://github.com/espnet/espnet#asr-demo)
