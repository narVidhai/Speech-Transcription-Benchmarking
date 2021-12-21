'''
Script to calculate Word Error Rate (WER)
'''

import jiwer
import sys, os
from os.path import basename, isfile
from glob import glob

punctuations = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
def replace_punctuations_by_space(text):
    for p in punctuations:
        text = text.replace(p, ' ')
    return text

def RemovePunctuation(replace_by_space=False):
    if not replace_by_space:
        return jiwer.RemovePunctuation()
    return replace_punctuations_by_space

transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    RemovePunctuation(replace_by_space=False),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.RemoveEmptyStrings(),
    jiwer.SentencesToListOfWords(),
    jiwer.RemoveWhiteSpace(replace_by_space=False),
    jiwer.RemoveEmptyStrings(),
])

def compute_avg_wer(ground_truth, hypothesis):
    
    assert len(ground_truth) == len(hypothesis)
    wer_sum = 0
    for gt, h in zip(ground_truth, hypothesis):
        wer_score = jiwer.wer(
            gt, 
            h, 
            truth_transform=transformation, 
            hypothesis_transform=transformation
        )
        wer_sum += wer_score

    avg_wer = wer_sum / len(hypothesis)

    return avg_wer

def libri_wer(gt_folder, pred_folder):
    gt_files = glob(os.path.join(gt_folder, '*.txt'))
    if not gt_files:
        sys.exit('No txt files in:', gt_folder)
    
    gt_lines = []
    pred_lines = []
    skipped = 0
    
    for gt_file in gt_files:
        pred_file = os.path.join(pred_folder, basename(gt_file))
        if not isfile(pred_file):
            print('ERROR: No prediction txt for:', gt_file)
            skipped += 1
            continue
        
        with open(gt_file, encoding='utf-8') as gf, open(pred_file, encoding='utf-8') as pf:
            # Assuming each txt will have only one line
            try:
                g_line = gf.readlines()[0].strip()
            except:
                print('GT File Empty:', gt_file)
                skipped += 1
                continue
            
            try:
                p_line = pf.readlines()[0].strip()
            except:
                print('Error in file:', pred_file)
                skipped += 1
                continue
            
            if g_line and p_line:
                gt_lines.append(g_line)
                pred_lines.append(p_line)
            else:
                print('Skipping:', basename(gt_file))
                skipped += 1
    
    wer = compute_avg_wer(gt_lines, pred_lines)
    print('WER: %.4f \t Folder: %s' % (wer, pred_folder))
    

if __name__ == '__main__':
    libri_wer('ground_truth_txt_folder', 'predicted_txt_folder')
