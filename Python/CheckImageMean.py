import csv
import time, datetime
import sys, os
import threading
import cv2
import numpy as np
import queue
from dataclasses import dataclass
import argparse
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser("Input mkv file name.")
parser.add_argument('filename')
args = parser.parse_args()


vidcap = cv2.VideoCapture(args.filename)

# vidcap.set(cv2.CAP_PROP_POS_FRAMES, 2000)

success, image = vidcap.read()
count = 0

means = np.zeros(shape = (1,1))

amount_of_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

print(amount_of_frames)

while True:
    success, image = vidcap.read()
    
    if image is None:
        # print(len(means))
        break

    if amount_of_frames-10 == len(means):
        break

    img_mean = np.mean(image)
    print(img_mean)
    print('Read a new frame: ', success)
    means = np.append(means,img_mean)
    count += 1
print(count)
plt.hist(means, bins=255)
plt.show()
