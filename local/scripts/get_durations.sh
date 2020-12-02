#!/usr/bin/env bash

while read file_id file_path; do
  f="/home/maggie/kaldi/egs/msa_asr/$file_path"
  dur=$(sox $f -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p')
  echo $file_id $file_path $dur >> wav_msa_durations.txt
done </home/maggie/kaldi/egs/msa_asr/local/data/wav_msa.scp