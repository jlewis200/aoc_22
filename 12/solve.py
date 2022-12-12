#!/usr/bin/python3                                                                                                       
                                                                                                                         
import numpy as np                                                                                                       
from code import interact                                                                                                
                                                                                                                         
with open("input.txt") as f_in:                                                                                     
    array = []                                                                                                           
                                                                                                                         
    for line in map(str.strip, f_in):                                                                                    
        line = map(lambda x: ord(x), line)                                                                               
        array.append(list(line))                                                                                         
                                                                                                                         
    array = np.asarray(array)                                                                                            
                                                                                                                         
    start = np.nonzero(array == ord("S"))                                                                                
    end = np.nonzero(array == ord('E'))                                                                                  
                                                                                                                         
    #replace start/end with "a"/"z"                                                                                      
    array[start] = ord("a")                                                                                              
    array[end] = ord("z")                                                                                                
                                                                                                                         
    start = (start[1] + (start[0] * array.shape[1]))[0]                                                                  
    end = (end[1] + (end[0] * array.shape[1]))[0]                                                                        
                                                                                                                         
    adjacencies = [[] for _ in range(array.size)]                                                                        
    dist = [np.inf for _ in range(array.size)]                                                                           
    dist[start] = 0                                                                                                                     
                                                                                                                         
    for idx in range(array.shape[0]):                                                                                    
        for jdx in range(array.shape[1]):                                                                                
            src = jdx + (idx * array.shape[1])                                                                           
                                                                                                                         
            idx_prime = idx - 1                                                                                          
                                                                                                                         
            for y, x in [(idx - 1, jdx), (idx + 1, jdx), (idx, jdx - 1), (idx, jdx + 1)]:                                
                                                                                                                         
                if y >= 0 and x >= 0 and y < array.shape[0] and x < array.shape[1] and array[y, x] - array[idx, jdx] <= 1:
                    dst = x + (y * array.shape[1])                                                                       
                                                                                                                         
                    adjacencies[src].append(dst)                                                                         
                                                                                                                         
                                                                                                                         
    src = start                                                                                                          
    queue = [start]                                                                                                      
                                                                                                                         
    while src != end:                                                                                                    
        src = queue.pop(0)                                                                                               
                                                                                                                         
        for dst in adjacencies[src]:                                                                                     
                                                                                                                         
            if dist[dst] == np.inf:                                                                                      
                dist[dst] = dist[src] + 1                                                                                
                queue.append(dst)                                                                                        
                                                                                                                         
    print(dist[end])                                                                                                     
                                                                                                                         
                                                                                                                         
                                                                                                                         
    interact(local=locals())  
