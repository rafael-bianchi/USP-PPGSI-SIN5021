import numpy as np
from gym import ObservationWrapper

class Binarizer(ObservationWrapper):

    def observation(self, state):

        # state = <round state to some amount digits.>
        # hint: you can do that with round(x,n_digits)
        # you will need to pick a different n_digits for each dimension
        state[0] = np.round(state[0], 0)
        state[1] = np.round(state[1], 0)
        state[2] = np.round(state[2], 2)
        state[3] = np.round(state[3], 1)

        return tuple(state)