## AWS Bulk Speech Transcribe - Python

### Steps

1. [Setup AWS command-line locally on your machine](https://docs.aws.amazon.com/transcribe/latest/dg/setup-asc-awscli.html).
2. Upload all your `wav` formatted wav files from your local `wav_folder` to AWS S3 Storage. ([Steps](https://aws.amazon.com/getting-started/hands-on/create-audio-transcript-transcribe/))
3. Ensure you have the HTTPS URL to the `wav_folder` of S3. Set it in the `S3_PREFIX_URI` variable of `aws_transcribe.py`
4. Set your local `wav_folder` and destination `output_folder` paths at the end of the same script.
5. To run bulk transcription: `python aws_transcribe.py`

### References
- [Python API reference](https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-python.html)
