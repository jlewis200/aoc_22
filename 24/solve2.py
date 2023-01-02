#!/usr/bin/python3

import numpy as np

class Blizzard(object):
    x_max = None
    y_max = None

    positions = None
    blizzards = None

    def __init__(self, y, x, y_v, x_v, char):
        self.y = y
        self.x = x

        self.y_v = y_v #y movement vector
        self.x_v = x_v #x movement vector

        self.char = char

        Blizzard.positions.add((y, x))
        Blizzard.blizzards.add(self)

    def move(self):
        self.y += self.y_v
        self.x += self.x_v

        self.y %= Blizzard.y_max
        self.x %= Blizzard.x_max

        Blizzard.positions.add((self.y, self.x))

    @classmethod
    def move_all(cls):
        cls.positions = set()

        for blizzard in cls.blizzards:
            blizzard.move()

    @classmethod
    def initialize(cls):
        cls.x_max = 0
        cls.y_max = 0

        cls.positions = set()
        cls.blizzards = set()

    @classmethod
    def validate(cls, y, x):
        return y >= 0 and y < cls.y_max and \
               x >= 0 and x < cls.x_max and \
               (y, x) not in cls.positions

    @classmethod
    def enumerate(cls, y, x):
        res = set()

        for y_d, x_d in {(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)}:
            pos_prime = (y + y_d, x + x_d)

            if cls.validate(*pos_prime):
                res.add(pos_prime)

        return res

    @classmethod
    def get_board(cls):
        board = np.full((cls.y_max, cls.x_max), '.')
        
        for blizzard in cls.blizzards:

            if board[blizzard.y, blizzard.x] == '.':
                board[blizzard.y, blizzard.x] = blizzard.char
            
            elif board[blizzard.y, blizzard.x] in ('>', 'v', '<', '^'):
                board[blizzard.y, blizzard.x] = '2'

            else:
                board[blizzard.y, blizzard.x] = str(int(board[blizzard.y, blizzard.x]) + 1)


        return str(board)


def solve(filename):
    Blizzard.initialize()
    board = []

    with open(filename) as f_in:
        for line in f_in:
            board.append(list(line.replace('#', '').strip()))

        #remove first/last lines
        board.pop(0)
        board.pop(-1)

        board = np.asarray(board)
        Blizzard.y_max, Blizzard.x_max = board.shape

        for y, row in enumerate(board):
            for x, col in enumerate(row):

                if col == '>':
                    Blizzard(y, x, 0, 1, '>')

                elif col == '<':
                    Blizzard(y, x, 0, -1, '<')

                elif col == '^':
                    Blizzard(y, x, -1, 0, '^')

                elif col == 'v':
                    Blizzard(y, x, 1, 0, 'v')
        
        #epedate to goal/start/goal, don't count last step of 1st/2nd trips
        steps = expedate((0, 0), (Blizzard.y_max - 1, Blizzard.x_max - 1)) - 1
        steps += expedate((Blizzard.y_max - 1, Blizzard.x_max - 1), (0, 0)) - 1
        steps += expedate((0, 0), (Blizzard.y_max - 1, Blizzard.x_max - 1))
        print(steps)
        
def expedate(start, end):
    #expedate:  the act of expeditioning

    #expedition positions
    e_pos = set()

    step = 0

    while end not in e_pos: # and step < 20:
        step += 1
       
        print('#'*80)
        print(step)
        print(Blizzard.get_board())
        print()
        #breakpoint()

        #move all blizzards
        Blizzard.move_all()

        #set up the next expedition positions set
        e_pos_prime = set()

        #check for open positions to move to based on previous positions
        for e in e_pos:
            e_pos_prime.update(Blizzard.enumerate(*e))

        #check if initial position is open
        if start not in Blizzard.positions:
            e_pos_prime.add(start)

        e_pos = e_pos_prime

    return step + 1 #plus 1 step to exit the board

        
if __name__ == "__main__":
    solve("test_input.txt")
    solve("input.txt")
