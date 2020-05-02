import pandas as pd
import sys
import numpy as np
import os.path


class EnvLoader():
    """Class used to load environments."""

    # self.T = None
    # self.R = None

    def __init__(self, envName):
        if type(envName).__name__ != 'str' or envName.__eq__(''):
            raise ValueError('Invalid environment.')

        self.envName = envName

        self.envParameters = {
                              'Ambiente1': {"X": 25, "Y": 5},
                              'Ambiente2': {"X": 100, "Y": 20}, 
                              'Ambiente3': {"X": 250, "Y": 50}
                             }
        self.X = self.envParameters[self.envName]['X']
        self.Y = self.envParameters[self.envName]['Y']

        self.states_X_Y = {}

        for y in range(0, self.Y):
            for x in range(0, self.X):
                s = y*self.X + x
                self.states_X_Y[s] = (x,y)

        base_path = f'{sys.path[0]}/assets/data/{envName}/'

        self.A = ['Norte', 'Sul', 'Leste', 'Oeste']

        cost_file = f'{base_path}Cost.txt'
        if not os.path.isfile(cost_file):
            raise OSError(f'File {cost_file} not found.')

        self.cost = pd.read_csv(cost_file, header=None).to_numpy()
        self.cost = self.cost.reshape(self.cost.shape[0],)

        self.S = len(self.cost)

        self.T = np.zeros((self.S, self.S, len(self.A)))
        self.R = np.repeat(self.cost, 4, axis=0).reshape(self.cost.shape[0],len(self.A))

        # %% Loading Transition Matrix
        dlmtr = '   '
        for action in self.A:
            file = f'{base_path}Action_{action}.txt'

            if not os.path.isfile(file):
                raise OSError(f'File {file} not found.')

            st_st_act_prob = pd.read_csv(file, engine='python', delimiter=dlmtr,
                                         header=None).astype({0: 'int32', 1: 'int32'})

            action_index = self.A.index(action)
            self.T[st_st_act_prob[0]-1, st_st_act_prob[1] -
                   1, action_index] = st_st_act_prob[2]

    def getActIdx(self, action):
        return self.A.index(action)