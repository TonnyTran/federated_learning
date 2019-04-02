import numpy as np
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy, MaxBoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from federated_learning_env import FederatedLearningEnv
from mobile import Mobile

class FederatedLearningProcessor(Processor):
    def process_action(self, action):
        energy_required3 = action % (Mobile.MAX_ENERGY + 1)
        action = action / (Mobile.MAX_ENERGY + 1)
        data_required3 = action % (Mobile.MAX_DATA + 1)
        action = action / (Mobile.MAX_DATA + 1)

        energy_required2 = action % (Mobile.MAX_ENERGY + 1)
        action = action / (Mobile.MAX_ENERGY + 1)
        data_required2 = action % (Mobile.MAX_DATA + 1)
        action = action / (Mobile.MAX_DATA + 1)

        energy_required1 = action % (Mobile.MAX_ENERGY + 1)
        action = action / (Mobile.MAX_ENERGY + 1)
        data_required1 = action

        return tuple([data_required1, energy_required1, data_required2, energy_required2, data_required3, energy_required3])

ENV_NAME = 'Federated_Learning'

# Get the environment and extract the number of actions.
env = FederatedLearningEnv()
np.random.seed(123)
# env.seed(123)
nb_actions = env.nb_actions

# Next, we build a very simple model.

model = Sequential()
model.add(Flatten(input_shape=(1, env.state_size)))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(nb_actions, activation='linear'))

print(model.summary())

# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
policy = EpsGreedyQPolicy(eps=0.05)

version = "3.2"
nb_steps = 1500000
nb_max_episode_steps = None
anneal_steps = 800000
processor = FederatedLearningProcessor()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, processor=processor, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy, vary_eps=True, anneal_steps=anneal_steps)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
dqn.fit(env, nb_steps=nb_steps, visualize=True, verbose=2, log_interval=1000, nb_max_episode_steps=nb_max_episode_steps, version=version)

# After training is done, we save the final weights.
dqn.save_weights('../save_weight/dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=0, visualize=True, nb_max_episode_steps=nb_max_episode_steps)
