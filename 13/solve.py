#!/usr/bin/python3


from functools import cmp_to_key


def compare(p_0, p_1):
    #return negative:  p_0 <  p_1
    #return 0:         p_0 == p_1
    #return positive:  p_0 > p_1

    if isinstance(p_0, int) and isinstance(p_1, int):
        #both ints
        return p_0 - p_1
    
    elif isinstance(p_0, int):
        #p_0 is int, p_1 is list, upgrade p_0 to list
        return compare([p_0], p_1)
    
    elif isinstance(p_1, int):
        #p_1 is int, p_0 is list, upgrade p_1 to list
        return compare(p_0, [p_1])
 
    else:
        #both lists
        for i_0, i_1 in zip(p_0, p_1):
            res = compare(i_0, i_1)

            if res != 0:
                return res

        #exhausted lists
        return len(p_0) - len(p_1)


with open("input.txt", "rb") as f_in:
    packets = []
    
    for line in f_in:
        line = line.strip()

        if len(line) == 0:
            continue

        packets.append(eval(line))

    #part 1
    index_sum = 0

    for idx in range(0, len(packets), 2):
        p_0, p_1 = packets[idx], packets[idx+1]

        if compare(p_0, p_1) < 0:
            index_sum += idx//2 + 1

    print(index_sum)

    #part 2
    div_0 = [[2]]
    div_1 = [[6]]
    packets += [div_0, div_1]

    packets = sorted(packets, key=cmp_to_key(compare))
    key = (packets.index(div_0) + 1) * (packets.index(div_1) + 1)
    print(key)

