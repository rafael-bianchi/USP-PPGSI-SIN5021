import numpy as np
from ..BaseAlgorithm import BaseAlgorithm
import random
from numpy import argmax

class LAOStar(BaseAlgorithm):
    '''Implementation of the LAO* algorithm
    '''
    def __init__(self, env, s0: int, **kwargs):
        self.env = env
        self.s0 = s0

    def search(self):
        pi = np.zeros(self.env.S, dtype=int) 
        V = np.array([self.heuristic(s,self.env.G[0])*2 for s in range(self.env.S)])
        #V[self.s0] = self.heuristic(self.s0, self.env.G[0])
        
        F = {self.s0}
        I = set()
        G_hat_s0 = I.union(F)
        G_hat_vl_s0 = set([self.s0])


        # while F ∩ Ĝs0 Vl has some non-goal states do
        while True: 
            # Expand a fringe state of the best partial policy
            F_G_hat_vl_s0_intersec = [itsc for itsc in F.intersection(G_hat_vl_s0) if itsc != self.env.G[0]]

            # No nodes on the Fringe
            if len(F_G_hat_vl_s0_intersec) == 0:
                break

            #s ← some non-goal state in F ∩ Ĝs0 V
            s = F_G_hat_vl_s0_intersec[np.argmin(V[F_G_hat_vl_s0_intersec], axis=0)]
            
            #  F ← F \ {s}
            F.remove(s) 
            
            #  F ← F ∪ {all successors s  of s under all actions, s  ∈ / I }
            children = self.expand_s(s)
            F = F.union(children.difference(I))

            # I ← I ∪ {s} 
            I = I.union({s})

            # Ĝs0 ← {nodes: I ∪ F, hyperedges: all actions in all states of I }
            G_hat_s0 = I.union(F) 
            
            # Update state values and mark greedy actions
            # Z ← {s and all states in Ĝs0 from which s can be reached via the current greedy policy}
            Z = set()
            for s_ in G_hat_s0.difference(F):
                visited = [False] * self.env.S
                self.create_Z(s_, visited, s, G_hat_s0, F, pi, Z)

            

            (V, pi) = self.z_value_iteration(Z, V, pi, 0.999, 0.000001)  # *
            
            states = [self.s0]
            G_hat_vl_s0 = set()
            while len(set(states).intersection(G_hat_s0)) > 0:
                current_s = states.pop()
                
                G_hat_vl_s0.add(current_s)
                
                if (current_s in F):
                    break

                for state in np.where(self.env.T[current_s,:,pi[current_s]] > 0):
                    states.append(state.item())




    def create_Z(self, start, visited, expanded, G_hat_s0, F, pi,Z):
        visited[start] = True

        found = False

        if start == expanded:
            Z.add(start)
            return True

        for next_state in np.where(self.env.T[start, :, pi[start]] > 0)[0]:
            if next_state in G_hat_s0 and (next_state not in F) and not visited[next_state]:
                if not found:
                    found = self.create_Z(next_state, visited, expanded, G_hat_s0, F, pi,Z)
                else:
                    self.create_Z(next_state, visited, expanded, G_hat_s0, F, pi,Z)

        # for t in start.T[pi[start]]:
        #     s2 = env.S[t['state']-1]
        #     # if s2 is in G and it is not a tip and it was not visited
        #     if s2 in G_hat_s0 and not F[s2.number - 1] and not visited[s2.number - 1]:
        #         if not found:
        #             found = recursion(s2,visited,Z)
        #         else:
        #             recursion(s2,visited,Z)

        if found:
            Z.add(start)
            return True
        return False
    
    def heuristic(self, s_, g_) -> int:
        #return 0

        ini_x = self.env.states_X_Y[s_][0]
        ini_y = self.env.states_X_Y[s_][1]
        
        goal_x = self.env.states_X_Y[g_][0]
        goal_y = self.env.states_X_Y[g_][1]

        return abs(ini_x - goal_x) + abs(ini_y - goal_y)

    def expand_s(self, s) -> set:
        possible_states = np.any(self.env.T[s] > 0, axis=1)
        #return the indexes of s successors
        return set(np.where(possible_states)[0]).difference({s})

    def z_value_iteration(self, Z, V, pi, gamma=0.999, epsilon=0.00001):
        """
        update the values of the state's object and also returns a list with the values of each state
        :param mdp: a MDP object
        :param Z: a set of states that will be updated
        :param values: previous values of each state
        :param best_actions: previous best actions of each state
        :param gamma: used for limit the propagation of infinite values
        :param epsilon: precision measured by the number of zeros on epsilon
        :return: list of values for each state as well as the best actions that gave the minimum values of each state
        """
        if len(Z) == 0:  # whether nothing was passed as Z, we will consider all states in the mdp
            Z = [s for s in range(self.env.S)]

        res = float("Inf")
        
        vk = V.copy()
        vk1 = vk.copy()

        while res > epsilon:
            for s in Z:  # for each state in the mdp
                minimum = float('Inf')
                best_action = 0
                
                nextstate_action = np.where(self.env.T[s,:,:] > 0)
                actions = {}
                nextstate_action = list(zip(nextstate_action[0], nextstate_action[1]))

                for state_action in nextstate_action:
                    a = state_action[1]
                    if a not in actions.keys():
                        actions[a] = []
                    
                    actions[a].append(state_action[0])
                
                for action in actions.keys():
                    summ = self.env.cost[s]

                    for next_state in actions[action]:
                        summ += self.env.T[s,next_state,action] * gamma * vk[next_state]

                    if summ < minimum:
                        minimum = summ
                        best_action = action

                vk1[s] = minimum
                pi[s] = best_action

            maxi = 0
            for i in range(len(vk1)):
                summ = abs(vk1[i] - vk[i])
                if summ > maxi:
                    maxi = summ
            res = maxi
            vk = vk1.copy()

        return vk1, pi