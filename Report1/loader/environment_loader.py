import pandas as pd
import sys
import numpy as np


class EnvLoader():
    """Class used to load environments."""
    
    # self.T = None
    # self.R = None

    def __init__(self, envName):
        if type(envName).__name__ != 'str' or envName.__eq__(''):
            raise ValueError('Invalid environment.')

        base_path = f'{sys.path[0]}/assets/data/{envName}/'

        actions = ['Norte', 'Sul', 'Leste', 'Oeste']

        cost = pd.read_csv(f'{base_path}Cost.txt', header=None)
        map_size = len(cost)

        self.T = np.zeros((map_size, map_size, len(actions)))
        self.R = np.ones((map_size))

        #%% Loading Transition Matrix
        dlmtr = '   '
        for action in actions:
            st_st_act_prob = pd.read_csv(f'{base_path}Action_{action}.txt', delimiter=dlmtr,
                                         header=None).astype({0: 'int32', 1: 'int32'})

            action_index = actions.index(action)
            self.T[st_st_act_prob[0]-1, st_st_act_prob[1] -
                1, action_index] = st_st_act_prob[2]
        
        #%% Loading cost values
        self.R = cost.to_numpy()
