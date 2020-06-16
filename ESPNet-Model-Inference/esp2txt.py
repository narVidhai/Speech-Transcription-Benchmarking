from glob import glob
from tqdm import tqdm
import os
from os.path import basename
import json

def convert_to_txt(decode_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    folders = sorted(glob(os.path.join(decode_folder, '*')))
    for folder in tqdm(folders):
        if not os.path.isdir(folder):
            continue
        result_file = os.path.join(folder, 'result.json')
        with open(result_file, encoding='utf-8') as f:
            data = json.load(f)
        transcript = data['utts'][list(data['utts'].keys())[0]]['output'][0]['rec_text']
        transcript = transcript.replace('<eos>', '').replace('▁', ' ').strip()
        output_file = os.path.join(output_folder, basename(folder)+'.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
    return

if __name__ == '__main__':
    convert_to_txt('decode', 'output-transformer-libri')
