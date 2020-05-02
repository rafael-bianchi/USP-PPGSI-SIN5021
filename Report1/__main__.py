# %%
import loader.environment_loader as el
import numpy as np
from algorithms.classical.VI import VI

env = el.EnvLoader('Ambiente1')

epsilon = 0.00001
gamma = 1

vi = VI(env=env, gamma=gamma, epsilon=epsilon)
V, pi = vi.train()

# %%

# %%
import seaborn as sns; 
sns.set()
ax = sns.heatmap(V.reshape(5,25))


# %%
pi = pi.reshape