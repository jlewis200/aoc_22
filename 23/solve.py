#!/usr/bin/python3

from code import interact

INF = 2**32

class Elf(object):
    def __init__(self, y, x):
        self.y, self.x = y, x

        Elf.elves.add(self)
        Elf.positions.add((y, x))

    def propose(self):
        self.proposition = None

        #if any elf is adjacent
        if any(self.add_mod(mod) in Elf.positions for mod in Elf.mods.values()):

            #consider the directions in order
            for consideration in Elf.considerations:
                
                #check that the 3 positions in the direction are clear
                if all(not self.add_mod(mod) in Elf.positions for mod in Elf.directions[consideration]):
                    proposition = self.add_mod(Elf.mods[consideration])
                    self.proposition = proposition

                    if proposition in Elf.propositions:
                        Elf.propositions[proposition] += 1

                    else:
                        Elf.propositions[proposition] = 1

                    break

        #interact(local=locals())

    def move(self):
        #move if no other elf proposed moving to the proposed location
        if self.proposition is not None and Elf.propositions[self.proposition] == 1:
            self.y, self.x = self.proposition

        Elf.positions.add((self.y, self.x))

    def add_mod(self, modifier):
        return self.y + modifier[0], self.x + modifier[1]

    @classmethod
    def move_elves(cls):
        for elf in Elf.elves:
            elf.propose()

        Elf.positions = set()

        for elf in Elf.elves:
            elf.move()

        terminate = len(Elf.propositions) == 0
        
        Elf.propositions = {}

        Elf.considerations.append(Elf.considerations.pop(0))

        return terminate

    @classmethod
    def get_area(cls):
        y_min, y_max = INF, -INF
        x_min, x_max = INF, -INF

        for y, x in Elf.positions:
            y_min, y_max = min(y_min, y), max(y_max, y)
            x_min, x_max = min(x_min, x), max(x_max, x)

        return (y_max + 1 - y_min) * (x_max + 1 - x_min) - len(Elf.elves)

    @classmethod
    def initialize(cls):
        cls.elves = set()
        cls.positions = set()
        cls.propositions = {}

        cls.mods = {"NW": (-1, -1), 
                    "N":  (-1,  0), 
                    "NE": (-1,  1), 
                    "E":  ( 0,  1), 
                    "SE": ( 1,  1), 
                    "S":  ( 1,  0), 
                    "SW": ( 1, -1), 
                    "W":  ( 0, -1)}

        cls.considerations = ["N", "S", "W", "E"]
        cls.directions = {"N": (cls.mods["N"], cls.mods["NE"], cls.mods["NW"]),
                          "S": (cls.mods["S"], cls.mods["SE"], cls.mods["SW"]),
                          "W": (cls.mods["W"], cls.mods["NW"], cls.mods["SW"]),
                          "E": (cls.mods["E"], cls.mods["NE"], cls.mods["SE"])}
     
    @classmethod
    def print_board(cls):
        y_min, y_max = INF, -INF
        x_min, x_max = INF, -INF

        for y, x in Elf.positions:
            y_min, y_max = min(y_min, y), max(y_max, y)
            x_min, x_max = min(x_min, x), max(x_max, x)

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if (y, x) in Elf.positions:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()


def solve(filename):
    Elf.initialize()
    
    with open(filename) as f_in:
        board = []

        for line in f_in:
            board.append(list(line))

        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if col == '#':
                    Elf(y, x)

        Elf.print_board()

        for _ in range(10):
            Elf.move_elves()
            Elf.print_board()

        print(Elf.get_area())

def solve2(filename):
    Elf.initialize()
    
    with open(filename) as f_in:
        board = []

        for line in f_in:
            board.append(list(line))

        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if col == '#':
                    Elf(y, x)

        Elf.print_board()

        rounds = 1

        while not Elf.move_elves():
            rounds += 1
            Elf.print_board()

        print(rounds)


if __name__ == "__main__":
    #solve("test_input2.txt")
    solve("test_input.txt")
    #solve("input.txt")

    #solve2("test_input2.txt")
    #solve2("test_input.txt")
    solve2("input.txt")
