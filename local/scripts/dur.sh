#!/usr/bin/env bash

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################

while read file_id file_name dur; do
  echo $dur >> local/data/dur.txt
done <local/data/wav_msa_durations.txt