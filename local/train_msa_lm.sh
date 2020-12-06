#!/usr/bin/env bash

stage=0

lm_text="data/local/lm/lm_train__msa_plus_transcipts.txt"
lm_vocab="data/local/lm/lm_train__words_list.txt"
lm_test="data/local/lm/lm_test__msa_corpus_clean_ASMO.txt"
lm_dir="data/local/lm/trigram"
srilm_dir="../../tools/srilm/bin/i686-m64"


################################################# Data Preparation ##################################################
#append train transcripts to lm train data and generate words list
python local/scripts/gen_lm_data.py

#sort unique the words list to avoid any duplicates
sort -u -o $lm_vocab $lm_vocab 
#####################################################################################################################


################################################### LM Training #####################################################
#trigram language model with limiting bi-gram and tri-gram counts
#echo "$0: Training trigram language model"
$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $lm_dir/tri_lm.o3g.kn.gz -gt2min 3 -gt3min 2

#measure perplexity
#echo "$0: Perplexity for trigram language model"
$srilm_dir/ngram -unk -lm $lm_dir/tri_lm.o3g.kn.gz -ppl $lm_test -debug 0 >& $lm_dir/tri_lm.ppl0
#file data/language_model/test_lm_ASMO_118k_words.txt: 7857 sentences, 118250 words, 577 OOVs
#0 zeroprobs, logprob= -273972.6 ppl= 152.2393 ppl1= 212.9382

#convert ARPA-format language models to FSTs.
#echo  "$0: Converting language model to G.fst"
#utils/format_lm.sh data/lang $lm_dir/tri_lm.o3g.kn.gz $dict_dir_nosp/lexicon.txt $lang_test_dir || exit 1;
#####################################################################################################################