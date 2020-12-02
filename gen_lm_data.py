
#append train transcripts to lm train
with open('../../data/train/text', 'r') as train_text:
    with open('../../data/local/lm/lm_train__msa_corpus_clean_ASMO.txt', 'r') as lm_train:
        with open('../../data/local/lm/lm_train__msa_plus_transcipts.txt', 'w') as out:
            for line in train_text:
                txt = line.split(" ", 1)[1].strip()
                txt = txt.replace("SIL", '')
                out.write(txt + '\n')
            for line in lm_train:
                out.write(line)




'''
#generate words list
words_dict = {}
with open('../../data/local/lm/lm_train__msa_corpus_clean_ASMO.txt', 'r') as lm_train:
    with open('../../data/local/lm/words_list.txt', 'w') as words_list:
        for line in lm_train:
            words = line.strip().split()
            for word in words:
                words_dict[word] = word
        
        for word in words_dict:

'''