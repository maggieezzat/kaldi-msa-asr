#!/usr/bin/env bash

mkdir missing_waves

while read fname ch1 ch2 ;
    do
        path='waves/'$fname
        echo $path
        rsync -aXS $path missing_waves
    done < diff.txt