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
        V = np.ones(self.env.S) * np.nan
        V[self.s0] = self.heuristic(self.s0, self.env.G[0])
        F = {self.s0}
        I = set()
        G_hat_s0 = I.union(F)
        G_hat_vl_s0 = { self.s0 }
        pi = None


        # while F ∩ Ĝs0 Vl has some non-goal states do
        while any([itsc != self.env.G[0] for itsc in F.intersection(G_hat_vl_s0)]): 
            # Expand a fringe state of the best partial policy
            intersec = [itsc for itsc in F.intersection(G_hat_vl_s0) if itsc != self.env.G[0]]
            s = np.argmin(V[intersec], axis=0) #s ← some non-goal state in F ∩ Ĝs0 V
            V[s] = self.heuristic(s, self.env.G[0])
            F.remove(s) #  F ← F \ {s}
            children = self.expand_s(s)
            F = F.union(children.difference(I)) #  F ← F ∪ {all successors s  of s under all actions, s  ∈ / I }
            I = I.union(s)  # I ← I ∪ {s}
            G_hat_s0 = I.union(F) # Ĝs0 ← {nodes: I ∪ F, hyperedges: all actions in all states of I }
            # Update state values and mark greedy actions

    def heuristic(self, s_, g_) -> int:
        ini_x = self.env.states_X_Y[s_][0]
        ini_y = self.env.states_X_Y[s_][1]
        
        goal_x = self.env.states_X_Y[g_][0]
        goal_y = self.env.states_X_Y[g_][1]

        return abs(ini_x - goal_x) + abs(ini_y - goal_y)


    def expand_s(self, s) -> set:
        possible_states = np.any(self.env.T[s] > 0, axis=1)
        #return the indexes of s successors
        return set(np.where(possible_states)[0]).difference({s})

    # def policy_iteration(self, mdp):
    #     """
    #     Solve an MDP by policy iteration [Fig. 17.7]
        
    #     mdp: an MDP object
        
    #     returns: best policy, dictionary mapping state to action
    #     """    
        
    #     U = dict([(s, 0) for s in mdp.states])
    #     pi = dict([(s, random.choice(mdp.actions(s))) for s in mdp.states])
        
    #     while True:
    #         U = policy_evaluation(pi, U, mdp)
    #         unchanged = True
    #         for s in mdp.states:
    #             a = argmax(mdp.actions(s), lambda a: expected_utility(a,s,U,mdp))
    #             if a != pi[s]:
    #                 pi[s] = a
    #                 unchanged = False
    #         if unchanged:
    #             return pi
    
    # def policy_evaluation(pi, U, mdp, k=20):
    #     """Return an updated utility mapping U from each state in the MDP to its
    #     utility, using an approximation (modified policy iteration)."""
    #     for i in range(k):
    #         for s in mdp.states:
    #             U[s] = mdp.R(s) + expected_utility(pi[s], s, U, mdp)
    #     return U
