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

#%%
df = pd.DataFrame(l100rew).melt()
ax = sns.lineplot(x="variable", y="value", data=df)
ax.set_title('Q-Learning')
ax.set(xlabel='Episódios', ylabel='Recompensa(avg)')
plt.show()

#%%
n_exp = 10
episodes = 2000
l100rew=[]
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
ax = sns.lineplot(x="variable", y="value", data=df)
ax.set_title('Dyna-Q')
ax.set(xlabel='Episódios', ylabel='Recompensa(avg)')
plt.show()

#%%
# Just to store the long-term-reward of the last 100 experiments 
n_exp = 10
episodes = 2000
l100rew=[]
for ex in trange(n_exp):
    scores = deque(maxlen=100)
    lrews = []
    env = gym.make("CartPole-v0")
    agent = Actor_Critic_Agent(env)
    for episode in trange(episodes):
        observation = agent.env.reset()

        R = 0
        done = False
        R, reward = 0,0

        for step in range(env.spec.max_episode_steps):
            state = observation.reshape(-1, 4)
            action = agent.act(state)

            observation_next, reward, done, _ = agent.env.step(action)
            state_next = observation_next.reshape(-1, 4)
            if done and step < 199:
                reward = -1e-5
            loss1, loss2 = agent.train(state, action, reward, state_next, done)

            observation = state_next[0]
            R += reward

            if done:
                break
                        
        scores.append(R)
        lrews.append(np.mean(scores))

df = pd.DataFrame(l100rew).melt()
df.to_csv('actor_critic.csv')

#%%
df = pd.read_csv('actor_critic.csv')
# df = pd.DataFrame(l100rew).melt()
ax = sns.lineplot(x="variable", y="value", data=df)
ax.set_title('Actor-Critic')
ax.set(xlabel='Episódios', ylabel='Recompensa(avg)')
plt.show()

# %%
