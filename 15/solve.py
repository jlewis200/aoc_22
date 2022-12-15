#!/usr/bin/python3

import re
from code import interact


def solve(filename):
    with open(filename) as f_in:

        rows = {}

        for idx, line in enumerate(f_in, start=1):
            print(f"doing line:  {idx}")
            x_s, y_s, x_b, y_b = map(int, re.findall(r"-?\d+", line))

            #get the manhattan distance
            dist = abs(x_s - x_b) + abs(y_s - y_b)

            #get the top/bottom y index of the exclusion diamond
            y_top, y_bot = (y_s +  dist), (y_s - dist)
            
            #traverse the central vertical line of the diamond
            for y in range(y_bot, y_top + 1):
                
                #initialize row at y if it doesn't exist
                if y not in rows:
                    rows[y] = list()

                #get the x indices of the edges of the exclusion diamond
                h_dist = dist - abs(y_s - y)
                x_0, x_1 = (x_s - h_dist), (x_s + h_dist)
                
                #add the exclusion pair
                rows[y].append((x_0, x_1))

        for y in rows.keys():
            rows[y] = merge(rows[y])

        row_sum = 0

        for x_0, x_1 in rows[2000000]:
            if x_0 == x_1:
                row_sum += 1

            else:
                row_sum += x_1 - x_0

        print(row_sum)

        interact(local=locals())


def merge(intervals):
    merged = []
    start_len = len(intervals)

    while len(intervals) > 0:
        
        x_0, x_1 = intervals.pop(0)

        for idx in range(len(intervals) - 1, -1, -1):
            z_0, z_1 = intervals[idx]
            rng_0 = range(x_0, x_1 + 1)
            rng_1 = range(z_0, z_1 + 1)

            if x_0 in rng_1 or x_1 in rng_1 or z_0 in rng_0 or z_1 in rng_0: 
                x_0 = min(x_0, z_0)
                x_1 = max(x_1, z_1)
                intervals.pop(idx)

        merged.append((x_0, x_1))

    if len(merged) != start_len:
        merged = merge(merged)

    return merged
        

if __name__ == "__main__":
    solve("input.txt")
