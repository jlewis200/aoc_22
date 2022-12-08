#!/usr/bin/python3

import numpy as np

def get_score(array, idx, jdx):
    height = array[idx, jdx]
    score = 1
    
    row = idx - 1
    length = 0

    while row >= 0:
        length += 1

        if array[row, jdx] >= height:
            break
        
        row -= 1

    score *= length

    row = idx + 1
    length = 0

    while row < array.shape[0]:
        length += 1
 
        if array[row, jdx] >= height:
            break
        
        row += 1

    score *= length

    col = jdx - 1
    length = 0

    while col >= 0:
        length += 1

        if array[idx, col] >= height:
            break
 
        col -= 1

    score *= length

    col = jdx + 1
    length = 0

    while col < array.shape[1]:
        length += 1

        if array[idx, col] >= height:
            break

        col += 1

    score *= length

    return score

with open("input.txt") as f_in:
    array = np.asarray([list(line.strip()) for line in f_in], dtype=int)
    scores = np.zeros_like(array)

    for idx in range(array.shape[0]):
        for jdx in range(array.shape[1]):
            
            scores[idx, jdx] = get_score(array, idx, jdx) 

    print(scores.max())
