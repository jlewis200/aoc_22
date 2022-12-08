#!/usr/bin/python3

import numpy as np

with open("input.txt") as f_in:
    array = np.asarray([list(line.strip()) for line in f_in], dtype=int)

    count = 0

    for idx in range(array.shape[0]):
        for jdx in range(array.shape[1]):
            
            row = array[idx, :]
            col = array[:, jdx]
            
            if row[:jdx+1].argmax() == jdx or \
               col[:idx+1].argmax() == idx or \
               row[jdx:][::-1].argmax() == row.shape[0] - jdx - 1 or \
               col[idx:][::-1].argmax() == col.shape[0] - idx - 1:
                count += 1


    print(count)
