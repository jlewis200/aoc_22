#!/usr/bin/python3

import re
from code import interact

o_cost = 0
c_cost = 0
b_cost = 0
g_cost = 0
o_max = 0
c_max = 0
b_max = 0
g_max = 0

def solve(filename):

    with open(filename) as f_in:
        blueprints = []
        
        for line in f_in:
            blueprints.append(list(map(int, re.findall(r"\d+", line))))


        #part 1
        qual_sum = 0

        for blueprint in blueprints:
            print(f"blueprint:  {blueprint}")
            qual_sum += blueprint[0] * max_geodes(blueprint, 24)

            print(f"qual_sum:  {qual_sum}")
        #interact(local=locals())

        #part 2
        qual_prod = 1
        
        for blueprint in blueprints[:3]:
            print(f"blueprint:  {blueprint}")
            qual_prod *= max_geodes(blueprint, 32)

            print(f"qual_prod:  {qual_prod}")
        #interact(local=locals())



def max_geodes(blueprint, steps):
    global o_cost, c_cost, b_cost, g_cost, o_max, c_max, b_max, g_max

    o_cost = blueprint[1]
    c_cost = blueprint[2]
    b_cost = blueprint[3:5]
    g_cost = blueprint[5:]
   
    o_max = 3 + max(o_cost, c_cost, b_cost[0], g_cost[0])
    c_max = 3 + b_cost[1]
    b_max = 3 + g_cost[1]

    o_bots = 1 
    c_bots = 0
    b_bots = 0
    g_bots = 0

    o = 0
    c = 0
    b = 0
    g = 0

    state_dict = {}

    return recurse(steps, state_dict, o, c, b, g, o_bots, c_bots, b_bots, g_bots)


def recurse(steps, state_dict, o, c, b, g, o_bots, c_bots, b_bots, g_bots):
    if steps <= 0:
        return g

    base = 10000

    state = (min(o, o_max) * base**0) + \
            (min(c, c_max) * base**1) + \
            (min(b, b_max) * base**2) + \
            (min(g, 21) * base**3) + \
            (o_bots * base**5) + \
            (c_bots * base**6) + \
            (b_bots * base**7) + \
            (g_bots * base**8) + \
            (steps * base**10)
    
    if state in state_dict:
        return state_dict[state]

    new_bots = []

    if o >= o_cost:
        new_bots.append((True, False, False, False))

    if o >= c_cost:
        new_bots.append((False, True, False, False))

    if o >= b_cost[0] and c >= b_cost[1]:
        new_bots.append((False, False, True, False))

    if o >= g_cost[0] and b >= g_cost[1]:
        new_bots.append((False, False, False, True))

    new_bots.append((False, False, False, False))

    g_max = 0

    for new_bot in new_bots:

        o_ =  o + o_bots - \
              (o_cost * new_bot[0]) - \
              (c_cost * new_bot[1]) - \
              (b_cost[0] * new_bot[2]) - \
              (g_cost[0] * new_bot[3])

        c_ = c + c_bots - (b_cost[1] * new_bot[2])
        b_ = b + b_bots - (g_cost[1] * new_bot[3])
        g_ = g + g_bots
        
        o_bots_ = o_bots + new_bot[0]
        c_bots_ = c_bots + new_bot[1]
        b_bots_ = b_bots + new_bot[2]
        g_bots_ = g_bots + new_bot[3]
        
        if o_ >= 0 and c_ >= 0 and b_ >= 0:
            g_max = max(g_max, 
                        recurse(steps - 1, state_dict, o_, c_, b_, g_, o_bots_, c_bots_, b_bots_, g_bots_))

    state_dict[state] = g_max

    return g_max


if __name__ == "__main__":
    solve("input.txt")
