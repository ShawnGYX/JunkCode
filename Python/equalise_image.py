#!/usr/bin/env python3
import cv2
import os
import argparse
import progressbar

parser = argparse.ArgumentParser(description="Equalise the histogram(s) of given image(s).")
parser.add_argument('f',  type=str, help="The file or folder to convert.")
parser.add_argument('--folder', action='store_true', help="Used to indicate we are converting a folder. Default: False.")
parser.add_argument('--video', action='store_true', help="Used to indicate we are converting a video. Default: False.")
parser.add_argument('--extension', metavar='e',  type=str, default="png", help="The extension of the files to convert. Default: png.")
args = parser.parse_args()

fname = args.f
folder_flag = args.folder
# Check if file or folder
if not folder_flag and not args.video:
    img = cv2.imread(fname)
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_eq = cv2.equalizeHist(img)
    ext_pos = fname.rfind('.')
    out_str = fname[:ext_pos] + "_equalised" + fname[ext_pos:]
    cv2.imwrite(out_str, img_eq)
    exit(0)

# Check if video
if args.video:
    cap = cv2.VideoCapture(fname)
    ext_pos = fname.rfind('.')
    new_fname = fname[:ext_pos] + "_equalised" + fname[ext_pos:]

    ret, img = cap.read()
    writer = cv2.VideoWriter(new_fname, cv2.VideoWriter_fourcc(*"X264"), cap.get(cv2.CAP_PROP_FPS), (img.shape[1], img.shape[0]), False)

    while ret:
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_eq = cv2.equalizeHist(img)

        writer.write(img_eq)
        ret, img = cap.read()
    
    cap.release()
    writer.release()
    exit(0)
    


# If the program reaches here, we are dealing with a folder
if fname[-1] == "/":
    new_folder = fname[:-1]+"_equalised/"
else:
    new_folder = fname+"_equalised/"
if not os.path.exists(new_folder):
    os.mkdir(new_folder)

ext_str = args.extension
file_names = os.listdir(fname)
file_names = [f for f in file_names if f.endswith(ext_str)]
for img_name in progressbar.progressbar(file_names):
    img = cv2.imread(os.path.join(fname, img_name))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_eq = cv2.equalizeHist(img)
    cv2.imwrite(os.path.join(new_folder, img_name), img_eq)


