#!/usr/bin/python3

import re
import numpy as np

from math import copysign
from code import interact

def solve(filename, cube_size):
    with open(filename) as f_in:
        board = []
        max_len = 0

        for line in f_in:
            if len(line) == 1:
                break

            board.append(list(line.replace('\n', '')))
            
            max_len = max(max_len, len(board[-1]))
        
        for row in board:
            while len(row) < max_len:
                row.append(' ')

        board = np.asarray(board)
        start = np.argwhere(board=='.')[0]

        path = f_in.readline().strip()
        path = re.findall(r"\d+|R|L", path)

        print_board(board)
        print_board(path)

        cube = get_cube(board, cube_size)
        
        print_cube(cube)

        interact(local=locals())

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
    cube = np.full((cube_size + 2, cube_size + 2, cube_size + 2), ' ')
    
    y = 0
    x = 0

    #find first non-empty face of board
    while board[y, x] == ' ':
        x += cube_size

    #roll cube along the board
    roll_cube(board.copy(), cube, y, x)

    return cube

def roll_cube(board, cube, y, x):
    """
    Roll the cube along the board to "pick up" the board layout.  Geometrically this would look
    like rolling the cube from underneath the board so the layout isn't reversed.
    """

    #cube size is shape - edge padding
    cube_size = cube.shape[0] - 2
    
    #check if cube is under a valid index and non-empty portion of the board
    if y < 0 or y >= board.shape[0] or \
       x < 0 or x >= board.shape[1] or \
       board[y, x] == ' ':
        return

    #copy the board to cube face
    cube[0, 1:-1, 1:-1] = board[y: y + cube_size, x: x + cube_size]

    #clear the board area to prevent repeated copying
    board[y: y + cube_size, x: x + cube_size] = ' '
   
    rolls, shifts = get_rolls(), get_shifts(cube_size)

    #try each roll/shift combination
    for roll, shift in zip(rolls, shifts):
        roll_cube(board, roll(cube), *shift(y, x))


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
    print(f"part 1:  {solve('test_input.txt', 4)}")
#    print(f"part 1:  {solve('input.txt')}")

