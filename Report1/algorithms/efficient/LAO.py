import math
import numpy as np
import timeit

def getPossibleStates(T, state_from, action):
    return np.where(T[state_from, :, action] > 0)[0]

def LAO(env, s0, gamma, epsilon, t_start, timeout):

    def h(s, g, env):
        ini_x = env.states_X_Y[s][0]
        ini_y = env.states_X_Y[s][1]
        
        goal_x = env.states_X_Y[g][0]
        goal_y = env.states_X_Y[g][1]

        return (abs(ini_x - goal_x) + abs(ini_y - goal_y)) * 2

    pi = [0] * env.S
    V = [0] * env.S 

    F = [False] * env.S
    F[s0] = True
    G = set([s0])

    while True:
        now = timeit.default_timer()
        elapsed = now - t_start

        if (elapsed / 60 > timeout):
            raise TimeoutError

        expanded = None
        bfs = [s0]
        visited = [False] * env.S
        while bfs:
            s = bfs.pop(0)
            if F[s]:
                expanded = s
                break
            else:
                for t in getPossibleStates(env.T, s, pi[s]):
                    if not visited[t]:
                        bfs.append(t)
                        visited[t] = True

        if expanded == None:
            break

        F[expanded] = False

        for a in env.A:
            action_index = env.A.index(a)
            for t in getPossibleStates(env.T, s, action_index):
                if t not in G:
                    G.add(t)
                    F[t] = True
                    if t == env.G[0]:
                        V[t] = 0
                    else:
                        V[t] = h(t, env.G[0], env)

        def recursion(s,visited,Z):
            visited[s] = True

            found = False

            if s == expanded:
                Z.add(s)
                return True

            for p_state in getPossibleStates(env.T, s, pi[s]):
                if p_state in G and not F[p_state] and not visited[p_state]:
                    if not found:
                        found = recursion(p_state,visited,Z)
                    else:
                        recursion(p_state,visited,Z)

            if found:
                Z.add(s)
                return True
            return False

        Z = set()
        for start in G:
            if not F[start]:
                visited = [False] * env.S
                recursion(start, visited, Z)

        (V, pi) = perform_value_iteration(env, Z, V, pi, gamma, epsilon)  # *

    return V, pi


def perform_value_iteration(env, Z, values, pi, gamma=0.999, epsilon=0.00001):
    residual = float("Inf")
    v_current = values.copy()
    v = v_current.copy()
    while residual > epsilon:
        for s in Z:
            minimum = float('Inf')
            best_action = 0
            for a in env.A:
                action_index = env.A.index(a)
                summ = env.cost[s]
                for t in getPossibleStates(env.T, s, action_index):
                    summ += env.T[s, t, action_index] * gamma * v_current[t]
                if summ < minimum:
                    minimum = summ
                    best_action = action_index

            v[s] = minimum
            pi[s] = best_action

        maxi = 0
        for i in range(len(v)):
            summ = abs(v[i] - v_current[i])
            if summ > maxi:
                maxi = summ
        residual = maxi
        v_current = v.copy()

    return v, pi