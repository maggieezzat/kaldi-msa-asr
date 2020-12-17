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


def make_boxPlot(file_path):
    j = 0
    sizes = []
    with open(file_path, 'r') as f:
        for line in f:
            n = float(line.strip())
            if n<=20:
                sizes.append(n)
            else:
                j += 1

    print(j)

    plt.boxplot(np.array(sizes))
    plt.show()


if __name__ == "__main__":
    file_path = sys.argv[1]
    make_boxPlot(file_path)