
words = []
with open('data/text_all', 'r') as f:
    for line in f:
        line = line.strip().split()
        text = line[1:]
        for word in text:
            words.append(word)

words = list(set(words))

lexicon_words = {}
with open('data/dict/lexicon.txt', 'r') as f:
    for line in f:
        word = line.strip().split()[0]
        lexicon_words[word] = word
        
print("Length of unique words in our transcripts: " + str(len(words)))
print("Length of the lexicon: " + str(len(lexicon_words)))

count=0
for word in words:
    if word not in lexicon_words.keys():
        count+=1

print("Count of words in our transcripts not present in lexicon: " + str(count))