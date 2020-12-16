import wave
import contextlib
import matplotlib.pyplot as plt
import sys
import glob
import os
import numpy as np

def get_duration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def make_boxPlot(dir_path):
    files = glob.glob(os.path.join(dir_path, "*.wav"))
    sizes = []
    for file in files:
        sizes.append(get_duration(file))
        print(get_duration(file))
    plt.boxplot(np.array(sizes))
    plt.show()


if __name__ == "__main__":
    dir_path = sys.argv[1]
    make_boxPlot(dir_path)