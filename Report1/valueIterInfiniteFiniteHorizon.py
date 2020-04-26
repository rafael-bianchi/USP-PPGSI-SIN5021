# Reward function
def R(s,a):
    return -1


# Probability matrix
def T(a,s,s_l):
    return 1.0


from random import random
import numpy as np

A = [ 'N', 'E', 'W', 'S'] #possible actions
S = 10  #Number of states

k = 0
k_max = 10

gamma = 0.99
epsilon = 1.0
l2norm = 0.0 #init

V = np.zeros((1,S))

while (k < k_max and epsilon > l2norm):
    V_k_plus_1 = np.empty((1,S), float)
    for s in range(0, S):
        max_V = float("-inf")
        for a in A:
            sum_next_ss =  sum([ T(s,a,s_l) * V[k][s_l] for s_l in range(0, S)])
            v = R(s,a) + gamma * sum_next_ss
            if (v > max_V):
                max_V = v
        
        V_k_plus_1[0, s] = max_V

    l2norm = V.linalg.norm() #k - (k-1)
    k += 1

    V = np.append(V, V_k_plus_1, axis=0)
