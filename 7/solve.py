#!/usr/bin/python3


class Vertex(object):
    def __init__(self, parent=None):
        self.files = {}
        self.parent = parent 
        self.children = {}
        self.size = 0


def build_tree(f_in):
    root = Vertex()
    vertex = root

    for tokens in map(lambda x: x.strip().split(), f_in):
        
        if tokens[0] == "$":

            if tokens[1] == "cd":
                
                if tokens[2] == "/":
                    vertex = root
                
                elif tokens[2] == "..":
                    vertex = vertex.parent
                
                else:
                    vertex = vertex.children[tokens[2]]

            elif tokens[1] == "ls":
                pass

        elif tokens[0] == "dir":
            vertex.children[tokens[1]] = Vertex(vertex)

        else:
            vertex.files[tokens[1]] = int(tokens[0])

    return root


def dfs(vertex, sizes):
    for child in vertex.children.values():
        dfs(child, sizes)
        vertex.size += child.size

    vertex.size += sum(vertex.files.values())
    sizes.append(vertex.size)


def part_1(root, sizes):
    size_sum = 0

    for size in sorted(sizes):
        if size > 100000:
            return size_sum

        size_sum += size


def part_2(root, sizes):
    min_delete_size = 30000000 - (70000000 - root.size)

    for size in sorted(sizes):
        if size >= min_delete_size:
            return size


def main():
    with open("input.txt") as f_in:
        root = build_tree(f_in)
        sizes = list()
        dfs(root, sizes)

        print(f"part 1:  {part_1(root, sizes)}")
        print(f"part 2:  {part_2(root, sizes)}")
        

if __name__ == "__main__":
    main()

