train_dur = 0
test_dur = 0
dev_dur = 0

durations = {}

with open('data/wav_msa_durations.txt', 'r') as f:
    for line in f:
        line = line.strip().split()
        id = line[1][6:]
        id = id[:-4]
        dur = float(line[2])
        durations[id] = dur

with open('../data/train/wav.scp', 'r') as f:
    for line in f:
        line = line.strip().split()
        id = line[0]
        train_dur += durations[id]

with open('../data/test/wav.scp', 'r') as f:
    for line in f:
        line = line.strip().split()
        id = line[0]
        test_dur += durations[id]

with open('../data/dev/wav.scp', 'r') as f:
    for line in f:
        line = line.strip().split()
        id = line[0]
        dev_dur += durations[id]

train_dur = train_dur / 3600
print("Total train duration: {:.2f} hours".format(train_dur))

dev_dur = dev_dur / 3600
print("Total dev duration: {:.2f} hours".format(dev_dur))

test_dur = test_dur / 3600
print("Total test duration: {:.2f} hours".format(test_dur))
