#!/usr/bin/python3                                                                                                       

import numpy as np


INF = 2**32


with open("input.txt") as f_in:
    array = []

    for line in map(str.strip, f_in):
        line = map(lambda x: ord(x), line)
        array.append(list(line))

    array = np.asarray(array)

    #get indices of start/end
    start = np.nonzero(array == ord("S"))
    end = np.nonzero(array == ord('E'))

    #replace start/end with "a"/"z"
    array[start] = ord("a")
    array[end] = ord("z")

    #get flattened indices
    start = np.ravel_multi_index(start, array.shape)[0]
    end = np.ravel_multi_index(end, array.shape)[0]

    #BFS can provide a single source all dest shortest unweighted path
    #BFS starting from end to find shortest path to all other vertices
    dist = np.full(array.size, INF, dtype=int)
    dist[end] = 0

    #build the graph adjacency list
    adjacencies = [[] for _ in range(array.size)]

    for idx in range(array.shape[0]):
        for jdx in range(array.shape[1]):
            #get flat index
            src = np.ravel_multi_index((idx, jdx), array.shape)

            for mdx, ndx in [(idx - 1, jdx), (idx + 1, jdx), (idx, jdx - 1), (idx, jdx + 1)]:
                
                #if y, x in proper range
                if mdx >= 0 and \
                   ndx >= 0 and \
                   mdx < array.shape[0] and \
                   ndx < array.shape[1] and \
                   array[mdx, ndx] - array[idx, jdx] >= -1:
                    
                    #add adjacency
                    dst = np.ravel_multi_index((mdx, ndx), array.shape)
                    adjacencies[src].append(dst)

    #BFS
    queue = [end]                                                                                                      

    while len(queue) > 0:
        src = queue.pop(0)

        for dst in adjacencies[src]:

            #if unvisited, update dist and add to queue
            if dist[dst] == INF:
                dist[dst] = dist[src] + 1
                queue.append(dst)

    #get dist to start
    print(dist[start])                                                                                                     

    #get smallest dist to an 'a' vertex
    print(dist[array.flatten() == ord('a')].min())
