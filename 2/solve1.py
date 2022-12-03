#!/usr/bin/python3

                #rock   paper  sciss
score_matrix = [[1 + 3, 2 + 6, 3 + 0],
                [1 + 0, 2 + 3, 3 + 6],
                [1 + 6, 2 + 0, 3 + 3]]

score = 0

with open("input.txt") as f_in:
    for line in f_in:
        idx, jdx = list(map(ord, line.split()))
        score += score_matrix[idx - ord("A")][jdx - ord("X")]

print(score)
