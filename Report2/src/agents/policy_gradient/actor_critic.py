import numpy as np
import keras.backend as K
import keras.losses
import keras.layers as layers
from keras.models import Model
from keras.optimizers import Adam
from keras.initializers import glorot_uniform
from collections import defaultdict
import matplotlib.pyplot as plt


class Actor_Critic_Agent():
    def __init__(self, env):
        self.env = env
        self.gamma = 0.99
        self.actor_lr = 0.001
        self.critic_lr = 0.001 #0.01
        self.build_actor()
        self.build_critic()


    def build_actor(self):
        inputs = layers.Input(shape=(4,))
        h1 = layers.Dense(32, activation='relu', kernel_initializer='ones')(inputs)
        # h2 = layers.Dense(20, activation='relu', kernel_initializer='ones')(h1)
        d1 = layers.Dropout(0.6, input_shape=(32,))(h1)
        out = layers.Dense(1, activation='sigmoid', kernel_initializer='ones')(d1)
        self.actor = Model(inputs=inputs, outputs=out)

        def _actor_loss(y_true, y_pred):
            action_pred = y_pred
            action_true, td_error = y_true[:, 0], y_true[:, 1]
            action_true = K.reshape(action_true, (-1, 1))
            loss = K.binary_crossentropy(action_true, action_pred)
            return loss * K.flatten(td_error)

        self.actor.compile(loss=_actor_loss, optimizer=Adam(lr=self.actor_lr))


    def build_critic(self):
        inputs = layers.Input(shape=(4,))
        h1 = layers.Dense(16, activation='relu')(inputs)
        h2 = layers.Dense(16, activation='relu')(h1)
        out = layers.Dense(1, activation='linear')(h2)
        self.critic = Model(inputs=inputs, outputs=out)
        self.critic.compile(loss='mse', optimizer=Adam(lr=self.critic_lr))


    def discount_reward(self, next_states, reward, done):
        q = self.critic.predict(next_states)[0][0]
        target = reward
        if not done:
            target = reward + self.gamma * q
        
        return target


    def act(self, state):
        prob = self.actor.predict(state)[0][0]
        action = np.random.choice(np.array(range(2)), p=[1 - prob, prob])
        return action


    def train(self, state, action, reward, state_next, done):
        target = self.discount_reward(state_next, reward, done)
        y = np.array([target])

        td_error = target - self.critic.predict(state)[0][0]
        loss1 = self.critic.train_on_batch(state, y)

        y = np.array([[action, td_error]])
        loss2 = self.actor.train_on_batch(state, y)
        return loss1, loss2
