#!/usr/bin/python3

import re


def solve(filename, target_row, search_max):
    with open(filename) as f_in:

        rows = {}
        beacons = {}

        for idx, line in enumerate(f_in, start=1):
            print(f"doing line:  {idx}")
            x_s, y_s, x_b, y_b = map(int, re.findall(r"-?\d+", line))

            #add the beacons to the set of beacons per row dict
            if y_b not in beacons:
                beacons[y_b] = set()

            beacons[y_b].add(x_b)

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

        #merge overlapping/adjacent intervals
        for y in rows.keys():
            rows[y] = merge(rows[y])

        #part 1
        row_sum = 0

        #sum the exclusion intervals
        for x_0, x_1 in rows[target_row]:
            row_sum += (x_1 - x_0) + 1

        #subtract the number of beacons in the row
        row_sum -= len(beacons[target_row])
        print(row_sum)

        #part 2
        #for each row
        for idx in range(0, search_max + 1):
            #sort ranges in increasing order
            ranges = sorted(rows[idx], key=lambda x: x[0])
            jdx = 0

            #try the columns
            while jdx <= search_max and len(ranges) > 0:

                rng = ranges.pop(0)

                if jdx >= rng[0] and jdx <= rng[1]:
                    jdx = rng[1] + 1

                else:
                    print((jdx * 4000000) + idx)
                    break


def merge(intervals):
    merged = []
    start_len = len(intervals)

    while len(intervals) > 0:
        x_0, x_1 = intervals.pop(0)

        for idx in range(len(intervals) - 1, -1, -1):
            z_0, z_1 = intervals[idx]
            rng_0 = range(x_0, x_1 + 1)
            rng_1 = range(z_0, z_1 + 1)

            #merge overlapping or adjacent
            if (x_0 in rng_1 or x_1 in rng_1 or z_0 in rng_0 or z_1 in rng_0) or \
               (z_0 - x_1 == 1 or x_0 - z_1 == 1):
                x_0 = min(x_0, z_0)
                x_1 = max(x_1, z_1)
                intervals.pop(idx)

        merged.append((x_0, x_1))

    #merge again if anything was merged
    if len(merged) != start_len:
        merged = merge(merged)

    return merged


if __name__ == "__main__":
    solve("test_input.txt", 10, 20)
    solve("input.txt", 2000000, 4000000)
