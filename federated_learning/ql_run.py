from __future__ import print_function
from collections import deque
from rl.agents.tabular_q_learner import QLearner
from federated_learning_env import FederatedLearningEnv
import xlwt
from mobile import Mobile
import numpy as np

ENV_NAME = 'Federated_Learning'

# Get the environment and extract the number of actions.
env = FederatedLearningEnv()

def digitalizeState(observation, env=None):
    state = 0
    for index in range(0, len(observation)):
        state += observation[len(observation) - 1 - index] * (Mobile.MAX_ENERGY ** index)
    return state

def digitalizeAction(action):
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

state_dim = (Mobile.MAX_CPU + 1) ** env.nb_MB * (Mobile.MAX_ENERGY + 1) ** env.nb_MB
num_actions = env.nb_actions


nb_steps = 3000000
anneal_steps = 2500000
# MAX_STEPS = 200
# MAX_EPISODES = nb_steps / MAX_STEPS

version = '4.1'
q_learner = QLearner(state_dim, num_actions, anneal_steps=anneal_steps, e_vary=True)

# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('QL')

episode_history = deque(maxlen=100)
i_episode = 0
i_step = 0
while i_step < nb_steps:
    # initialize
    observation = env.reset()
    state = digitalizeState(observation, env)
    action = q_learner.initializeState(state)
    dAction = digitalizeAction(action)
    episode_reward = np.zeros(7, dtype=np.float32)
    done = False

    while not done:
        env.render()
        observation, reward, done, _ = env.step(dAction)

        state = digitalizeState(observation, env)

        episode_reward += reward
        action = q_learner.updateModel(state, reward[0])
        dAction = digitalizeAction(action)
        training_data = episode_reward[1]
        if training_data > FederatedLearningEnv.DATA_LIMIT:
            done = True
        i_step += 1


    episode_history.append(episode_reward[0])
    mean_rewards = np.mean(episode_history)

    sheet.write(i_episode + 1, 0, str(i_episode))
    sheet.write(i_episode + 1, 1, str(episode_reward[0]))
    sheet.write(i_episode + 1, 2, str(episode_reward[1]))
    sheet.write(i_episode + 1, 3, str(episode_reward[2]))
    sheet.write(i_episode + 1, 4, str(episode_reward[3]))

    print("Episode {}".format(i_episode))
    print("Reward for this episode: {}".format(episode_reward[0]))
    print("Average reward for last 100 episodes: {:.2f}".format(mean_rewards))
    i_episode += 1

file_name = 'result_v' + version + '_QL.xls'
workbook.save('../results/' + file_name)