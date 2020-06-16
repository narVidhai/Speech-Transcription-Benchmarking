from rev_ai import apiclient, JobStatus

API_TOKEN = 'SET_ACCESS_TOKEN_HERE'
REV_CLIENT = apiclient.RevAiAPIClient(API_TOKEN)

from glob import glob
from tqdm import tqdm
from time import sleep
import sys, os
from os.path import basename, isfile

def schedule_jobs(audio_files):
    fid2jid = {}
    for audio_file in tqdm(audio_files, desc='Scheduling jobs'):
        file_id = basename(audio_file).replace('.wav', '')
        job = REV_CLIENT.submit_job_local_file(audio_file)
        if job.status == JobStatus.FAILED:
            print('Job Schedule failed for:', audio_file)
            continue
        fid2jid[file_id] = job.id
    return fid2jid

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

def bulk_transcribe(audio_files, output_folder):
    fid2json = schedule_jobs(audio_files)
    success_count = 0
    while fid2json:
        processed_fids = []
        for fid in tqdm(fid2json, desc='Retrieving transcripts'):
            job_details = REV_CLIENT.get_job_details(fid2json[fid])
            if job_details.status == JobStatus.IN_PROGRESS:
                continue
            elif job_details.status == JobStatus.FAILED:
                print('Transcription failed for:', fid)
                processed_fids.append(fid)
                continue
            elif job_details.status == JobStatus.TRANSCRIBED:
                transcript_text = REV_CLIENT.get_transcript_text(fid2json[fid])
                # Assuming Libri-Speech like destination format
                raw_text = ' '.join(row.split('    ')[2] for row in transcript_text.split('\n') if row)
                # Remove the transcribed job later by making a note of it
                processed_fids.append(fid)
                # Save the txt
                output_txt = os.path.join(output_folder, fid + '.txt')
                with open(output_txt, 'w', encoding='utf-8') as f:
                    f.write(raw_text)
                success_count += 1
        # Remove completed jobs from queue
        for fid in processed_fids:
            del fid2json[fid]
    print('Successfully transcribed %d / %d samples' % (success_count, len(audio_files)))
    return

if __name__ == '__main__':
    libri_transcribe('wav_folder', 'output_revai')
