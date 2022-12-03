#!/usr/bin/python3

priorities = 0

with open("input.txt") as f_in:
    lines = [line.strip() for line in f_in]

    while len(lines) >= 3:
        r_1, r_2, r_3 = set(lines.pop()), set(lines.pop()), set(lines.pop())
        item = (r_1 & r_2 & r_3).pop()

        if item.islower():
            priorities += ord(item) - ord("a") + 1

        else:
            priorities += ord(item) - ord("A") + 27

print(priorities)


