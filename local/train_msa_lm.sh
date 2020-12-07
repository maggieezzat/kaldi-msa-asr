#!/usr/bin/env bash

srilm_dir="../../tools/srilm/bin/i686-m64"

#####################################################################
#NOTE: big-lex, small-lex and big-lm, small-lm are there for development purposes and shall be removed in the end

#lm_text="data/local/lm/big-lm-data/lm_train__msa_plus_transcipts.txt"
#lm_vocab="data/local/lm/big-lm-data/lm_train__words_list.txt"
#lm_test="data/local/lm/big-lm-data/lm_test__msa_corpus_clean_ASMO.txt"
#tri_dir="data/local/lm/big-lm-trigram"

#lang_test_dir="data/lang_test_big_lex"
#dict_dir_nosp="data/local/dict_nosp_big_lex"


lm_text="data/local/lm/small-lm-data/2-5_lm_corpus_FULL.txt"
lm_vocab="data/local/lm/small-lm-data/2-5_lm_vocab_FULL.txt"
lm_test="data/local/lm/small-lm-data/test_lm_ASMO_118k_words.txt"
tri_dir="data/local/lm/small-lm-trigram"

lang_test_dir="data/lang_test"
dict_dir_nosp="data/local/dict_nosp"
#####################################################################



mkdir -p $tri_dir

################################################# Data Preparation ##################################################
#append train transcripts to lm train data and generate words list
python local/scripts/gen_lm_data.py

#sort unique the words list to avoid any duplicates
sort -u -o $lm_vocab $lm_vocab 
#####################################################################################################################


################################################### LM Training #####################################################
#trigram language model with limiting bi-gram and tri-gram counts
echo "$0: Training trigram language model"
$srilm_dir/ngram-count -text $lm_text -order 3 -limit-vocab -vocab $lm_vocab -unk -map-unk "<UNK>" -kndiscount -interpolate -lm $tri_dir/tri_lm.o3g.kn.gz -gt2min 3 -gt3min 2

#measure perplexity
echo "$0: Measuring perplexity for trigram language model"
$srilm_dir/ngram -unk -lm $tri_dir/tri_lm.o3g.kn.gz -ppl $lm_test -debug 0 >& $tri_dir/tri_lm.ppl0
#file data/language_model/test_lm_ASMO_118k_words.txt: 7857 sentences, 118250 words, 577 OOVs
#0 zeroprobs, logprob= -273972.6 ppl= 152.2393 ppl1= 212.9382


#convert ARPA-format language models to FSTs.
echo  "$0: Converting language model to G.fst"
utils/format_lm.sh data/lang $tri_dir/tri_lm.o3g.kn.gz $dict_dir_nosp/lexicon.txt $lang_test_dir || exit 1;
#####################################################################################################################