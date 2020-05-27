#%%
import loader.environment_loader as el
import numpy as np
from algorithms.classical.VI import VI

env = el.EnvLoader('Ambiente1')

# epsilon = 0.000000000000001
# gamma = 1

# vi = VI(env=env, gamma=gamma, epsilon=epsilon)
# V, pi = vi.search()

# %%

# %%
import loader.environment_loader as el
import numpy as np
from algorithms.efficient.LAOStar import LAOStar

env = el.EnvLoader('Ambiente1')

epsilon = 0.000000000000001
gamma = 1

laoStar = LAOStar(env=env, s0 = 0)
g = laoStar.search()

# %%
pi = pi.reshape