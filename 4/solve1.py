#!/usr/bin/python3

import re

with open("input.txt") as f_in:
    fully_contained = 0
    
    for line in f_in:
        a, b, c, d = list(map(int, re.split(',|-', line.strip())))
        rng_0 = range(a, b + 1)
        rng_1 = range(c, d + 1)

        if (a in rng_1 and b in rng_1) or (c in rng_0 and d in rng_0):        
            fully_contained += 1
    
    print(fully_contained)
