#%%
import math
from collections import deque

import gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tqdm
from tqdm import trange

from src.agents.policy_gradient import Actor_Critic_Agent
from src.agents.sample_efficient import Dyna_Q_Agent
from src.agents.value_based import Q_Learning_Agent
from src.utils import Binarizer, Trial

# Num	Observation	    Min	    Max
# 0     Cart Position	-2.4    2.4
# 1	    Cart Velocity	-Inf    Inf
# 2	    Pole Angle	    ~-41.8° ~41.8°
# 3	    Pole Velocity At Tip    -Inf	Inf

#%%
n_exp = 10
episodes = 2000
l100rew=[]

for ex in trange(n_exp):
    scores = deque(maxlen=100)
    lrews = []
    env = gym.make("CartPole-v0")
    env_b = Binarizer(env)
    agent = Q_Learning_Agent(alpha=0.5, alpha_decay=0.99999, epsilon=0.4, epsilon_decay = 0.99999 ,gamma=0.999, n_actions= env_b.action_space.n)
    
    T = Trial(env=env_b, agent=agent, episodes=episodes, scores=scores, lrews = lrews)    
    T.interact()
    
    l100rew.append(lrews)

df = pd.DataFrame(l100rew).melt()
sns.lineplot(x="variable", y="value", data=df)

#%%
for ex in trange(n_exp):
    scores = deque(maxlen=100)
    lrews = []
    env = gym.make("CartPole-v0")
    env_b = Binarizer(env)
    agent = Dyna_Q_Agent(alpha=0.5, alpha_decay=0.9999 , epsilon=0.4, epsilon_decay = 0.99999 ,gamma=0.999, planning_steps=20, n_actions= env.action_space.n)
    
    T = Trial(env=env_b, agent=agent, episodes=episodes, scores=scores, lrews = lrews)    
    T.interact()
    
    l100rew.append(lrews)

df = pd.DataFrame(l100rew).melt()
sns.lineplot(x="variable", y="value", data=df)
#%%
# Just to store the long-term-reward of the last 100 experiments 
scores = deque(maxlen=100)
lrews = []
lr = []

episodes = 2000
env_b = gym.make('CartPole-v0')
agent = Actor_Critic_Agent(env_b)
reward_hist = []

for episode in range(episodes):
    observation = agent.env.reset()

    for step in range(500):
        state = observation.reshape(-1, 4)
        action = agent.act(state)

        observation_next, reward, done, _ = agent.env.step(action)
        state_next = observation_next.reshape(-1, 4)
        if done and step < 199:
            reward = -1e-5
        loss1, loss2 = agent.train(state, action, reward, state_next, done)

        observation = state_next[0]

        if done:
            reward_hist.append(step+1)
            if episode % 50 == 0:
                print('Episode: {}/{} | Score: {}'.format(episode, episodes, step+1))
            break
