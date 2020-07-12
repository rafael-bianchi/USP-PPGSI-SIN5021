from collections import defaultdict
import random
import numpy as np

class Dyna_Q_Agent:
    def __init__(self, alpha, alpha_decay, epsilon, epsilon_decay, gamma, planning_steps, n_actions):
        
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.Qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.model = defaultdict()
        self.possible_actions = list(range(n_actions))
        self.epsilon_decay = epsilon_decay
        self.alpha_decay = alpha_decay
        self.planning_steps = planning_steps
        
    def get_value_of_state(self, s):
        
        v = -1 * np.inf
        
        for ac in self.possible_actions:
            ac_val = self.Qvalues[s][ac]
            if ac_val > v:
                v = ac_val

        return v
        
    def update(self, s, a, r, s_prime):
        
        q_sa = self.Qvalues[s][a]
        self.Qvalues[s][a] = q_sa + self.alpha * (r + self.gamma * self.get_value_of_state(s_prime) - q_sa)
        
        #update the model
        
    def update_model(self, s, a, r, s_prime):
        self.model[(s,a)] = (r, s_prime)
        
    def best_action(self, s):
        
        s_action = None
        best_q = -1 * np.inf
        
        for ac in self.possible_actions:
            ac_val = self.Qvalues[s][ac]
            if ac_val > best_q:
                best_q = ac_val
                s_action = ac
                
        return s_action
    
    def select_action(self, state):
        
        toss = np.random.uniform()
        
        if toss < self.epsilon:
            chosen_action = np.random.choice(self.possible_actions)
        else:
            chosen_action = self.best_action(state)
            
            
        self.epsilon = self.epsilon * self.epsilon_decay
        self.alpha = self.alpha * self.alpha_decay
        
        if len(self.model.keys()) > self.planning_steps:
            #Do the planning steps:
            imaginary_samples = random.sample(list(self.model.keys()),self.planning_steps)
            for i in range(self.planning_steps):
                imag_s, imag_a = imaginary_samples[i]
                imag_r, imag_s_prime = self.model[imaginary_samples[i]]
                
                self.update(imag_s, imag_a, imag_r, imag_s_prime)
            

        return chosen_action