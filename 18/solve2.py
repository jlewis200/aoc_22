#!/usr/bin/python3


import numpy as np
import sys

from code import interact


def solve(filename):
    with open(filename) as f_in:
        coords = list()

        for coord in list(map(lambda x: x.strip().split(","), f_in)):
            coords.append(tuple(map(int, coord)))

        coords = np.asarray(coords, dtype=int)
        
        surface = get_external_surface(coords)

        print(surface)


def get_external_surface(coords):
    """
    Return a cube's external exposed surface area, ignore internal area.
    """
 
    #create bounds which encompass the shape plut 1 unit 
    x_min, x_max = coords[:, 0].min() - 1, coords[:, 0].max() + 1
    y_min, y_max = coords[:, 1].min() - 1, coords[:, 1].max() + 1
    z_min, z_max = coords[:, 2].min() - 1, coords[:, 2].max() + 1

    x_rng = range(x_min, x_max + 1)
    y_rng = range(y_min, y_max + 1)
    z_rng = range(z_min, z_max + 1)
    
    coord = np.asarray((x_min, y_min, z_min))
    visited = []

    test_coords = [(0, 0, 1), (0, 0, -1),
                   (0, 1, 0), (0, -1, 0),
                   (1, 0, 0), (-1, 0, 0)]
    
    return recurse(coords, coord, test_coords, visited, x_rng, y_rng, z_rng)


def recurse(coords, coord, test_coords, visited, x_rng, y_rng, z_rng):
    surface = 0

    if coord.tolist() in visited:
        return surface

    coord = np.asarray(coord)
    visited.append(coord.tolist())

    for test_coord in test_coords:
        test_coord += coord

        if any(np.equal(coords, test_coord).all(1)):
            surface += 1

        elif test_coord[0] in x_rng and \
             test_coord[1] in y_rng and \
             test_coord[2] in z_rng:
            surface += recurse(coords, test_coord, test_coords, visited, x_rng, y_rng, z_rng)
   
    return surface

if __name__ == "__main__":
    sys.setrecursionlimit(9999)

    solve("test_input.txt")
    solve("input.txt")
