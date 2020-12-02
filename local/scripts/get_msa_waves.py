with open('data/wav_all.scp', 'r') as f:
    with open('data/wav_msa.scp', 'w') as out:
        for line in f:
            if "Waves/msa/waves/" in line:
                line = line.strip().split()
                id = line[0]
                name = line[1].split("/")[-1]
                out.write(id + " " + "waves/" + name + '\n')
