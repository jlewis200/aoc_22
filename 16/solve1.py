#!/usr/bin/python3

import numpy as np
from code import interact


INF = 2**32


class Vertex(object):
    count = 0

    def __init__(self, label):
        self.index = Vertex.count
        Vertex.count += 1

        self.label = label
        self.flow = 0
        self.adjacencies = set()


def solve(filename):
    import re

    with open(filename) as f_in:
        vertices = {}
        root = None

        lines = [line for line in f_in]
        #parse the src valve first to keep indexes in a sensible order
        for line in lines:
            flow = int(re.findall(r"\d+", line)[0])
            labels = re.findall(r"[A-Z]{2}", line)

            #add new vertices
            for label in labels[:1]:
                if label not in vertices:
                    vertices[label] = Vertex(label)

        flows = np.zeros(Vertex.count, dtype=int)

        for line in lines:
            flow = int(re.findall(r"\d+", line)[0])
            labels = re.findall(r"[A-Z]{2}", line)

            #set flow
            src = vertices[labels.pop(0)]
            src.flow = flow
            flows[src.index] = flow

            if root is None:
                root = src

            #link vertices
            for dst in map(lambda label: vertices[label], labels):
                src.adjacencies.add(dst)
        
        #all pair shortest path:  dist[src, dst]
        dist = get_all_pair(vertices)
        
        interact(local=locals())


def get_all_pair(vertices):

    dist = np.full((Vertex.count, Vertex.count), INF, dtype=int)
    
    for src in vertices.values():
        dist[src.index] = bfs(src)

    return dist


def bfs(src):
    dist = np.full(Vertex.count, INF, dtype=int)
    dist[src.index] = 0

    queue = [src]

    while len(queue) > 0:
        src = queue.pop(0)

        #for every adjacent vertex
        for dst in src.adjacencies:

            #if unvisited, update dist and add to queue
            if dist[dst.index] == INF:
                dist[dst.index] = dist[src.index] + 1
                queue.append(dst)

    return dist

if __name__ == "__main__":
    solve("test_input.txt")
