#!/usr/bin/python3

import re

class Data(object):
    coefficients = [256**idx for idx in range(10)]

    def __init__(self, blueprint):

        if isinstance(blueprint, list):
            #create a new data object and reset state_dict if initialized from a list
            self.o_cost = blueprint[1]
            self.c_cost = blueprint[2]
            self.b_cost = blueprint[3:5]
            self.g_cost = blueprint[5:]

            #i thought a +1 would work here, but it doesn't seem to
            self.o_max = 2 + max(self.o_cost, self.c_cost, self.b_cost[0], self.g_cost[0])
            self.c_max = 2 + self.b_cost[1]
            self.b_max = 2 + self.g_cost[1]

            self.o_bots = 1 
            self.c_bots = 0
            self.b_bots = 0
            self.g_bots = 0

            self.o = 0
            self.c = 0
            self.b = 0
            self.g = 0
        
            Data.state_dict = {}
            
        elif isinstance(blueprint, Data):
            #copy the data, don't reset state_dict if initialized from a Data object
            self.o_cost = blueprint.o_cost
            self.c_cost = blueprint.c_cost
            self.b_cost = blueprint.b_cost
            self.g_cost = blueprint.g_cost
            
            self.o_max = blueprint.o_max
            self.c_max = blueprint.c_max
            self.b_max = blueprint.b_max

            self.o_bots = blueprint.o_bots
            self.c_bots = blueprint.c_bots
            self.b_bots = blueprint.b_bots
            self.g_bots = blueprint.g_bots

            self.o = blueprint.o
            self.c = blueprint.c
            self.b = blueprint.b
            self.g = blueprint.g
    
    def hash(self, steps):
        #get the hash of the data, this will represent the state for memoization
        #the coefficients form a base-256 number system
        #if larger values are possible, the base should be increased to avoid collision

        state = (Data.coefficients[0] * min(self.o, self.o_max)) + \
                (Data.coefficients[1] * min(self.c, self.c_max)) + \
                (Data.coefficients[2] * min(self.b, self.b_max)) + \
                (Data.coefficients[3] * self.g) + \
                (Data.coefficients[4] * self.o_bots) + \
                (Data.coefficients[5] * self.c_bots) + \
                (Data.coefficients[6] * self.b_bots) + \
                (Data.coefficients[7] * self.g_bots) + \
                (Data.coefficients[8] * steps)

        return state


def solve(filename):
    with open(filename) as f_in:
        blueprints = []
        
        for line in f_in:
            blueprints.append(list(map(int, re.findall(r"\d+", line))))

        #part 1
        print("#"*80)
        print("part 1")
        
        qual_sum = 0

        #find sum of max geodes multiplied by blueprint number
        for blueprint in blueprints:
            print(f"blueprint:  {blueprint}")
            qual_sum += blueprint[0] * max_geodes(24, Data(blueprint))
            print(f"qual_sum:  {qual_sum}")
        
        print()
        
        #part 2
        print("#"*80)
        print("part 2")
        
        qual_prod = 1
       
        #find product of max geodes for 1st 3 blueprints
        for blueprint in blueprints[:3]:
            print(f"blueprint:  {blueprint}")
            qual_prod *= max_geodes(32, Data(blueprint))
            print(f"qual_prod:  {qual_prod}")
        
        print()


def max_geodes(steps, data):
    #base case, return g if no steps remain
    if steps <= 0:
        return data.g

    #get the state
    state = data.hash(steps)

    #return the max geodes if this state has been encountered before
    if state in Data.state_dict:
        return Data.state_dict[state]

    #accumulate possible paths to take at this point
    new_bots = []

    if data.o >= data.o_cost:
        new_bots.append((True, False, False, False))

    if data.o >= data.c_cost:
        new_bots.append((False, True, False, False))

    if data.o >= data.b_cost[0] and data.c >= data.b_cost[1]:
        new_bots.append((False, False, True, False))

    if data.o >= data.g_cost[0] and data.b >= data.g_cost[1]:
        new_bots.append((False, False, False, True))

    #doing nothing is always an option
    new_bots.append((False, False, False, False))

    g_max = 0

    #for each configuration of new bots 
    for new_bot in new_bots:
        #copy the data
        data_copy = Data(data)

        #find new minearl counts at this step
        data_copy.o += data.o_bots - \
                      (data.o_cost * new_bot[0]) - \
                      (data.c_cost * new_bot[1]) - \
                      (data.b_cost[0] * new_bot[2]) - \
                      (data.g_cost[0] * new_bot[3])

        data_copy.c += data.c_bots - (data.b_cost[1] * new_bot[2])
        data_copy.b += data.b_bots - (data.g_cost[1] * new_bot[3])
        data_copy.g += data.g_bots
        
        #find new bot counts at this step
        data_copy.o_bots += new_bot[0]
        data_copy.c_bots += new_bot[1]
        data_copy.b_bots += new_bot[2]
        data_copy.g_bots += new_bot[3]
        
        #retain the maximum geode value
        g_max = max(g_max, max_geodes(steps - 1, data_copy))

    #memoize the max for the current state
    Data.state_dict[state] = g_max

    return g_max


if __name__ == "__main__":
    solve("input.txt")
