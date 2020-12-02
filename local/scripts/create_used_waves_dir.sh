#!/usr/bin/env bash

train="../data/train/wav.scp"
test="../data/test/wav.scp"
dev="../data/dev/wav.scp"

mkdir ../used_waves

for x in $dev $test $train; do
    echo $x
    while read id path ;
    do
        path='../'$path
        rsync -aXS $path ../used_waves
    done < $x
done
