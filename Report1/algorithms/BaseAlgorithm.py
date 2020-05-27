from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    def __init__(self, env, gamma, epsilon, **kwargs):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon
        self.iterations = 0

    @abstractmethod
    def search(self):
        pass
