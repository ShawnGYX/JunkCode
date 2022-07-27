import cv2
import numpy as np
import time, datetime
import sys, os


now = datetime.datetime.now()
dt = now.strftime("%Y-%m-%d %H-%M-%S")
cam_cap_dir = "Cam_Capture_{}".format(dt)
os.mkdir(cam_cap_dir)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) #means manual


exposure = 0.5 # Indoor initial value
gain = 1e-4
# Control camera exposure
cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

ret, frame = cap.read()

frame_count = 0
print("Video recording is started.")
while(True):
    ret, frame = cap.read()
    if not ret:
        print("Video frame did not return correctly!")
        continue
    
    frame_count += 1
    # cv2.imshow('frame',frame)
    cv2.imwrite(cam_cap_dir+"/{}.jpg".format(frame_count),frame)

    # img_mean = np.mean(frame)

    # if img_mean > 128-32 and img_mean < 128+32:
    #     continue

    # exposure += gain * (128 - img_mean) * exposure
    # if exposure > 0.7:
    #     exposure = 0.7
    # elif exposure <= 0.0:
    #     exposure = 1e-6
