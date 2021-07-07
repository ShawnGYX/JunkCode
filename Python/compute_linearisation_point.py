#!/usr/bin/env python3
import pdb

import csv
import argparse
import itertools
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape

from pylie import SE3
from pylie import analysis


parser = argparse.ArgumentParser(description="Compute the best linearisation point based on previous result")
parser.add_argument("output", metavar='o', type=str, help="The output file of EQVIO.")
parser.add_argument("GIFT", metavar='g', type=str, help="The output file of GIFT.")

args = parser.parse_args()

fname_1 = args.output
fname_2 = args.GIFT

P_init = []

def is_in(line, id):
    fid = []
    for i in range(int(line[1])):
        fid.append(int(line[1+4*i+1]))
    if id in fid:
        n = fid.index(id)
        return True, n
    else:
        return False, 0
        


def fid_maximum(fname_1 : str):
    with open(fname_1, 'r') as file:
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


def fid_maximum_again(fname_2 : str):
    with open(fname_2, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        fid = []

        for line in reader:
            for i in range(int(line[1])):
                fid.append(int(line[1+4*i+1]))
        maxid = np.amax(fid)
    return maxid

# Read the csv file

maxid = fid_maximum(fname_1)
maxid_2 = fid_maximum_again(fname_2)
assert (maxid == maxid_2)
print("The maximum feature id is", maxid)
f_linearization = np.empty(shape=(maxid+1,4))



for i in range(maxid):
    mat_A = np.zeros(shape=(300,104))
    id = i + 1


    with open(fname_1, 'r') as t1, open(fname_2, 'r') as t2:
        f_output = csv.reader(t1)
        f_gift = csv.reader(t2)
        next(f_output)
        next(f_gift)
        
        
        n = 0
        
        for row1, row2 in itertools.zip_longest(f_output, f_gift):
            
            

            assert float(row1[0]) == float(row2[0])
            # print(row2[0])
            if float(row1[0])<0:
                continue

            if n > 99:
                break
            
            observed, f_num = is_in(row2, id)

            if observed:
                pose = SE3.from_list(row1[1:], format_spec="xw")

                mat_A[3*n:3*n+3,0:4] = pose.inv().as_matrix()[0:3,0:4]

                if n == 0 :
                    P_init = pose

                # y = np.ones(3)
                # y = np.array(float(row2[1+4*f_num+2: 1+4*f_num+5]))
                y = np.array([float(row2[1+4*f_num+2]),float(row2[1+4*f_num+3]), float(row2[1+4*f_num+4])])
                # y[3] = -1
                # pdb.set_trace()
                mat_A[3*n:3*n+3,4+n] = -np.transpose(y)

                # pdb.set_trace()

                n += 1

    if n<=100:
        mat_A = mat_A[0:3*n,0:4+n]
        

    U, d, Vh = np.linalg.svd(mat_A)
    V = np.transpose(Vh)
    last_col = [row[-1] for row in V]
    p_optimal = last_col[0:3]
    p_optimal.append(1)

    p_bff = P_init.inv().as_matrix()@np.transpose(p_optimal)
    f_linearization[i] = p_bff

    # pdb.set_trace()

    # print(P_init.as_matrix())
    print("The best estimate of feature No.{} is {}.".format(id, p_optimal))
    print("The bff coordinates in the initial scene is {}.".format(p_bff))

    # print(np.linalg.norm(p_optimal))


# Save the results into a new csv file
with open('optimal.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Feature ID", "x", "y", "z"])
    # writer.writerows(f_linearization)
    for i in range(maxid):
        writer.writerow([i+1, f_linearization[i][0], f_linearization[i][1], f_linearization[i][2]])
            

            
                    

            
    

