N = 100 #Horizon
S = 10  #Number of states

#1. defina V(s, N) = 0
V = [[0]*S]*N



for n in range(N-1, 0-1, -1):
    for s in range(0,S):
        for 