from collections import defaultdict
import numpy as np

class Q_Learning_Agent:
    def __init__(self, alpha, alpha_decay, epsilon, epsilon_decay, gamma, n_actions):
        
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.Qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.possible_actions = list(range(n_actions))
        self.epsilon_decay = epsilon_decay
        self.alpha_decay = alpha_decay
        
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

        return chosen_action