import numpy as np
from ..BaseAlgorithm import BaseAlgorithm

class VI(BaseAlgorithm):
    '''Implementation of the Value iteration algorithm
    '''
    def train(self):
        '''Trains the model and returns the Value table and the policy.

        Returns:
            V(array1):The string which gets reversed.
            pi(array2): The policy.   
        '''

        V = np.zeros((self.env.S));

        res = float("inf")



        Q = np.zeros((self.env.S, len(self.env.A)))

        residuos = [];

        while res > self.epsilon:
            for action in self.env.A:
                a = self.env.getActIdx(action)
                Q[:, a] = self.env.R[:, a] +  self.gamma * self.env.T[:,:,a].dot(V)  

            V_old = V;
            pi = np.argmin(Q, axis=1)
            V = np.amin(Q, axis=1)
            res = max(abs(V_old-V));
            residuos.append(res)
        
        return V, pi