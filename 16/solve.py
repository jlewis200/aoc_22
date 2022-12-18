#!/usr/bin/python3

import re
import numpy as np

from multiprocessing import Pool
from os import cpu_count
from itertools import combinations


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
    with open(filename) as f_in:
        vertices = {}

        for line in f_in:
            flow = int(re.findall(r"\d+", line)[0])
            labels = re.findall(r"[A-Z]{2}", line)

            #add new vertices
            for label in labels:
                if label not in vertices:
                    vertices[label] = Vertex(label)
            
            #set flow
            src = vertices[labels.pop(0)]
            src.flow = flow

            #link vertices
            for dst in map(lambda label: vertices[label], labels):
                src.adjacencies.add(dst)
        
        #all pair shortest path:  dist[src, dst]
        dist = get_all_pair(vertices)
        
        #get flow rates for:  flows[idx] = flow_rate
        flows = get_flows(vertices)

        ########################################################################
        #solve part 1
        print(f"part 1:  {get_max_flow(vertices['AA'].index, 30, flows, dist)}")
       
        ########################################################################
        #solve part 2
        
        #find the maximal flow for a given partition of the valve graph using two independent actors
        max_flow = 0

        #find idices where flow is non-zero
        non_zero_indices = np.where(flows != 0)[0].tolist()
        
        progress = 0

        with Pool(max(2, cpu_count() - 2)) as pool:

            #partition the valves each actor will open into every n choose k possibility
            for n in range(1, 1 + len(non_zero_indices)//2):
                args = []

                #build the args list
                for combination in combinations(non_zero_indices, n):
                    flows_0 = flows.copy()
                    flows_1 = flows.copy()
                    
                    for idx in non_zero_indices:
                        #remove indicies not in combination for first run
                        if idx in combination:
                            flows_0[idx] = 0

                        #remove indicies in combinations for second run
                        else:                
                            flows_1[idx] = 0

                    args.append((flows_0, flows_1, dist, vertices))

                #use the multiprocessing pool to perform execute find the max of the partitions
                combinations_maxs = pool.map(get_max_flow_double, args)
                
                #find the max of this set of combinations and preivous iteration
                max_flow = max(*combinations_maxs, max_flow)
                
                #print the progress
                print(f"part 2:  {n}/{len(non_zero_indices)//2}:  {max_flow}")

        print(f"part 2:  {max_flow}")
                 

def get_max_flow_double(arg):
    """
    Return the maximum flow of two actors working working with mutually
    exclusive sets of valves.
    """

    flows_0, flows_1, dist, vertices = arg
    flow = get_max_flow(vertices["AA"].index, 26, flows_0, dist)
    flow += get_max_flow(vertices["AA"].index, 26, flows_1, dist)

    return flow


def get_max_flow(pos, rem_step, flows, dist):
    """
    Return the maximum future flow given current position, number of remaining
    steps, valve flows, and 2-D dist matrix.
    """

    max_flow = 0

    for pos_prime in range(flows.shape[0]):
        #get the remaining steps for moving from pos to pos_prime
        rem_step_prime = rem_step - (dist[pos, pos_prime] + 1)
        
        #skip if the flow is 0 or the step count exceeds n_steps
        if flows[pos_prime] == 0 or rem_step_prime <= 0:
            continue
     
        #future flow of turning this valve on
        future_flow = rem_step_prime * flows[pos_prime]

        #save the flow of pos_prime for later restoration
        saved_flow = flows[pos_prime]

        #set the flow to 0 to prevent from future use (valve can only be turned on once)
        flows[pos_prime] = 0
        
        #get the flow of taking this step and then the maximum subsequent flow
        flow = future_flow + get_max_flow(pos_prime, rem_step_prime, flows, dist)

        #restore the flow of pos_prime
        flows[pos_prime] = saved_flow

        max_flow = max(flow, max_flow)

    return max_flow


def get_flows(vertices):
    """
    Return the flow for each valve as an array.
    """

    flows = np.zeros(Vertex.count, dtype=int)

    for vertex in vertices.values():
        flows[vertex.index] = vertex.flow

    return flows


def get_all_pair(vertices):
    """
    Return the all pair shortest paths as a 2-D array.
    """

    dist = np.full((Vertex.count, Vertex.count), INF, dtype=int)
    
    for src in vertices.values():
        dist[src.index] = bfs(src)

    return dist


def bfs(src):
    """
    Return the single-source/all-dest shortest path as an array.
    """

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
    solve("input.txt")
