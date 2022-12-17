#!/usr/bin/python3

import numpy as np
from multiprocessing import Pool
from os import cpu_count
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
        rewards = get_rewards(vertices)


        from itertools import combinations
        max_reward = 0
        non_zero_indices = np.where(rewards != 0)[0].tolist()
        
        progress = 0

        with Pool(max(2, cpu_count() - 2)) as pool:
            for n in range(1, 1 + len(non_zero_indices)//2):
                print(f"{n}/{len(non_zero_indices)//2}:  ", end='')
                stuffs = []

                for combination in combinations(non_zero_indices, n):
                    
                    rewards_0 = rewards.copy()
                    rewards_1 = rewards.copy()
                    
                    for idx in non_zero_indices:
                        
                        #remove indicies not in combination for first run
                        if idx in combination:
                            rewards_0[idx] = 0

                        #remove indicies in combinations for second run
                        else:                
                            rewards_1[idx] = 0

                    stuff = rewards_0, rewards_1, dist, vertices
                    stuffs.append(stuff)


                combinations_maxs = pool.map(get_max_reward_double, stuffs)
                max_reward = max(*combinations_maxs, max_reward)
                print(max_reward)
                 

def get_max_reward_double(stuff):
    rewards_0, rewards_1, dist, vertices = stuff
    reward = get_max_reward(vertices["AA"].index, 26, rewards_0, dist)
    reward += get_max_reward(vertices["AA"].index, 26, rewards_1, dist)

    return reward


def get_max_reward(pos, rem_step, rewards, dist):
    max_reward = 0

    for pos_prime in range(rewards.shape[0]):
        rem_step_prime = rem_step - (dist[pos, pos_prime] + 1)
        
        #skip if the reward is 0 or the step count exceeds n_steps
        if rewards[pos_prime] == 0 or rem_step_prime <= 0:
            continue
     
        #future reward of turning this valve on
        future_reward = rem_step_prime * rewards[pos_prime]

        #save the reward of pos_prime for later restoration
        saved_reward = rewards[pos_prime]

        #set the reward to 0 to prevent from future use (valve can only be turned on once)
        rewards[pos_prime] = 0
        
        #get the reward of taking this step and then the maximum subsequent reward
        reward = future_reward + get_max_reward(pos_prime, rem_step_prime, rewards, dist)

        #restore the reward of pos_prime
        rewards[pos_prime] = saved_reward

        max_reward = max(reward, max_reward)

    return max_reward


def get_rewards(vertices):
    rewards = np.zeros(Vertex.count, dtype=int)

    for vertex in vertices.values():
        rewards[vertex.index] = vertex.flow

    return rewards


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
    solve("input.txt")
