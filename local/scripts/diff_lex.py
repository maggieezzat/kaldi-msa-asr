
with open('data/diff_lexicon.txt', 'w') as out:
    with open('data/ar_lexicon.txt', 'r') as f:
        for line in f:
            line = line.strip().split(" ", 1)
            word = line[0]
            lex_ = line[1]
            lex = lex_.replace(' ', '')
            if word != lex:
                out.write(word + "      " + lex_ + '\n')
