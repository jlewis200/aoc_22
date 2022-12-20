#!/usr/bin/python3

from math import copysign


class Node(object):
    #track the number of nodes in the list
    length = 0

    def __init__(self, value):
        self.value = value
        self.l = self
        self.r = self
    
    def remove(self):
        """
        Unlink node.
        """

        self.l.r = self.r
        self.r.l = self.l

        Node.length -= 1
 
    def insert(self, node):
        """
        Insert node to the right of self.
        """

        node.l = self 
        node.r = self.r
        node.l.r = node
        node.r.l = node

        Node.length += 1


def solve(filename, multiplier, mixs):
    """
    Solve the input for a given multiplier and number of mixs to perform.
    """

    #reset the list length
    Node.length = 0

    with open(filename) as f_in:
        #create nodes with multiplier
        nodes = [Node(multiplier * int(line)) for line in f_in]
        root = nodes[0]

        #append the nodes to the end of the list
        for node in nodes:
            root.l.insert(node)
        
        #mix some number of times
        for _ in range(mixs):
            mix(nodes)

        #find the zero node to traverse from
        zero_node = find(root, 0)
        
        #get the sum of the values at 1k, 2k, 3k
        return sum((traverse(zero_node, 1000).value,
                    traverse(zero_node, 2000).value,
                    traverse(zero_node, 3000).value))


def mix(nodes):
    """
    Mix the nodes.
    """

    for node in nodes:
        shift = node.value
        
        #remove the node
        node.remove()

        #left will be used to keep track of where the node should be reinserted
        left = traverse(node.l, shift)

        #reinsert the node at the shifted location
        left.insert(node)
        
        zero_node = find(nodes[0], 0)


def traverse(node, shift):
    """
    Traverse from node the number of times specified by shift.
    """

    #mod negative numbers as if they were positive
    shift = int(copysign(abs(shift) % Node.length, shift))

    #shift to the right
    while shift > 0:
        node = node.r
        shift -= 1
        
    #shift to the left
    while shift < 0:
        node = node.l
        shift += 1

    return node 


def find(node, value):
    """
    Find the first node with the given value.
    """

    while node.value != value:
        node = node.r

    return node


def print_list(root):
    """
    Print the list.
    """

    node = root.r
    print(f"{root.value}, ", end='')

    while node != root:
        print(f"{node.value}, ", end='')
        node = node.r

    print()

if __name__ == "__main__":
    print(f"part 1:  {solve('test_input.txt', 1, 1 )}")
    print(f"part 2:  {solve('test_input.txt', 811589153, 10)}")
    print(f"part 1:  {solve('input.txt', 1, 1 )}")
    print(f"part 2:  {solve('input.txt', 811589153, 10)}")
 
