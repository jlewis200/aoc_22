#!/usr/bin/python3

def find_distinct(sequence, length):
    for idx in range(length, 1 + len(line)):
        chunk = set(line[idx-length:idx])

        if len(chunk) == length:
            return idx
    
with open("input.txt") as f_in:
    for line in f_in:
        print(f"{find_distinct(line, 4)}  {find_distinct(line, 14)}")
    
