#!/usr/bin/python3

import re

with open("input.txt") as f_in:
    overlap = 0
    
    for line in f_in:
        a, b, c, d = list(map(int, re.split(',|-', line.strip())))
        rng_0 = range(a, b + 1)
        rng_1 = range(c, d + 1)

        if a in rng_1 or b in rng_1 or c in rng_0 or d in rng_0: 
            overlap += 1

    print(overlap)
