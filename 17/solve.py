#!/usr/bin/python3


import numpy as np


ROCKS = [np.asarray([(0, 0), (1, 0), (2, 0), (3, 0)]),
         np.asarray([(0, 1), (1, 1), (2, 1), (1, 2), (1, 0)]),
         np.asarray([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
         np.asarray([(0, 0), (0, 1), (0, 2), (0, 3)]),
         np.asarray([(0, 0), (1, 0), (0, 1), (1, 1)])]
 

def solve(filename, n_rocks):

    with open(filename) as f_in:
        jets = list(f_in.readline().strip())
        jets = [(ord(char) - ord('='), 0) for char in jets]

        #set of (x, y) tuples indicating occupied indices, initialize with floor
        occupied = set((idx, 0) for idx in range(1, 8))

        maxs = [0]

        idx_jets = 0
        idx_rocks = 0
        rock_count = 0
        y_max = 0

        while rock_count < n_rocks:
            rock = ROCKS[idx_rocks] + (3, y_max + 4) #initial offset
            rock_count += 1
            rock_prime = rock
            
            while not rock_contact(rock_prime, occupied):
                rock = rock_prime

                #test wind movement
                jet = jets[idx_jets]
                idx_jets += 1
                idx_jets %= len(jets)

                rock_prime = rock + jet
                
                if not rock_contact(rock_prime, occupied):
                    rock = rock_prime

                #test vertical movement
                rock_prime = rock + (0, -1)
            
            #add rock to occupied
            for coord in rock:
                occupied.add(tuple(coord))
            
            y_max = max(y_max, rock[:, 1].max())

            idx_rocks += 1
            idx_rocks %= 5

            maxs.append(y_max)
        
        #get the maxs/diffs per rock iteration
        maxs = np.asarray(maxs)
        diffs = get_diffs(maxs)      
        
        #get the indices of a diff repeating sequence
        idx_0, idx_1 = repeated_substring(diffs)
        seq = diffs[idx_0 : idx_1 + 1]
        
        n_rocks = 1000000000000
       
        #number of full sequences required to reach n_rocks
        n_full_sequences = (n_rocks - idx_0) // seq.shape[0]
        
        #number of elements of the partial sequence required to reach n_rocks
        len_partial_sequence = (n_rocks - idx_0) % seq.shape[0]

        #the target value is composed of the max height of the rock before the first sequence
        #plus the number of full sequences times the sum of diffs in the sequence
        #plus the sum of the length of the partial sequence which doesn't evenly divide n_rocks
        y_max = maxs[idx_0 - 1] + \
                (n_full_sequences * sum(seq)) + \
                sum(seq[:len_partial_sequence + 1])

        print(maxs[2022])
        print(y_max)
        print()


def get_diffs(maxs):
    """
    Get the max height difference from one iteration to the next.
    """

    diffs = np.zeros_like(maxs)
    
    for idx in range(1, len(maxs)):
        diffs[idx] = maxs[idx] - maxs[idx - 1]

    return diffs


def repeated_substring(diffs):
    """
    Get the start/end index of a cycle in the diffs.
    """

    #start with a short sequence on the end of the diffs
    for jdx in range(2, diffs.shape[0]):
        seq_indices = []

        #take the last jdx values from diff as the candidate sequence
        seq = diffs[-jdx:]

        #find the indices in diffs where the subsequence matches
        idx_0 = 0

        while idx_0 <= diffs.shape[0] - jdx:
            idx_1 = idx_0 + jdx
            
            if np.array_equal(diffs[idx_0 : idx_1], seq):
                #add subsequences to the list
                seq_indices.append((idx_0, idx_1))
                idx_0 = idx_1 + 1

            else:
                idx_0 += 1

        print(seq_indices)
   
        #if all of the sequences are adjacent, these are the maximal subsequence without repetition
        if all([seq_indices[idx - 1][1] == seq_indices[idx][0] - 1 for idx in range(1, len(seq_indices))]):
            break

    #return the first sequence (any of them will work)
    return seq_indices[0]


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
    solve("test_input.txt", 2022)
    solve("input.txt", 5000)
