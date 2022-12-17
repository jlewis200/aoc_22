#!/usr/bin/python3

import numpy as np

from code import interact

rocks = [np.asarray([(0, 0), (1, 0), (2, 0), (3, 0)]),
         np.asarray([(0, 1), (1, 1), (2, 1), (1, 2), (1, 0)]),
         np.asarray([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
         np.asarray([(0, 0), (0, 1), (0, 2), (0, 3)]),
         np.asarray([(0, 0), (1, 0), (0, 1), (1, 1)])]


def solve(filename, height):

    with open(filename) as f_in:
        jets = list(f_in.readline().strip())
        jets = [(ord(char) - ord('='), 0) for char in jets]

        #set of (x, y) tuples indicating occupied indices
        occupied = set((idx, 0) for idx in range(1, 8))

        #rock positions (x, y, type)
        rock_positions = [(0, 0, -1)]
        maxs = [0]

        idx_jets = 0
        idx_rocks = 0
        rock_count = 0
        y_max = 0

        #floor at y=0

        while rock_count < height:
            rock = rocks[idx_rocks] + (3, y_max + 4) #initial offset
            rock_count += 1

            while True:
                #test wind movement
                jet = jets[idx_jets]
                idx_jets += 1
                idx_jets %= len(jets)

                rock_prime = rock + jet
                
                if not rock_contact(rock_prime, occupied):
                    rock = rock_prime

                #test vertical movement
                rock_prime = rock + (0, -1)
                
                if not rock_contact(rock_prime, occupied):
                    rock = rock_prime

                else:
                    for coord in rock:
                        occupied.add(tuple(coord))
                    
                    rock_positions.append(np.asarray(tuple(rock[0]) + (idx_rocks,)))

                    y_max = max(y_max, rock[:, 1].max())
                    break

            idx_rocks += 1
            idx_rocks %= 5

            print(f"{rock_count:10} {y_max} ") 
            maxs.append(y_max)
        
        print_rocks(occupied, y_max)
        print(y_max) 
        print()
        
        for idx in range(len(rock_positions) - 1, 0, -1):
            #print(rock_positions[idx])
            rock_positions[idx][:2] -= rock_positions[idx - 1][:2]


        print('#'*80)

        for idx in range(len(rock_positions) - 1, 0, -1):
            rock = rock_positions[idx]

            print(f"{idx:3}     {rock[0]:3} {rock[1]:3} {rock[2]:3}")
            
        for idx in range(len(jets), len(maxs) + 1, len(jets)):
            diff = maxs[idx] - maxs[idx - len(jets)]
            print(f"{idx:10} {diff} ") 
        interact(local=locals())

def print_rocks(occupied, y_max):
    for idx in range(y_max + 1, 0, -1):

        row = '|'

        for jdx in range(1, 8):
            if (jdx, idx) in occupied:
                row += '#'
            else:
                row += '.'

        row += '|'
        print(row)
    print("+-------+")




def rock_contact(rock_prime, occupied):
    #return true if any portion of the rock overlaps another rock or is out of range

    for coord in rock_prime:
        if (coord[0], coord[1]) in occupied or \
           coord[0] == 0 or coord[0] == 8   :
            return True

    return False


if __name__ == "__main__":
    #solve("test_input.txt", 2022)
    #solve("input.txt", 2022)
    solve("test_input.txt", 1000)
    
    #solve("test_input.txt", 1000000000000)
    #solve("input.txt", 2022)
