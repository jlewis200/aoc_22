#!/usr/bin/python3


import numpy as np


from code import interact


def solve(filename):
    with open(filename) as f_in:
        coords = list()

        for coord in list(map(lambda x: x.strip().split(","), f_in)):
            coords.append(tuple(map(int, coord)))

        coords = np.asarray(coords, dtype=int)
        
        surface = 0

        for coord in coords:
            surface += get_surface(coords, coord)

        print(surface)


def get_surface(coords, coord):
    """
    Return a cube's exposed surface area not covered by another cube.
    """

    test_coords = [(0, 0, 1), (0, 0, -1),
                   (0, 1, 0), (0, -1, 0),
                   (1, 0, 0), (-1, 0, 0)]

    test_coords = np.asarray(test_coords)

    surface = 0

    for test_coord in test_coords:
        test_coord += coord

        print(test_coord)

        if not any(np.equal(coords, test_coord).all(1)):
            surface += 1
            
    return surface


if __name__ == "__main__":
    #solve("test_input.txt")
    solve("input.txt")
