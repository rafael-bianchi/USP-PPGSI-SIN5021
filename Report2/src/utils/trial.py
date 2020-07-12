
from collections import deque

import numpy as np

from ..agents.sample_efficient import Dyna_Q_Agent


class Trial:
    
    def __init__(self, env, agent, episodes, scores : deque, lrews : list):
        
        # Just to store the long-term-reward of the last 100 experiments 
        self.scores = scores
        self.lrews = lrews

        self.env = env
        self.agent = agent
        self.episodes = episodes
        
    def interact(self):
        
        for episode in range(1, self.episodes+1):
            state = self.env.reset()
            R = 0
            done = False
            R, reward = 0,0

            for step in range(self.env.spec.max_episode_steps):
                action = self.agent.select_action(state)

                next_state, reward, done, info = self.env.step(action)

                self.agent.update(state, action, reward, next_state)
                
                if isinstance(self.agent, Dyna_Q_Agent):
                    self.agent.update_model(state, action, reward, next_state)                   

                state = next_state
                R += reward

                if done:
                    break
            
            self.scores.append(R)
            self.lrews.append(np.mean(self.scores))