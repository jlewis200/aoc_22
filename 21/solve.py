#!/usr/bin/python3

import re

from decimal import *
from code import interact

class Monkey(object):
    def __init__(self):
        self.op = None
        self.value = None
        self.adjacencies = list()

    def add(self, other):
        self.adjacencies.append(other)

    def get_value(self):
        #return if monkey is constant
        if self.value is not None:
            return self.value
        
        #if non-constant, perform op with subordinate monkey values
        return self.op(self.adjacencies[0].get_value(), self.adjacencies[1].get_value())


def get_monkeys(filename):
    with open(filename) as f_in:
        monkeys = {}
    
        #fancy lambda dictionary
        operations = {"+": lambda x, y: x + y,
                      "-": lambda x, y: x - y,
                      "*": lambda x, y: x * y,
                      "/": lambda x, y: x / y}

        for line in f_in:
            names = re.findall(r"[a-z]{4}", line)
            op = re.findall(r"[\+|\-|*|/]", line)
            value = re.findall(r"\d+", line)

            for name in names:
                if name not in monkeys:
                    monkeys[name] = Monkey()
                
            if len(op) == 1:
                monkeys[names[0]].op = operations[op[0]]
                monkeys[names[0]].add(monkeys[names[1]])
                monkeys[names[0]].add(monkeys[names[2]])

            elif len(value) == 1:
                #use high precision decimal to avoid accumulated floating point errors
                monkeys[names[0]].value = Decimal(value[0])

        return monkeys


def solve_1(monkeys):
    return monkeys["root"].get_value()


def solve_2(monkeys):
    #set the root op to return the two numbers
    monkeys["root"].op = lambda x, y: (x, y)

    #i am humn
    #the input appears to be a tree, so humn values only affect one side of the tree at the root level
    
    #composing linear functions results in a linear function:  f(x) = m * x + b
    monkeys["humn"].value = Decimal(0)
    f_0, _ = monkeys["root"].get_value()

    monkeys["humn"].value = Decimal(1)
    f_1, target = monkeys["root"].get_value()

    #find the slope when humn varies by 1:  m = f(1) - f(0)
    m = f_1 - f_0
    
    #find x such that f(x) = target
    #f(x) = target = m * x + b
    x = (target - f_0) / m 

    #set the humn value
    monkeys["humn"].value = x

    return x, monkeys["root"].get_value()


if __name__ == "__main__":
    #set a high decimal precision to avoid accumulated floating point errors
    getcontext().prec = 50

    monkeys = get_monkeys("test_input.txt")
    print(f"part 1:  {solve_1(monkeys)}")
    print(f"part 2:  {solve_2(monkeys)}")
    
    monkeys = get_monkeys("input.txt")
    print(f"part 1:  {solve_1(monkeys)}")
    print(f"part 2:  {solve_2(monkeys)}")
