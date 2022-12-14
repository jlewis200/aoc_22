#!/usr/bin/python3


import numpy as np
from math import copysign


def print_board(array):
    for row in array:
        for element in row:
            print(element, end='')
        print()


def draw_line(array, x_0, y_0, x_1, y_1):
    x_step = 0
    y_step = 0
    
    if x_0 != x_1:
        x_step = int(copysign(1, x_1 - x_0))

    if y_0 != y_1:
        y_step = int(copysign(1, y_1 - y_0))

    array[y_0, x_0] = "#" 

    while (x_0, y_0) != (x_1, y_1):
        x_0 += x_step
        y_0 += y_step
        array[y_0, x_0] = "#"

def get_array(filename):
    array = None
    y_max = 0

    with open(filename) as f_in:
        array = np.full((1000,1000), ".", dtype="<U1")

        for line in f_in:
            points = line.split(" -> ")
            
            x_0, y_0 = map(int, points.pop(0).split(","))

            while len(points) > 0:
                x_1, y_1 = map(int, points.pop(0).split(","))
                y_max  = max(y_max, y_0, y_1)
                    
                draw_line(array, x_0, y_0, x_1, y_1)
                x_0, y_0 = x_1, y_1

        draw_line(array, 0, y_max + 2, array.shape[1] - 1, y_max + 2)

    return array, y_max

def solve1(filename):
    array, y_max = get_array(filename)

    idx = 0
    initial = (500, 0)
    x, y = initial

    #while the sand source is not blocked
    while y < y_max:

        #down path open
        if array[y + 1, x] == ".":
            y += 1

        #down path blocked, try left
        elif array[y + 1, x - 1] == ".":
            y += 1
            x -= 1

        #down-left path blocked, try down-right
        elif array[y + 1, x + 1] == ".":
            y += 1
            x += 1
        
        #no path, sand rests here, reset sand coords
        else:
            array[y, x] = 'o'
            idx += 1
            x, y = initial

    print(idx)
    print_board(array[:y_max + 3, 300:701])


def solve2(filename):
    array, y_max = get_array(filename)

    idx = 0
    initial = (500, 0)
    x, y = initial

    #while the sand source is not blocked
    while array[y, x] != "o":

        #down path open
        if array[y + 1, x] == ".":
            y += 1

        #down path blocked, try left
        elif array[y + 1, x - 1] == ".":
            y += 1
            x -= 1

        #down-left path blocked, try down-right
        elif array[y + 1, x + 1] == ".":
            y += 1
            x += 1
        
        #no path, sand rests here, reset sand coords
        else:
            array[y, x] = 'o'
            idx += 1
            x, y = initial

    print(idx)
    print_board(array[:y_max + 3, 300:701])

if __name__ == "__main__":
    solve1("input.txt")
    solve2("input.txt")
