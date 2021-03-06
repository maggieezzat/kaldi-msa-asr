
from wave_manipulator import wave_manipulator as wm
import glob
import os
import sys

#############################################################################
#NOTE: THIS SCRIPT IS TO BE CALLED FROM THE ROOT OF THE REPO (KALDI-MSA-ASR)
#############################################################################


output_path = "waves/waves"

if not os.path.exists(output_path):
    os.makedirs(output_path)

input_path = "waves/all_waves/"
    
files = glob.glob(os.path.join(input_path, "*.wav"))


total = len(files)
i=0

for _file in files:
    i+=1
    print("File: " + str(i) + "/"+str(total), end='\r')
    try:
        dummy = wm(_file)
        dummy.add_silence_beginning_and_end(400, 400)
        dummy.export_file(os.path.join(output_path, os.path.basename(_file)))
    except:
        raise Exception("Bad file: " + _file)