#!/usr/bin/env python3
import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape

from pylie import SE3
from pylie import analysis


parser = argparse.ArgumentParser(description="Plot the feature depth (z) convergence")
parser.add_argument("output", metavar='o', type=str, help="The output file of EQVIO.")

args = parser.parse_args()

fname = args.output

def fid_maximum(fname : str):
    with open(fname, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        fid=[]
        for line in reader:
            t = float(line[0])
            if t < 0:
                continue

            for i in range(int(line[11])):
                fid.append(int(line[11+4*i+1]))
        maxid = np.amax(fid)
    return maxid


# Read the csv file

maxid = fid_maximum(fname)
print("The maximum feature id is", maxid)
fz = np.empty(shape=(maxid+1,1))


with open(fname, 'r') as file:
    reader = csv.reader(file)
    # SKip header
    next(reader)
    for line in reader:
        t = float(line[0])
        if t<0:
            continue

        pose = SE3.from_list(line[1:], format_spec="xw")

        for i in range(int(line[11])):
            p = np.ones(4)
            p[0:3] = np.array(line[11+4*i+2:11+4*i+5])
            p_bff = pose.inv().as_matrix() * np.transpose(p)
            np.append(fz[int(line[11+4*i+1])], p_bff[2,3])

    print("Finish recording all the feature depth.")    

    

