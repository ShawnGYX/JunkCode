from ast import arg
import cv2
import numpy as np
import time, datetime
import sys, os
import pygame
import argparse

parser = argparse.ArgumentParser(description="Save images with webcam")
parser.add_argument('--auto', action="store_true", help="Use this flag to automatically record frames")
args = parser.parse_args()

pygame.init()
pygame.display.set_mode((100,100))

now = datetime.datetime.now()
dt = now.strftime("%Y-%m-%d %H-%M-%S")
cam_cap_dir = "Cam_Capture_{}".format(dt)
os.mkdir(cam_cap_dir)

cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) #means manual
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 

exposure = 0.5 # Indoor initial value
gain = 1e-4

ret, frame = cap.read()

if args.auto:
    frame_count = 0
    print("Video recording is started.")
    while(True):
        ret, frame = cap.read()
        if not ret:
            print("Video frame did not return correctly!")
            continue
        
        frame_count += 1
        cv2.imshow('frame',frame)
        cv2.imwrite(cam_cap_dir+"/{}.jpg".format(frame_count),frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    break
        # Control camera exposure
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        img_mean = np.mean(frame)

        if img_mean > 128-32 and img_mean < 128+32:
            continue

        exposure += gain * (128 - img_mean) * exposure
        if exposure > 0.7:
            exposure = 0.7
        elif exposure <= 0.0:
            exposure = 1e-6

    cap.release()
    cv2.destroyAllWindows()
else:
    frame_count = 0
    print("Press X to save image, press Q to quit.")
    while(True):
        ret, frame = cap.read()
        if not ret:
            print("Video frame did not return correctly!")
            continue
        
        frame_count += 1
        cv2.imshow('frame',frame)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    cv2.imwrite(cam_cap_dir+"/{}.jpg".format(frame_count),frame)
                    print("Frame saved.")
                if event.key == pygame.K_q:
                    break
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Control camera exposure
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        img_mean = np.mean(frame)

        if img_mean > 128-32 and img_mean < 128+32:
            continue

        exposure += gain * (128 - img_mean) * exposure
        if exposure > 0.7:
            exposure = 0.7
        elif exposure <= 0.0:
            exposure = 1e-6

    cap.release()
    cv2.destroyAllWindows()