#!/usr/bin/python3

priorities = 0

with open("input.txt") as f_in:
    for line in f_in:
        c_1, c_2 = set(line[:len(line)//2]), set(line[len(line)//2:])
        item = (c_1 & c_2).pop()

        if item.islower():
            priorities += ord(item) - ord("a") + 1

        else:
            priorities += ord(item) - ord("A") + 27

print(priorities)


