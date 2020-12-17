import os
import random
import re
import numpy as np


#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################
MAX_DURATION=20

text = {}
all_waves = []
waves_dict = {}

with open('local/data/text_all', 'r') as f:
    for line in f:
        line = line.strip().split(" ", 1)
        if len(line) > 1:
            sent = line[1]
            sent = re.sub("SIL", "", sent)
            sent = re.sub(' +', ' ', sent) 
            text[line[0]] = sent.strip()

total_duration = 0

with open('local/data/wav_msa_durations.txt', 'r') as f:
    with open('local/data/long_utterances.txt', 'w') as out:
        for line_ in f:
                line = line_.strip().split()
                id = line[0]
                path = "waves/waves/"+line[1]
                name = line[1][:-4]
                dur = int(float(line[2]))
                if dur <= MAX_DURATION:
                    all_waves.append(id)
                    waves_dict[id] = (name, path)
                    total_duration+=dur
                else:
                    out.write(line_)

print(total_duration)
exit(0)

#check if arrays were saved, load them
#if not, create them
train_npy = 'local/data/train.npy'
test_npy = 'local/data/test.npy'
dev_npy = 'local/data/dev.npy'

print("Numpy arrays of dev, test and train exist. Loading them...")
# load arrays
train_waves = np.load('local/data/train.npy').tolist()
test_waves = np.load('local/data/test.npy').tolist()
dev_waves = np.load('local/data/dev.npy').tolist()

#dev + test
dev_test = test_waves + dev_waves

#remove dev and test sets from all_waves
train_waves_all = [wave for wave in all_waves if wave not in dev_test ]
np.save('local/data/train_all.npy', np.asarray(train_waves_all))

#write train_waves_all to train_all
train_dir = 'data/train_all'

if not os.path.exists(train_dir):
    os.makedirs(train_dir)

with open(train_dir+'/wav.scp', 'w') as wavscp:
    with open(train_dir+'/text', 'w') as text_out:
        with open(train_dir+'/utt2spk', 'w') as utt2spk:
            for wave_id in train_waves_all:
                name = waves_dict[wave_id][0]
                path = waves_dict[wave_id][1]
                wavscp.write(name + " " + path + '\n')
                text_out.write(name + " " + text[wave_id] + '\n')
                utt2spk.write(name + " " + name + '\n')


          