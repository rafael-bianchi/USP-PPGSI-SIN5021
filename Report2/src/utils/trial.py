
from ..agents.sample_efficient import Dyna_Q_Agent

class Trial:
    
    def __init__(self, env, agent, episodes, max_steps):
        
        self.env = env
        self.agent = agent
        self.episodes = episodes
        self.max_steps = max_steps
        self.returns = []
        
    def interact(self):
        
        for j in range(self.episodes):
            obs = self.env.reset()
            treturn = 0

            for i in range(self.max_steps):
                a = self.agent.select_action(obs)

                next_state, r, done, info = self.env.step(a)

                self.agent.update(obs, a, r, next_state)
                
                if isinstance(agent, Dyna_Q_Agent):
                    self.agent.update_model(obs, a, r, next_state)                   

                obs = next_state
                treturn += r

                if done:
                    break
                
            self.returns.append(treturn)
            
        return self.returns
        