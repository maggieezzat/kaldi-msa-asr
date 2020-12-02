all_vocab = {}

with open('../data/local/dict/lexicon.txt', 'w') as out:
    with open('../data/local/dict/lexiconp.txt', 'w') as out_p:
        with open('data/dict/lexicon.txt', 'r') as f:
            out.write("SIL    SIL" + '\n')
            out_p.write("SIL    1.0    SIL" + '\n')
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
        
        with open('../data/language_model/lm_corpus_VOCAB.txt', 'r') as f:
            for line in f:
                if "<" in line:
                    print(line)
                else:
                    if (line.strip() not in all_vocab):
                        lex = " ".join(line.strip())
                        out.write(line.strip() + "    " + lex + '\n')
                        out_p.write(line.strip() + "    1.0    " + lex + '\n')
                        all_vocab[line.strip()] = line.strip()
                        


