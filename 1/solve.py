#!/usr/bin/python3

sums = [0]

with open("input.txt") as f_in:
    for line in f_in:
        try:
            sums[-1] += int(line)
       
        except ValueError:
            sums.append(0)
            
print(sorted(sums)[-1]) #largest
print(sum(sorted(sums)[-3:])) #sum of 3 largest
