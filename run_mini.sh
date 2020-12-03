#!/usr/bin/env bash

stage=0

cmd="run.pl"
nj=$(grep -c ^processor /proc/cpuinfo)

train_dir="data/train"
train_dir_half="data/train_half"
train_dir_30k="data/train_30k"
test_dir="data/test"
dev_dir="data/dev"

lang_dir="data/lang"
lang_test_dir="data/lang_test"
dict_dir_nosp="data/local/dict_nosp"
dict_dir="data/local/dict"

##TODO: SET LM DIR
lm_dir="data/local/lm/trigram"


. ./path.sh

if [ $stage -le 7 ]; then
    utils/format_lm.sh data/lang $lm_dir/tri_lm.o3g.kn.gz $dict_dir/lexicon.txt $lang_test_dir
fi

if [ $stage -le 10 ]; then
    #decoding
    utils/mkgraph.sh $lang_test_dir exp/tri6 exp/tri6/graph || exit 1;
    steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri6/graph $dev_dir exp/tri6/decode_dev
    steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri6/graph $test_dir exp/tri6/decode_test
fi

if [ $stage -le 11 ]; then
    echo "$0: Starting nnet training"
    nvidia-smi -c 3
    state=$(nvidia-smi  --query | grep 'Compute Mode')
    state=($state)
    state=${state[3]}
    if [ ! "$state" == "Exclusive_Process" ]; then
      echo "Please run the script using sudo in order to set the compute mode"
      exit 1
    else
      echo "Successfully set compute mode to Exclusive_Process"
    fi
    CUDA_VISIBLE_DEVICES=0,1 local/nnet3/run_tdnn.sh --stage 9
fi