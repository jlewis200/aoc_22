#!/usr/bin/python3

import re
import numpy as np

from math import copysign
from code import interact

class Char(object):
    """
    Wrapper to provide a pseudo mutable string type.
    """

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.val == other


def solve(filename, cube_size):
    with open(filename) as f_in:
        board = []
        max_len = 0

        for line in f_in:
            if len(line) == 1:
                break

            line = [Char(char) for char in line.replace('\n', '')]

            board.append(line)
            
            max_len = max(max_len, len(board[-1]))
        
        for row in board:
            while len(row) < max_len:
                row.append(Char(' '))

        #convert the string to int
        #i use a mutable type here so changes to the cube faces are reflected in the flat board representation
        #python strings are immutable so it ends up replacing the refrerence in the cube and changes don't reflect back to the board
        board = np.asarray(board)

        path = f_in.readline().strip()
        path = re.findall(r"\d+|R|L", path)

        print_board(board)
        print(path)
        
        cube = get_cube(board, cube_size)
        
        print_cube(cube)
        

        traverse(cube, path)

        print_cube(cube)
        print_board(board)

        index = (np.argwhere(board == 'X') + 1)[0]
        interact(local=locals())
        value = index[0] * 1000 + index[1] * 4
        print(value)
        return value

def walk(cube, y_0, x_0, orientation, dist):
    roll_f, roll_b, roll_r, roll_l = get_rolls()
    cube_size = cube.shape[0]

    while dist > 0:
        y_1, x_1 = y_0, x_0

        if orientation == 0:
            x_1 += 1

        elif orientation == 1:
            y_1 += 1

        elif orientation == 2:
            x_1 -= 1

        elif orientation == 3:
            y_1 -= 1

        if cube[0, y_1, x_1] in ('.', '>', 'v', '<', '^'):
            y_0, x_0 = y_1, x_1

            id_0 = id(cube[0, y_0, x_0])
            cube[0, y_0, x_0].val = get_or(orientation)
            if id_0 != id(cube[0, y_0, x_0]):
                print('wtf')
                interact(local=locals())

        elif cube[0, y_1, x_1] == '#':
            #early termination if we hit a wall
            dist = 0

        elif y_1 == 0 and cube[1, y_1, x_1] != '#':
            #rotate cube back, place agent at bottom of cube face
            return walk(roll_b(cube), cube.shape[0] - 1, x_0, orientation, dist)

        elif y_1 == cube_size - 1 and cube[1, y_1, x_1] != '#':
            #rotate cube forward, place agent at top of cube face
            return walk(roll_f(cube), 0, x_0, orientation, dist)

        elif x_1 == 0 and cube[1, y_1, x_1] != '#':
            #rotate cube left, place agent at right of cube face
            return walk(roll_l(cube), y_0, cube.shape[0] - 1, orientation, dist)

        elif x_1 == cube_size - 1 and cube[1, y_1, x_1] != '#':
            #rotate right, place agent at left of cube face
            return walk(roll_r(cube), y_0, 0, orientation, dist)

        dist -= 1

    return cube, y_0, x_0

def traverse(cube, path):
    y, x = 1, 1

    #0 R
    #1 D
    #2 L
    #3 U
    orientation = 0

    for move in path:
        if move == "R":
            orientation += 1

        elif move == "L":
            orientation -= 1

        else:
            dist = int(move)
            cube, y, x = walk(cube, y, x, orientation, dist)

        orientation %= 4

        cube[0, y, x].val = get_or(orientation)
    cube[0, y, x].val = 'X'
    #cube[0, y, x].val = f"{orientation}"
    #value = (1000 * y) + (4 * x) + orientation
    #TODO: calculate the orientation from the board perspective
    value = (1000 * y) + (4 * x)
    return value

def get_or(orientation):

    if orientation == 0:
        orientation = '>'

    elif orientation == 1:
        orientation = 'v'

    elif orientation == 2:
        orientation = '<'

    elif orientation == 3:
        orientation = '^'

    return orientation


def print_cube(cube):
    roll_f, roll_b, roll_r, roll_l = get_rolls()

    for _ in range(4):
        print('#' * 80)
        print_board(cube[0, 1:-1, 1:-1])
        cube = roll_f(cube)

    for _ in range(4):
        print('#' * 80)
        print_board(cube[0, 1:-1, 1:-1])
        cube = roll_l(cube)



def get_cube(board, cube_size):
    cube = np.full((cube_size + 2, cube_size + 2, cube_size + 2), Char(' '))
    
    y = 0
    x = 0

    #find first non-empty face of board
    while board[y, x] == ' ':
        x += cube_size

    #use a stack to keep track of the rolls
    roll_stack = []

    #roll cube along the board
    roll_cube(board.copy(), cube, y, x)

    return cube

def roll_cube(board, cube, y, x):
    """
    Roll the cube along the board to "pick up" the board layout.  Geometrically this would look
    like rolling the cube from underneath the board so the layout isn't reversed.  Return true if
    a face was absorbed into the cube.
    """

    #cube size is shape - edge padding
    cube_size = cube.shape[0] - 2
    
    #check if cube is under a valid index and non-empty portion of the board
    if y < 0 or y >= board.shape[0] or \
       x < 0 or x >= board.shape[1] or \
       board[y, x] == ' ':
        return False

    #copy the board to cube face
    cube[0, 1:-1, 1:-1] = board[y: y + cube_size, x: x + cube_size]

    #clear the board area to prevent repeated copying
    board[y: y + cube_size, x: x + cube_size] = ' '
   
    rolls, shifts = get_rolls(), get_shifts(cube_size)

    #try each roll/shift combination
    for roll, shift in zip(rolls, shifts):
        roll_cube(board, roll(cube), *shift(y, x))

    return True

def get_rolls():
    #initialize the cube rolls
    roll_f = lambda cube: np.rot90(cube, axes=(0, 1))
    roll_b = lambda cube: np.rot90(cube, axes=(1, 0))
    roll_r = lambda cube: np.rot90(cube, axes=(0, 2))
    roll_l = lambda cube: np.rot90(cube, axes=(2, 0))

    return (roll_f, roll_b, roll_r, roll_l)


def get_shifts(cube_size):
    #initialize the board shifts
    shift_f = lambda y, x: (y + cube_size, x)
    shift_b = lambda y, x: (y - cube_size, x)
    shift_r = lambda y, x: (y, x + cube_size)
    shift_l = lambda y, x: (y, x - cube_size)

    return (shift_f, shift_b, shift_r, shift_l)


def print_board(board):
    """
    Print the board.
    """

    for row in board:
        for col in row:
            print(col, end='')

        print()
    print()

if __name__ == "__main__":
 #   print(f"part 2:  {solve('test_input.txt', 4)}")
    print(f"part 2:  {solve('input.txt', 50)}")

