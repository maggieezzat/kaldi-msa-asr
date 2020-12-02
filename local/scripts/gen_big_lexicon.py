import os

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

if not os.path.exists('data/local/dict_nosp'):
    os.makedirs('data/local/dict_nosp')


all_vocab = {}

with open('data/local/dict_nosp/lexicon.txt', 'w') as out:
    with open('data/local/dict_nosp/lexiconp.txt', 'w') as out_p:
        
        with open('local/data/dict_nosp/lexicon.txt', 'r') as f:
            for line in f:
                line = line.strip().split(" ", 1)
                word = line[0].strip()
                lex_ = line[1].strip()
                lex = lex_.replace(' ', '')
                if word == lex or word == '<UNK>':
                    if word not in all_vocab.keys():
                        out.write(word + "    " + lex_ + '\n')
                        out_p.write(word + "    1.0    " + lex_ + '\n')
                        all_vocab[word] = word
        
        with open('data/local/lm/lm_train__words_list.txt', 'r') as f:
            for line in f:
                if (line.strip() not in all_vocab):
                    lex = " ".join(line.strip())
                    out.write(line.strip() + "    " + lex + '\n')
                    out_p.write(line.strip() + "    1.0    " + lex + '\n')
                    all_vocab[line.strip()] = line.strip()
        
        with open('data/train/text', 'r') as f:
            for line in f:
                txt = line.strip().split(" ", 1)[1]
                words = txt.split()
                for word in words:
                    if word not in all_vocab.keys():
                        lex = " ".join(word)
                        out.write(word + "    " + lex + '\n')
                        out_p.write(word + "    1.0    " + lex + '\n')
                        all_vocab[word] = word

                        


