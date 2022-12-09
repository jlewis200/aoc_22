#!/usr/bin/python3

from math import copysign


class Node(object):

    x_min = 0
    x_max = 5
    y_min = -4
    y_max = 0

    def __init__(self, label):
        self.label = label
        self.x = 0
        self.y = 0
        self.parent = None
        self.child = None
        self.positions = set()

    def move(self, direction):
        
        #move the head node
        if direction == "U":
            self.y -= 1

        elif direction == "D":
            self.y += 1

        elif direction == "L":
            self.x -= 1

        elif direction == "R":
            self.x += 1

        #update the child nodes recursively
        self.child.update()
       
        #update the mins/maxs
        Node.x_min = min(self.x, Node.x_min)
        Node.x_max = max(self.x, Node.x_max)
        Node.y_min = min(self.y, Node.y_min)
        Node.y_max = max(self.y, Node.y_max)

    def update(self):
        h_move = False
        v_move = False

        #if manhattan distance between parent/child >= 3, this indicates a diagonal move is required
        if abs(self.x - self.parent.x) + abs(self.y - self.parent.y) >= 3:
            h_move = True
            v_move = True

        #a horizontal diff of 2 indicates a horizontal move is required
        elif abs(self.x - self.parent.x) == 2:
            h_move = True

        #a vertical diff of 2 indicates a vertical move is required
        elif abs(self.y - self.parent.y) == 2:
            v_move = True
        
        #vertical move
        if v_move:
            #move 1 unit in the required vertical direction
            self.y += copysign(1, self.parent.y - self.y)

        #horizontal move
        if h_move:
            #move 1 unit in the required horizontal direction
            self.x += copysign(1, self.parent.x - self.x)

        #add new coordinates to the positions set
        self.positions.add((self.y, self.x))

        #update the child nodes recursively
        if self.child is not None:
            self.child.update()

    def get_label(self, y, x):
        #parent nodes take priority over children, return first label in any grid location
        if self.y == y and self.x == x:
            return self.label

        #if no node occupies the position, return a "."
        if self.child is None:
            return "."

        #recurse
        return self.child.get_label(y, x)

    def print_board(self):
        for idx in range(Node.y_min, Node.y_max + 1):
            for jdx in range(Node.x_min, Node.x_max + 1):
                print(self.get_label(idx, jdx), end = '')
            print()
        print()

    def print_visited(self):
        for idx in range(Node.y_min, Node.y_max + 1):
            for jdx in range(Node.x_min, Node.x_max + 1):
                if (idx, jdx) in self.positions:
                    print("#", end='')
                else:
                    print(".", end='')
            print()
        print()


def solve(length, filename, debug=True):
    nodes = []

    labels = ["H"] + [str(idx) for idx in range(1, length)]
    nodes = [Node(label) for label in labels]

    #link child to parent
    for idx in range(1, length):
        nodes[idx].parent = nodes[idx - 1]

    #link parent to child
    for idx in range(0, length - 1):
        nodes[idx].child = nodes[idx + 1]

    head = nodes[0]
    tail = nodes[-1]

    with open(filename) as f_in:
        for direction, steps in map(str.split, f_in):

            if debug:
                print(f"== {direction} {steps} ==")

            for _ in range(int(steps)):
                head.move(direction)

                if debug:
                    head.print_board()

        if debug:
            tail.print_visited()

        print(len(tail.positions))


if __name__ == "__main__":
    solve(2, "test_input.txt", True)
    solve(10, "test_input.txt", True)

    solve(2, "input.txt", False)
    solve(10, "input.txt", False)
