#!/usr/bin/python3

import numpy as np
from code import interact


INF = 2**32
REWARDS_MASK = None

class Vertex(object):
    count = 0

    def __init__(self, label):
        self.index = Vertex.count
        Vertex.count += 1

        self.label = label
        self.flow = 0
        self.adjacencies = set()


def solve(filename, n_steps):
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
        rewards2 = get_rewards(vertices)

        #set the REWARDS_MASK
        global REWARDS_MASK
        REWARDS_MASK = rewards != 0
        n_states = 2**(rewards[REWARDS_MASK]).shape[0]

        #track the max future payoff given [step, pos]
        a_max = np.full((n_steps +1, rewards.shape[0], n_states), -1)
        
        #track the action which maximizes future payoff given [step, pos]
        a_argmax = np.full((n_steps+1, rewards.shape[0], n_states), -1)

        max_reward = recurse(0, 0, rewards, dist, n_steps, a_max, a_argmax)
        print(max_reward)

        step = 0
        pos = 0
        rewards_state = -1
        
        f=get_rewards_state

        reward_sum = 0

        while step <= 30 and rewards_state != 0:
            rewards_state = get_rewards_state(rewards)
            pos_prime = a_argmax[step, pos, rewards_state]
            step += 1 + dist[pos, pos_prime]
            reward_sum += (30 - step) * rewards[pos_prime]
           
            print("#"*80)
            print(f"step: {step}")
            print(f"pos: {pos}")
            print(f"rewards_state: {rewards_state}")
            print(f"pos_prime: {pos_prime}")
            print(f"pos_prime: {chr(ord('A') + pos_prime)}")
            print(f"reward_sum: {reward_sum}")
            print()
            
            pos = pos_prime
            rewards[pos] = 0
        
        interact(local=locals())

def get_boolean(array):
    res = 0
    for exponent, value in enumerate((array != 0)[::-1]):
        res += value * (2**exponent)
    return res

def get_rewards_state(rewards):
    return get_boolean(rewards[REWARDS_MASK])

def recurse(pos, step, rewards, dist, n_steps, a_max, a_argmax):
    max_reward = 0
    argmax_reward = 0
    rewards_state = get_rewards_state(rewards)

    #memoized result
#    if a_max[step, pos, rewards_state] != -1:
#        return a_max[step, pos, rewards_state]

    #get the future rewards for opening a valve given the current position
    future_rewards = rewards * (n_steps - step - dist[pos] - 1)

    #choose a move
    #use the highest reward first, then 2nd highest, etc...
    for pos_prime in future_rewards.argsort()[::-1]:
        step_prime = step + (dist[pos, pos_prime] + 1)
        
        #skip if the reward is 0 or the step count exceeds n_steps
        if rewards[pos_prime] == 0 or step_prime >= n_steps:
            continue
       
        #save the reward of pos_prime for later restoration
        saved_reward = rewards[pos_prime]

        #set the reward to 0 to prevent from future use (valve can only be turned on once)
        rewards[pos_prime] = 0

        reward = future_rewards[pos_prime] + recurse(pos_prime,
                                                     step_prime,
                                                     rewards,
                                                     dist,
                                                     n_steps,
                                                     a_max,
                                                     a_argmax)

        #restore the reward of pos_prime
        rewards[pos_prime] = saved_reward

        if reward > max_reward:
            max_reward = reward
            argmax_reward = pos_prime

    a_max[step, pos, rewards_state] = max_reward
    a_argmax[step, pos, rewards_state] = argmax_reward
    
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
    #solve("test_input.txt", 30)
    solve("input.txt", 30)
