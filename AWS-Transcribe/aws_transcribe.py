import sys, os, traceback
from os.path import basename, isfile
from time import sleep
import boto3
import requests, json
from glob import glob
from tqdm import tqdm
from uuid import uuid4

TRANSCRIBE_CLIENT = boto3.client('transcribe')
# AWS S3 Storage HTTPS URL to the folder where you have uploaded your wav files
S3_PREFIX_URI = 'https://speech-project.s3.region.amazonaws.com/wav_folder/'

def pretty_write_json(data, outfile, sort_keys=False):
    try:
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=sort_keys)
    except:
        print(traceback.format_exc())
        print('Failed to save JSON:', outfile)
    return

def schedule_jobs(audio_files):
    # Assumes files are already uploaded to AWS S3
    fid2jid = {}
    for audio_file in tqdm(audio_files, desc='Scheduling jobs'):
        file_id = basename(audio_file).replace('.wav', '')
        audio_uri = S3_PREFIX_URI + file_id + '.wav'
        job_name = uuid4().hex # Random ID
        TRANSCRIBE_CLIENT.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_uri},
            MediaFormat='wav',
            LanguageCode='en-IN'
        )
        fid2jid[file_id] = job_name
    return fid2jid

def bulk_transcribe(audio_files, output_folder):
    aws_output_folder = output_folder + '_aws_json'
    os.makedirs(aws_output_folder, exist_ok=True)
    fid2json = schedule_jobs(audio_files)
    success_count = 0
    attempts = 0
    sleep(20)
    while fid2json:
        attempts += 1
        print('Starting Attempt-%d...' % attempts)
        sleep(20)
        processed_fids = []
        for fid in tqdm(fid2json, desc='Retrieving transcripts'):
            status = TRANSCRIBE_CLIENT.get_transcription_job(TranscriptionJobName=fid2json[fid])
            # Check if success or failed or in-progress
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                # Get transcript result URL
                transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                try: # Get Transcript as JSON
                    output = requests.get(transcript_url).json()
                except:
                    print(traceback.format_exc())
                    continue
                # Assuming Libri-Speech like destination format
                raw_text = output['results']['transcripts'][0]['transcript']
                # Remove the transcribed job later by making a note of it
                processed_fids.append(fid)
                # Save the txt
                output_txt = os.path.join(output_folder, fid + '.txt')
                with open(output_txt, 'w', encoding='utf-8') as f:
                    f.write(raw_text)
                pretty_write_json(output, os.path.join(aws_output_folder, fid+'.json'))
                success_count += 1
            elif status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                print('Transcription failed for:', fid)
                processed_fids.append(fid)
            elif status['TranscriptionJob']['TranscriptionJobStatus'] == 'IN_PROGRESS':
                continue
            else:
                print(fid, status['TranscriptionJob']['TranscriptionJobStatus'])
        # Remove completed jobs from queue
        for fid in processed_fids:
            del fid2json[fid]
    print('Successfully transcribed %d / %d samples' % (success_count, len(audio_files)))
    return

def libri_transcribe(audio_folder, output_folder, samples_per_batch=100):
    os.makedirs(output_folder, exist_ok=True)
    audio_files = sorted(glob(os.path.join(audio_folder, '*.wav')))
    total_batches = (len(audio_files) + samples_per_batch-1) / samples_per_batch
    i = 0
    while i < len(audio_files):
        print('Transcribing batch %d/%d' % (i/samples_per_batch + 1, total_batches))
        bulk_transcribe(audio_files[i:i+samples_per_batch], output_folder)
        i += samples_per_batch
    return

if __name__ == '__main__':
    audio_folder, output_folder = sys.argv[1:3]
    libri_transcribe('wav_folder', 'output_folder')
