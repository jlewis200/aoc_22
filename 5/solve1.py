#!/usr/bin/python3

import re

with open("input.txt") as f_in:
    line = f_in.readline()
    n_stacks = len(line) // 4
    stacks = [[] for _ in range((1 + n_stacks))]

    while '[' in line:
        jdx = 1

        for idx in range(1, len(line), 4):
            if line[idx] != ' ':
                stacks[jdx].insert(0, line[idx])

            jdx += 1

        line = f_in.readline()

    f_in.readline()

    for line in f_in:
        n, src, dst = list(map(int, re.findall(r"\d+", line)))
        
        for _ in range(n):
            stacks[dst].append(stacks[src].pop())

    for stack in stacks[1:]:
        print(stack[-1], end='')

    print()


