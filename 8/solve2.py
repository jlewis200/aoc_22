#!/usr/bin/python3

import numpy as np

def get_score(array_slice, height):
    idx = 0

    for idx, element in enumerate(array_slice, start=1):
        if element >= height:
            break
    
    return idx


with open("input.txt") as f_in:
    array = np.asarray([list(line.strip()) for line in f_in], dtype=int)
    scores = np.zeros_like(array)

    for idx in range(array.shape[0]):
        for jdx in range(array.shape[1]):
            
            scores[idx, jdx] = get_score(array[idx, :jdx][::-1], array[idx, jdx]) * \
                               get_score(array[idx, jdx+1:], array[idx, jdx]) * \
                               get_score(array[:idx, jdx][::-1], array[idx, jdx]) * \
                               get_score(array[idx+1:, jdx], array[idx, jdx])

    print(scores.max())
