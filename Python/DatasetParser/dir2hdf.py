#!/usr/bin/env python3
import glob
import argparse
import os
import cv2
import csv
import h5py
import pandas as pd
import numpy as np




if __name__ == "__main__":
    parser = argparse.ArgumentParser("Convert an ArduPilot VIO dataset into a HDF5 file.")
    parser.add_argument("Directory", metavar='d', help="The directory containing the VIO dataset in traditional format.")
    args = parser.parse_args()

    PathName = args.Directory
    keys = PathName.split('/')
    DatasetName = keys[-1]
    
    print('Dataset will be extracted from folder: {}.'.format(PathName))
    print('It is being converted into {}.'.format(DatasetName+".hdf5"))

    img_dir_path = PathName + "/cam0"
    img_path = PathName + "/cam0/data"
    imu_path = PathName + "/imu0/data.csv"
    gt_path = PathName + "/groundtruth/data.csv"

    f = h5py.File(DatasetName+".hdf5", "w")
