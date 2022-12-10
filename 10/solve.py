#!/usr/bin/python3

class Cpu(object):
    def __init__(self):
        self.cycle = 1
        self.x = 1
        self.cycles = [idx for idx in range(20, 221, 40)]
        self.signals = []
        self.render = ""

    def op(self, tokens):
        
        if tokens[0] == "noop":
            self.noop()

        elif tokens[0] == "addx":
            self.addx(int(tokens[1]))

    def noop(self):
        self.tick()

    def addx(self, val):
        #tick twice before performing the addition
        self.tick()
        self.tick()
        self.x += val

    def tick(self):
       
        #calculate the signal strength if this is one of the target cycles
        if self.cycle in self.cycles:
            self.signals.append(self.cycle * self.x)

        #render a "#" if self.x is within one pixel of the cycle (mod 40), else render "."
        if abs(self.x - (self.cycle % 40) + 1) <= 1:
            self.render += "#"
        else:
            self.render += "."

        self.cycle += 1


def solve(filename):
    cpu = Cpu()

    with open(filename) as f_in:
        for tokens in map(str.split, f_in):
            cpu.op(tokens)

    print(sum(cpu.signals))

    for idx in range(0, 241, 40):
        print(cpu.render[idx:idx+40])


if __name__ == "__main__":
    solve("test_input.txt")
    solve("input.txt")

