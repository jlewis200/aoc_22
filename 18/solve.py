#!/usr/bin/python3


def solve(filename):
    with open(filename) as f_in:
        coords = list()

        for coord in list(map(lambda x: x.strip().split(","), f_in)):
            coords.append(tuple(map(int, coord)))

        print(f"part 1:  {get_surface(coords)}")
        print(f"part 2:  {get_external_surface(coords)}")


def get_external_surface(coords):
    """
    Return a cube's external exposed surface area, ignore internal area.
    """

    #get bounds which encompass the shape plus 1 unit 
    x_min, x_max, y_min, y_max, z_min, z_max = get_bounds(coords)
    
    x_rng = range(x_min, x_max + 1)
    y_rng = range(y_min, y_max + 1)
    z_rng = range(z_min, z_max + 1)
    ranges = (x_rng, y_rng, z_rng)

    #define the adjacent coords
    adjacencies = [(0, 0, 1), (0, 0, -1),
                   (0, 1, 0), (0, -1, 0),
                   (1, 0, 0), (-1, 0, 0)]
    
    surface = 0
    visited = []
    queue = [(x_min, y_min, z_min)]

    #BFS through the adjacent cubes
    while len(queue) > 0:
        coord = queue.pop(0)
        visited.append(coord)
        
        for adjacency in adjacencies:
            adjacency = add_coords(adjacency, coord)
            
            #increase surface area if the adjacency is a lava coord
            if adjacency in coords:
                surface += 1
           
            #add adjacency to queue if not a lava coord, within bounds, not visited, and not queued
            elif in_range(adjacency, *ranges) and adjacency not in visited and adjacency not in queue:
                queue.append(adjacency)
    
    return surface


def get_surface(coords):
    """
    Return a cube's exposed surface area not covered by another cube.
    """

    test_coords = [(0, 0, 1), (0, 0, -1),
                   (0, 1, 0), (0, -1, 0),
                   (1, 0, 0), (-1, 0, 0)]

    surface = 0

    for coord in coords:
        for test_coord in test_coords:
            test_coord = add_coords(test_coord, coord)

            if not test_coord in coords:
                surface += 1
            
    return surface


def get_bounds(coords):
    """
    Get the dimensional bounds of the coordinate list.
    """

    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    z_min, z_max = 0, 0

    for coord in coords:
        x_min, x_max = min(coord[0] - 1, x_min), max(coord[0] + 1, x_max)
        y_min, y_max = min(coord[1] - 1, y_min), max(coord[1] + 1, y_max)
        z_min, z_max = min(coord[2] - 1, z_min), max(coord[2] + 1, z_max)

    return x_min, x_max, y_min, y_max, z_min, z_max


def in_range(coord, x_rng, y_rng, z_rng):
    """
    Check if a coordinate is within range.
    """

    return coord[0] in x_rng and coord[1] in y_rng and coord[2] in z_rng


def add_coords(operand_0, operand_1):
    """
    Add 2 three-dimensional coords represented as a list of ints.
    """

    res = []

    for val_0, val_1 in zip(operand_0, operand_1):
        res.append(val_0 + val_1)

    return tuple(res)


if __name__ == "__main__":
    solve("test_input.txt")
    solve("input.txt")
