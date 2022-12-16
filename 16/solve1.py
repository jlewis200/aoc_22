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
        rewards = get_rewards(vertices)

        max_reward = recurse(0, 0, rewards, dist, 30)
        print(max_reward)


def recurse(pos, step, rewards, dist, n_steps=30, a_max=None, a_argmax=None):
    if a_max is None or a_argmax is None:
        #track the max future payoff given [step, pos]
        a_max = np.full((n_steps, rewards.shape[0]), -1)
        
        #track the action which maximizes future payoff given [step, pos]
        a_argmax = np.full((n_steps, rewards.shape[0]), -1)
        a_argmax

    reward = 0
    max_reward = 0
    argmax_reward = 0

    if a_max[step, pos] != -1:
        return a_max[step, pos]

    #get the future rewards for opening a valve given the current position
    future_rewards = rewards * (n_steps - step - dist[pos] - 1)

    #choose a move
    #use the highest reward first, then 2nd highest, etc...
    for pos_prime in future_rewards.argsort()[::-1]:
        step_prime = step + (dist[pos, pos_prime] + 1)
        
        #skip if the reward is 0 or the step count exceeds n_steps
        if rewards[pos_prime] == 0 or step_prime >= n_steps:
            continue
        
        rewards_prime = rewards.copy()
        rewards_prime[pos_prime] = 0

        reward = future_rewards[pos_prime] + recurse(pos_prime, step_prime, rewards_prime, dist)

        if reward > max_reward:
            max_reward = reward
            argmax_reward = pos_prime

    a_max[step, pos] = max_reward
    print(f"{step} {max_reward}")
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
    #solve("input.txt")
