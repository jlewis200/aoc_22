#!/usr/bin/python3

class Node(object):

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    def __init__(self, label):
        self.label = label
        self.parent = None
        self.x = 0
        self.y = 0
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.child = None
        self.positions = set()

    def move(self, direction):

        if direction == "U":
            self.y -= 1

        elif direction == "D":
            self.y += 1

        elif direction == "L":
            self.x -= 1

        elif direction == "R":
            self.x += 1

        self.child.update()
        
        Node.x_min = min(self.x, Node.x_min)
        Node.x_max = max(self.x, Node.x_max)
        Node.y_min = min(self.y, Node.y_min)
        Node.y_max = max(self.y, Node.y_max)

    def update(self):

        if abs(self.x - self.parent.x) >= 2:
            self.y = self.parent.y

        elif abs(self.y - self.parent.y) >= 2:
            self.x = self.parent.x
       
        if self.x == self.parent.x:
            self.y += int((self.parent.y - self.y) / 2) #round towards zero

        elif self.y == self.parent.y:
            self.x += int((self.parent.x - self.x) / 2) #round towards zero

        self.positions.add((self.y, self.x))

        if self.child is not None:
            self.child.update()

    def print_position(self):
        print(f"{self.y} {self.x}") 

    def get_label(self, y, x):
        if self.y == y and self.x == x:
            return self.label

        if self.child is None:
            return "."

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

    Node.y_min = -4
    Node.x_max = 5

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
#    solve(10, "test_input.txt", True)

    #solve(2, "input.txt", False)
    #solve(10, "input.txt", True)
