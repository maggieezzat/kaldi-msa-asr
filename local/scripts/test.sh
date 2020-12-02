#!/usr/bin/env bash

min_lmwt=7
max_lmwt=17
array=( $(seq $min_lmwt $max_lmwt ) )
LMWT=$min_lmwt:$max_lmwt

for x in "${array[@]}"; do
    echo $x

done