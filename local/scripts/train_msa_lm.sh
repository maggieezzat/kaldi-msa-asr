#!/usr/bin/env bash

lm_text="data/local/lm/msa_corpus_sample_ASMO.txt"
lm_vocab="data/local/lm/msa_corpus_words_list_ASMO.txt"
lm_test="data/local/lm/test_lm_ASMO_118k_words.txt"
lm_dir="data/local/lm/tri_gram"
srilm_dir="../../tools/srilm/bin/i686-m64"

#trigram language model with limiting bi-gram and tri-gram counts
$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $lm_dir/tri_lm.o3g.kn.gz -gt2min 3 -gt3min 2
echo "Perplexity for trigram LM:"
$srilm_dir/ngram -unk -lm $lm_dir/tri_lm.o3g.kn.gz -ppl $lm_test -debug 0 >& $lm_dir/tri_lm.ppl0
#file data/language_model/test_lm_ASMO_118k_words.txt: 7857 sentences, 118250 words, 577 OOVs
#0 zeroprobs, logprob= -273972.6 ppl= 152.2393 ppl1= 212.9382

#convert ARPA-format language models to FSTs.
#utils/format_lm.sh <lang_dir> <arpa-LM> <lexicon> <out_dir>
utils/format_lm.sh data/lang $lm_dir/tri_lm.o3g.kn.gz $dict_dir_nosp/lexicon.txt $lang_test_dir || exit 1;