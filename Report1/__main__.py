# %%
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import timeit
from datetime import datetime
from algorithms.efficient.LAO import LAO
import loader.environment_loader as el
import numpy as np
from algorithms.classical.VI import VI

timeout = 1

param = {}


# %%
for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    env = el.EnvLoader(e_name)
    param[e_name] = {}
    for gamma in [1, 0.99, 0.75, 0.5, 0.25, 0]:
        param[e_name][gamma] = {}
        for epsilon in [0.000000000000001, 0.00000001, 0.001, 0.1, 1, 3]:
            param[e_name][gamma][epsilon] = {'vi': None, 'lao': None}

            try:
                start = timeit.default_timer()
                V, pi = LAO(env, 0, gamma, epsilon, start, timeout)
                stop = timeit.default_timer()
                execution_time = stop - start
                param[e_name][gamma][epsilon]['lao'] = {
                    'V': V, 'pi': pi, 'execution_time': execution_time}
                print(
                    f'LAO: Env {e_name} gamma {gamma} and epsilon {epsilon} = execution_time: {execution_time}')
            except TimeoutError:
                param[e_name][gamma][epsilon]['lao'] = {
                    'V': None, 'pi': None, 'execution_time': None}
                print(
                    f'LAO: Env {e_name} Error with gamma {gamma} and epsilon {epsilon}')

            vi = VI(env=env, gamma=gamma, epsilon=epsilon)

            try:
                start = timeit.default_timer()
                V, pi = vi.search(start, timeout)
                stop = timeit.default_timer()
                execution_time = stop - start
                param[e_name][gamma][epsilon]['vi'] = {
                    'V': V, 'pi': pi, 'execution_time': execution_time}
                print(
                    f'VI: Env {e_name} gamma {gamma} and epsilon {epsilon} = execution_time: {execution_time}')
            except TimeoutError:
                param[e_name][gamma][epsilon]['vi'] = {
                    'V': None, 'pi': None, 'execution_time': None}
                print(
                    f'VI: Env {e_name} Error with gamma {gamma} and epsilon {epsilon}')

    # %%
sns.set()


# %%
col_names = ['Algorithm', 'Gamma', 'Epsilon', 'Ambiente', 'ExecutionTime']

df = pd.DataFrame(columns=col_names)

# %%
pd.DataFrame()
for alg in ['lao', 'vi']:
    for amb in param:
        for g in param[amb]:
            for e in param[amb][g]:
                pi = param[amb][g][e][alg]['pi']

                first_move_east = None
                if pi is not None:
                    first_move_east = 0
                    for p in range(len(pi)):
                        if (pi[p] == 0):
                            break
                        first_move_east += 1

                row = pd.DataFrame({'Algorithm': [alg], 'Gamma': [g], 'Epsilon': [e], 'Ambiente': [amb], 'ExecutionTime': [
                                   param[amb][g][e][alg]['execution_time']], 'FirstEastMove': [first_move_east]})
                df = df.append(row)

# %%
for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    for alg in ['lao', 'vi']:
        p = df[(df.Algorithm == alg) & (df.Ambiente == e_name)]
        p = p.replace([np.nan], np.inf)
        p = p.pivot('Gamma', 'Epsilon', 'ExecutionTime')
        f, ax = plt.subplots(figsize=(9, 6))
        n_display = 'LAO*' if alg == 'lao' else 'Iteração de Valor'
        ax.set_title(f'{e_name} - {n_display}')
        svm = sns.heatmap(p, annot=True, linewidths=.5, ax=ax)
        figure = svm.get_figure()
        figure.savefig(f'assets/images/{alg}_{e_name}.png', dpi=400)

# %%
for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    for alg in ['lao', 'vi']:
        p = df[(df.Algorithm == alg) & (df.Ambiente == e_name) & (df.pi)]
        p = p.replace([np.nan], np.inf)
        p = p.pivot('Gamma', 'Epsilon', 'ExecutionTime')
        f, ax = plt.subplots(figsize=(9, 6))
        n_display = 'LAO*' if alg == 'lao' else 'Iteração de Valor'
        ax.set_title(f'{e_name} - {n_display}')
        svm = sns.heatmap(p, annot=True, linewidths=.5, ax=ax)
        figure = svm.get_figure()
        figure.savefig(f'assets/images/{alg}_{e_name}.png', dpi=400)

# %%
for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    for alg in ['lao', 'vi']:
        p = df[(df.Algorithm == alg) & (df.Ambiente == e_name)
                & (df.FirstEastMove != np.nan)]
        p = p.replace([np.nan], np.inf)
        p = p.pivot('Gamma', 'Epsilon', 'FirstEastMove')
        f, ax = plt.subplots(figsize=(9, 6))
        n_display = 'LAO*' if alg == 'lao' else 'Iteração de Valor'
        ax.set_title(f'Primeiro movimento à leste - {e_name} - {n_display}')
        svm = sns.heatmap(p, annot=True, fmt="g", linewidths=.5, ax=ax)
        figure = svm.get_figure()
        figure.savefig(
            f'assets/images/FirstEastMove{alg}_{e_name}.png', dpi=400)

# %%
timeout = 3
params_lao = {}
for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    env = el.EnvLoader(e_name)
    params_lao[e_name] = {}

    start_states = set([s for s in range(0, env.S)]).difference({env.G[0]})
    start_states = start_states.difference({0})
    start_states = random.choices(list(start_states), k=10)

    for start_s in start_states:
        params_lao[e_name][start_s] = {}
        try:
            start = timeit.default_timer()
            V, pi = LAO(env, start_s, 0.99, 0.00001, start, timeout)
            stop = timeit.default_timer()
            execution_time = stop - start
            ini_x = env.states_X_Y[start_s][0]
            ini_y = env.states_X_Y[start_s][1]

            goal_x = env.states_X_Y[env.G[0]][0]
            goal_y = env.states_X_Y[env.G[0]][1]
            m_distance = abs(ini_x - goal_x) + abs(ini_y - goal_y)
            params_lao[e_name][start_s] = {
                'V': V, 'pi': pi, 'start_s': start_s, 'm_distance': m_distance, 'execution_time': execution_time}
            print(
                f'LAO: Env {e_name} gamma {gamma} and epsilon {epsilon} = execution_time: {execution_time}')
        except TimeoutError:
            params_lao[e_name][start_s] = {
                'V': None, 'pi': None, 'start_s': None, 'm_distance': None, 'execution_time': None}
            print(
                f'LAO: Env {e_name} Error with gamma {gamma} and epsilon {epsilon}')

# %%
import pandas as pd
col_names = ['Ambiente', 'ExecutionTime',
    'start_s', 'm_distance', 'execution_time']

df = pd.DataFrame(columns=col_names)

for e_name in ['Ambiente1', 'Ambiente2', 'Ambiente3']:
    for k in params_lao[e_name].keys():
        pd.DataFrame()

        row = pd.DataFrame({'Ambiente': [e_name]
        , 'ExecutionTime': [params_lao[e_name][k]['execution_time']]
        , 'start_s': [k]
        , 'm_distance':[params_lao[e_name][k]['m_distance']]})
        df = df.append(row)


# %%
df.s_start = df.s_start + 1

# %%
df.drop('execution_time', inplace=True, axis=1)

# %%
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
amb1 = df[df['Ambiente'] == 'Ambiente1']
ax.plot(amb1['m_distance'], amb1['ExecutionTime'])

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

# fig.savefig("test.png")
plt.show()
# %%
