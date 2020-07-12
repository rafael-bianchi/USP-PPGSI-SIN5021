

import math
from collections import deque

import gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.agents.policy_gradient import Actor_Critic_Agent
from src.agents.sample_efficient import Dyna_Q_Agent
from src.agents.value_based import Q_Learning_Agent

env = gym.make('CartPole-v1')
env.reset()

#%%


episodes = 2000
env = gym.make('CartPole-v1')
agent = Actor_Critic_Agent(env)
reward_hist = []

for episode in range(episodes):
    observation = agent.env.reset()

    for step in range(500):
        state = observation.reshape(-1, 4)
        action = agent.act(state)

        observation_next, reward, done, _ = agent.env.step(action)
        state_next = observation_next.reshape(-1, 4)
        if done and step < 499:
            reward = -1e-5
        loss1, loss2 = agent.train(state, action, reward, state_next, done)

        observation = state_next[0]

        if done:
            reward_hist.append(step+1)
            if episode % 50 == 0:
                print('Episode: {}/{} | Score: {}'.format(episode, episodes, step+1))
            break
# Num	Observation	    Min	    Max
# 0     Cart Position	-2.4    2.4
# 1	    Cart Velocity	-Inf    Inf
# 2	    Pole Angle	    ~-41.8° ~41.8°
# 3	    Pole Velocity At Tip    -Inf	Inf

#%%
# discr_vector = (1,3,16,20,)   # Resolution degrees: How many discrete states per variable. Play with this parameter!

# class Discretizer ():
#     """ mins: vector with minimim values allowed for each variable
#         maxs: vector with maximum values allowed for each variable
#     """
#     def __init__(self, vector_discr, mins, maxs):
#         self.mins=mins
#         self.maxs=maxs
        
#     def Discretize(self, obs):
#         ratios = [(obs[i] + abs(self.mins[i])) / (self.maxs[i] - self.mins[i]) for i in range(len(obs))]
#         new_obs = [int(round((discr_vector[i] - 1) * ratios[i])) for i in range(len(obs))]
#         new_obs = [min(discr_vector[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
#         return tuple(new_obs)

# # Create the discretizer with maxs and mins from the enviroment
# # Another approach. Try a lot of random actions and find maximum and minimum for each variable empirically
# # This approach also has some problems, because some states are found with very low probability.
# t=0
# tsteps=0
# treward=0

# lO=np.zeros((100000,4))
# for nexp in range(10000):   # Let's do 10 trials
#     done= False  
#     env.reset() 
#     while not done:
#         observation, reward, done, info = env.step(env.action_space.sample()) # take a random action
#         treward = treward + reward
#         tsteps = tsteps + 1
#         lO[nexp]=np.array(observation)        

# maxv=[np.max(lO[:,i]) for i in range(lO.shape[1])]
# minv=[np.min(lO[:,i]) for i in range(lO.shape[1])]


# minv = [env.observation_space.low[0], minv[1], env.observation_space.low[2], minv[3]]
# maxv = [env.observation_space.high[0], maxv[1], env.observation_space.high[2], maxv[3]]
# d = Discretizer(discr_vector, minv, maxv)

# #%%
# def choose_action(state, epsilon):
#     return env.action_space.sample() if (np.random.random() <= epsilon) else np.argmax(Q[state])

# # Set parameters for learning
# alpha = 0.2
# epsilon = 0.1
# gamma = 1

# # Create and initialize Q-value table to 0
# Q = np.zeros(discr_vector + (env.action_space.n,))

# # Just to store the long-term-reward of the last 100 experiments 
# scores = deque(maxlen=100)
# lrews = []
# lr = []

# for episode in range(1,10001):
#     done = False
#     R, reward = 0,0
#     state = d.Discretize(env.reset())
#     while done != True:
#         action = choose_action(state, epsilon) 
#         obs, reward, done, info = env.step(action) 
#         new_state = d.Discretize(obs)
#         Q[state][action] += alpha * (reward + gamma * np.max(Q[new_state]) - Q[state][action]) #3
#         R = gamma * R + reward
#         state = new_state   
#     lr.append(R)
#     scores.append(R)
#     mean_score = np.mean(scores)
#     lrews.append(np.mean(scores))

#     if episode % 100 == 0:
#         print('Episode {} Total Reward: {} Average Reward: {}'.format(episode,R,np.mean(scores)))
#     if mean_score >= 250 and episode >= 100:
#         print('Ran {} episodes. Solved after {} trials ✔'.format(episode, episode - 100))    
#         break


# # %%


# # %%
