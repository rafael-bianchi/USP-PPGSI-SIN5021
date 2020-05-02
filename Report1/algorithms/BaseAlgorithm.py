from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    def __init__(self, env, gamma, epsilon, **kwargs):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon

    @abstractmethod
    def train(self):
        pass
