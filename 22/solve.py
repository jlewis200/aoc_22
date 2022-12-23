#!/usr/bin/python3

import re

from code import interact


class Vertex(object):
    root = None

    def __init__(self, row, col, wall=False):
        self.row = row
        self.col = col
        self.wall = wall
        
        self.up = None
        self.right = None
        self.down = None
        self.left = None

        if Vertex.root is None:
            Vertex.root = self

def solve(filename):
    Vertex.root = None

    with open(filename) as f_in:
        board = []

        for line in f_in:
            if len(line) == 1:
                break

            board.append(list(line.replace('\n', '')))


        max_row = []

        #create vertices
        for idx, row in enumerate(board):
            max_row = row if len(row) > len(max_row) else max_row

            for jdx, col in enumerate(row):
                if col in ('#', '.'):
                    board[idx][jdx] = Vertex(idx + 1, jdx + 1, wall=(col=='#'))

                else:
                    board[idx][jdx] = None

        #pad to create a uniform column length with at least 1 None
        length = len(max_row) + 1

        for row in board:
            while len(row) < length:
                row.append(None)
        board.append([None] * len(max_row))

        #link rows 
        for idx, _ in enumerate(board):
            link_horizontal(board, idx)
                
        for jdx, _ in enumerate(board[0]):
            link_vertical(board, jdx)

        path = f_in.readline().strip()
        path = re.findall(r"\d+|R|L", path)

        vertex = Vertex.root

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
                vertex = traverse(vertex, orientation, dist)

            orientation %= 4

        value = (1000 * vertex.row) + (4 * vertex.col) + orientation
        return value
        #interact(local=locals())


def traverse(vertex, orientation, dist):
    if orientation == 0:
        for _ in range(dist):
            if not vertex.right.wall:
                vertex = vertex.right

    elif orientation == 1:
        for _ in range(dist):
            if not vertex.down.wall:
                vertex = vertex.down

    elif orientation == 2:
        for _ in range(dist):
            if not vertex.left.wall:
                vertex = vertex.left

    elif orientation == 3:
        for _ in range(dist):
            if not vertex.up.wall:
                vertex = vertex.up

    return vertex

def link_vertical(board, col):
    """
    Link a row vertically.
    """

    idx = 0
    
    #traverse to the first vertex in the column
    while board[idx][col] is None:
        idx += 1

        if idx == len(board):
            return

    #save reference to the first vertex in the column
    vertex_0 = board[idx][col]

    #link contiguous vertices
    while board[idx + 1][col] is not None:
        board[idx][col].down = board[idx + 1][col]
        board[idx + 1][col].up = board[idx][col]

        idx += 1

    #link first and last vertices
    board[idx][col].down = vertex_0
    vertex_0.up = board[idx][col]


def link_horizontal(board, row):
    """
    Link a row horizontally.
    """

    idx = 0
    
    #traverse to the first vertex in the row
    while board[row][idx] is None:
        idx += 1

        if idx == len(board[row]):
            return

    #save reference to the first vertex in the row
    vertex_0 = board[row][idx]

    #link contiguous vertices
    while board[row][idx + 1] is not None:
        board[row][idx].right = board[row][idx + 1]
        board[row][idx + 1].left = board[row][idx]

        idx += 1

    #link first and last vertices
    board[row][idx].right = vertex_0
    vertex_0.left = board[row][idx]


if __name__ == "__main__":
    print(f"part 1:  {solve('test_input.txt')}")
    print(f"part 1:  {solve('input.txt')}")

