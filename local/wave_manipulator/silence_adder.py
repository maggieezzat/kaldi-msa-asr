
from wave_manipulator import wave_manipulator as wm
import glob
import os
import sys

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################


output_path = "waves/waves"

if not os.path.exists(output_path):
    os.makedirs(output_path)

datasets = ['train', 'dev', 'test']
files = []

for dataset in datasets:
    with open('data/'+dataset+'/wav.scp', 'r') as f:
        for line in f:
            f_name = line.strip().split()[0]
            files.append("waves/used_waves/" + f_name + '.wav')


for _file in files:
    try:
        dummy = wm(_file)
        dummy.add_silence_beginning_and_end(400, 400)
        dummy.export_file(os.path.join(output_path, os.path.basename(_file)))
    except:
        raise Exception("Bad file: " + _file)