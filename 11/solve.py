#!/usr/bin/python3


class Monkey(object):
    @classmethod
    def initialize(cls):
        cls.monkeys = []
        cls.factors = 1

    @classmethod
    def do_round(cls):
        for monkey in Monkey.monkeys:
            #update the monkeys in order
            monkey.update()

    def __init__(self, items=None, f_update=None, f_test=None, div=True):
        self.items = items 
        self.f_update = f_update
        self.f_test = f_test
        self.div = div
        self.inspections = 0

        Monkey.monkeys.append(self)    
    
    def update(self):
        while len(self.items) > 0:
            self.inspections += 1
            
            item = self.items.pop(0)
            item = self.f_update(item)

            if self.div:
                #integer divide by 3 for part 1
                item //= 3

            #(addition/multiplicaiton mod product of all divisor) mod a single divisor ...
            #.. is congruent to addition/multiplication mod a single divisor
            #this keeps the item values from getting intractable
            item %= Monkey.factors
            
            Monkey.monkeys[self.f_test(item)].items.append(item)
    

def solve(filename, rounds, div=True):
    Monkey.initialize()

    with open(filename) as f_in:
        monkey = None

        for tokens in map(lambda x: x.replace(",", "").split(), f_in):
            if len(tokens) == 0:
                continue

            elif tokens[0] == "Monkey":
                #make a new monkey
                monkey = Monkey(div=div)

            elif tokens[0] == "Starting":
                #initialize monkey items
                monkey.items = [int(item) for item in tokens[2:]]

            elif tokens[0] == "Operation:":
                #get the operation/operand tokens
                operation, operand = tokens[-2:]

                if operand == "old":
                    if operation == "*":
                        monkey.f_update = lambda x: x**2 

                    elif operation == "+":
                        monkey.f_update = lambda x: x*2
                
                else:
                    #operand is a constant
                    operand = int(operand)

                    if operation == "*":
                        #"capture" current value of operand
                        monkey.f_update = lambda x, operand=operand: x * operand

                    elif operation == "+":
                        #"capture" current value of operand
                        monkey.f_update = lambda x, operand=operand: x + operand

            elif tokens[0] == "Test:":
                #get the divisor
                operand = int(tokens[-1])
                
                #get the two destination monkeys
                dst_0, dst_1 = int(f_in.readline().split()[-1]), int(f_in.readline().split()[-1])

                #construct lambda to send the item to the correct destination monkey
                monkey.f_test = lambda x, operand=operand, dst_0=dst_0, dst_1=dst_1: dst_0 if x % operand == 0 else dst_1
                
                #calculate to product of all "divisible by" operands
                Monkey.factors *= operand

        for round in range(rounds):
            Monkey.do_round()

        x, y = sorted([monkey.inspections for monkey in Monkey.monkeys])[-2:]
        
        return x * y


if __name__ == "__main__":
    print(solve("test_input.txt", 20))
    print(solve("input.txt", 20))
    print(solve("test_input.txt", 10000, div=False))
    print(solve("input.txt", 10000, div=False))
