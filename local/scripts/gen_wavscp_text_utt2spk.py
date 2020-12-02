import os
import random
import re


text = {}
train_waves = []
waves_dict = {}

with open('local/data/text_all', 'r') as f:
    for line in f:
        line = line.strip().split(" ", 1)
        if len(line) > 1:
            sent = line[1]
            #if sent.strip().startswith('SIL'):
            #    sent = sent[3:]
            #if sent.strip().endswith('SIL'):
            #    sent = sent[:-3]
            sent = sent.replace('SIL','')
            sent = re.sub(' +', ' ', sent)
            text[line[0]] = sent.strip()


with open('local/data/wav_msa_durations.txt', 'r') as f:
    with open('local/data/long_utterances.txt', 'w') as out:
        for line_ in f:
                line = line_.strip().split()
                id = line[0]
                name = line[1].split("/")[-1][:-4]
                path = line[1]
                dur = int(float(line[2]))
                if dur <= 12:
                    train_waves.append(id)
                    waves_dict[id] = (name, path)
                else:
                    out.write(line_)
            
            

#choose random 5000 waves for dev and random 5000 for test
dev_waves = random.sample(train_waves, 5000)
train_waves = list(list(set(train_waves)-set(dev_waves)) + list(set(dev_waves)-set(train_waves)))

test_waves = random.sample(train_waves, 5000)
train_waves = list(list(set(train_waves)-set(test_waves)) + list(set(test_waves)-set(train_waves)))

train_dir = 'data/train'

if not os.path.exists(train_dir):
    os.makedirs(train_dir)

with open(train_dir+'/wav.scp_tmp', 'w') as wavscp:
    with open(train_dir+'/text_tmp', 'w') as text_out:
        with open(train_dir+'/utt2spk_tmp', 'w') as utt2spk:
            for wave_id in train_waves:
                name = waves_dict[wave_id][0]
                path = waves_dict[wave_id][1]
                wavscp.write(name + " " + path + '\n')
                text_out.write(name + " " + text[wave_id] + '\n')
                utt2spk.write(name + " " + name + '\n')

test_dir = 'data/test'

if not os.path.exists(test_dir):
    os.makedirs(test_dir)

with open(test_dir+'/wav.scp_tmp', 'w') as wavscp:
    with open(test_dir+'/text_tmp', 'w') as text_out:
        with open(test_dir+'/utt2spk_tmp', 'w') as utt2spk:
            for wave_id in test_waves:
                name = waves_dict[wave_id][0]
                path = waves_dict[wave_id][1]
                wavscp.write(name + " " + path + '\n')
                text_out.write(name + " " + text[wave_id] + '\n')
                utt2spk.write(name + " " + name + '\n')


dev_dir = 'data/dev'

if not os.path.exists(dev_dir):
    os.makedirs(dev_dir)

with open(dev_dir+'/wav.scp_tmp', 'w') as wavscp:
    with open(dev_dir+'/text_tmp', 'w') as text_out:
        with open(dev_dir+'/utt2spk_tmp', 'w') as utt2spk:
            for wave_id in dev_waves:
                name = waves_dict[wave_id][0]
                path = waves_dict[wave_id][1]
                wavscp.write(name + " " + path + '\n')
                text_out.write(name + " " + text[wave_id] + '\n')
                utt2spk.write(name + " " + name + '\n')
          