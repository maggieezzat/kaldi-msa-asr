#!/usr/bin/env bash

CUDA_VISIBLE_DEVICES=0,1 local/nnet3/run_tdnn.sh --stage 10
