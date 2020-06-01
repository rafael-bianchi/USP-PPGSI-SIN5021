import numpy as np
from ..BaseAlgorithm import BaseAlgorithm
import timeit


class VI(BaseAlgorithm):
    '''Implementation of the Value iteration algorithm
    '''
    def search(self, t_start, timeout):
        '''Trains the model and returns the policy and Value table.

        Returns:
            pi(array1): The policy.   
            V(array2):The string which gets reversed.
        '''

        V = np.zeros((self.env.S));

        res = float("inf")

        Q = np.zeros((self.env.S, len(self.env.A)))

        residuos = [];

        self.iterations = 0

        while res > self.epsilon:
            now = timeit.default_timer()
            elapsed = now - t_start
            if elapsed / 60 > timeout:
                raise TimeoutError

            for action in self.env.A:
                a = self.env.getActIdx(action)
                Q[:, a] = self.env.R[:, a] +  self.gamma * self.env.T[:,:,a].dot(V)  

            V_old = V;
            pi = np.argmin(Q, axis=1)
            V = np.amin(Q, axis=1)
            res = max(abs(V_old-V));
            residuos.append(res)
            self.iterations += 1
        
        return pi, V