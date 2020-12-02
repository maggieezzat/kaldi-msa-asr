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

decode=false

. ./path.sh

####################################### Data Preparation & Feature Extraction #######################################
if [ $stage -le 0 ]; then
    echo "Creating necessary files and extracting features"

    #create wav.scp, text and utt2spk file for each of the train, dev and test set
    python gen_wavscp_text_utt2spk.py

    #create lexicon file from lm vocab + standard lexicon file (provided by Dr. Sherif)
    python local/gen_big_lexicon.py


    for x in $train_dir $test_dir $dev_dir; do
        #sort the files
        sort -u $x/wav.scp_tmp > $x/wav.scp
        rm $x/wav.scp_tmp
        sort -u $x/text_tmp > $x/text
        rm $x/text_tmp
        sort -u $x/utt2spk_tmp > $x/utt2spk
        rm $x/utt2spk_tmp

        #make spk2utt file
        utils/utt2spk_to_spk2utt.pl $x/utt2spk > $x/spk2utt

        #fix data directory
        utils/fix_data_dir.sh $x

        #make Mel Frequency features
        log_dir="$x/log"
        mfcc_dir="$x/mfcc"
        vad_dir="$x/vad"
        segments_dir="$x/segments"
        cmvn_dir="$x/cmvn"
        steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj $nj --cmd "$cmd" --write-utt2num-frames true $x $log_dir $mfcc_dir || exit 1;

        #fix data directory
        utils/fix_data_dir.sh $x 

        #compute cepstral mean and variance statistics per speaker.
        steps/compute_cmvn_stats.sh $x $log_dir $cmvn_dir || exit 1;

        #fix data directory
        utils/fix_data_dir.sh $x
    done

    #create files for data/lang
    utils/prepare_lang.sh $dict_dir_nosp "<UNK>" data/local/lang $lang_dir || exit 1;
    #create files for data/lang_test
    utils/prepare_lang.sh $dict_dir_nosp "<UNK>" data/local/lang $lang_test_dir || exit 1;
fi
#####################################################################################################################



############################################# Language Model Training ###############################################
if [ $stage -le 1 ]; then
    utils/train_msa_lm.sh
fi
#####################################################################################################################



################################################ Monophone Training #################################################
if [ $stage -le 2 ]; then
    echo "Splitting data and training monophone"
    # take subset of data (30k) for monophone training
    utils/subset_data_dir.sh --shortest $train_dir 30000 $train_dir_30k || exit 1;

    # take subset of data ( about half) for monophone alignment and first triphone training
    utils/subset_data_dir.sh --first $train_dir 40000 $train_dir_half || exit 1;

    # monophone training
    steps/train_mono.sh --nj $nj --cmd "$cmd" $train_dir_30k $lang_dir exp/mono || exit 1;
fi
#####################################################################################################################



############################################# First Triphone Training ###############################################
if [ $stage -le 3 ]; then
    echo "First triphone training"

    #aligning data in data/train_half using model from exp/mono, putting alignments in exp/mono_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" $train_dir_half $lang_dir exp/mono exp/mono_ali || exit 1;

    #train with delta features
    steps/train_deltas.sh --cmd "$cmd" 2000 10000 $train_dir_half $lang_dir exp/mono_ali exp/tri1 || exit 1;
fi
#####################################################################################################################



############################################# Second Triphone Training ##############################################
if [ $stage -le 4 ]; then
    echo "Second triphone training"

    #aligning data in data/train using model from exp/tri1, putting alignments in exp/tri1_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri1 exp/tri1_ali || exit 1;

    #train with delta features
    steps/train_deltas.sh --cmd "$cmd" 2500 15000 $train_dir $lang_dir exp/tri1_ali exp/tri2 || exit 1;
fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 5 ]; then
    echo "Third triphone training"

    #aligning data in data/train using model from exp/tri2, putting alignments in exp/tri2_ali
    steps/align_si.sh --nj $nj --cmd "$cmd" --use-graphs true $train_dir $lang_dir exp/tri2 exp/tri2_ali  || exit 1;

    #train LDA-MLLT triphones
    steps/train_lda_mllt.sh --cmd "$cmd" 3500 20000 $train_dir $lang_dir exp/tri2_ali exp/tri3 || exit 1;

    #Pronunciation & Silence Probabilities
    #now we compute the pronunciation and silence probabilities from training data and re-create the lang directory.
    steps/get_prons.sh --cmd "$cmd" $train_dir $lang_dir exp/tri3 || exit 1;
  
    utils/dict_dir_add_pronprobs.sh --max-normalize true $dict_dir_nosp exp/tri3/pron_counts_nowb.txt exp/tri3/sil_counts_nowb.txt exp/tri3/pron_bigram_counts_nowb.txt $dict_dir || exit 1;

    utils/prepare_lang.sh $dict_dir "<UNK>" data/local/lang $lang_dir || exit 1;
    utils/prepare_lang.sh $dict_dir "<UNK>" data/local/lang $lang_test_dir || exit 1;

    utils/format_lm.sh data/lang $lm_dir/tri_lm.o3g.kn.gz $dict_dir/lexicon.txt $lang_test_dir || exit 1;
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 6 ]; then
    echo "Fourth triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri3 exp/tri3_ali || exit 1;

    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 4200 40000 $train_dir $lang_dir exp/tri3_ali exp/tri4
    
    #decoding
    if $decode; then
        utils/mkgraph.sh $lang_test_dir exp/tri4 exp/tri4/graph
        steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri4/graph $dev_dir exp/tri4/decode_dev
    fi
fi
#####################################################################################################################



############################################ LDA-MLLT Triphones Training ############################################
if [ $stage -le 7 ]; then
    echo "Fifth triphone training"

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri4 exp/tri4_ali

    #train second pass of LDA-MLLT
    steps/train_lda_mllt.sh --cmd "$cmd" 5500 70000 $train_dir $lang_dir exp/tri4_ali exp/tri5
fi
#####################################################################################################################



############################################### SAT Triphones Training ##############################################
if [ $stage -le 8 ]; then
    echo "Sixth triphone training"

    #Align LDA-MLLT triphones with FMLLR
    steps/align_fmllr.sh --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri5 exp/tri5_ali
    
    #Train SAT triphones
    steps/train_sat_basis.sh --cmd "$cmd" 7000 100000 $train_dir $lang_dir exp/tri5_ali exp/tri6

    #Align SAT triphones with FMLLR
    steps/align_basis_fmllr.sh  --nj $nj --cmd "$cmd" $train_dir $lang_dir exp/tri6 exp/tri6_ali
    
    #decoding
    if $decode; then
        utils/mkgraph.sh $lang_test_dir exp/tri6 exp/tri6/graph || exit 1;
        steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri6/graph $dev_dir exp/tri6/decode_dev
        steps/decode_basis_fmllr.sh --nj $nj --cmd "$cmd" exp/tri6/graph $test_dir exp/tri6/decode_test
    fi
fi
#####################################################################################################################



#################################################### NNET Training ###################################################
if [ $stage -le 9 ]; then
    echo "nnet training"
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
    CUDA_VISIBLE_DEVICES=0,1 local/nnet3/run_tdnn.sh --stage 13
fi
#####################################################################################################################