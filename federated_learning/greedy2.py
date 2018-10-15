from federated_learning_env import FederatedLearningEnv
import numpy as np
from mobile import Mobile
import xlwt
import math

env = FederatedLearningEnv()
env.reset()
nb_steps = 3000000
version = '2.0'

step = 0
episode = 0

# open workbook to store result
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Greedy')

episode_step = np.int16(0)
episode_reward = np.float32(0)
env.reset()

while (step < nb_steps):
    data_required1 = Mobile.MAX_DATA
    data_required2 = Mobile.MAX_DATA
    data_required3 = Mobile.MAX_DATA
    if env.MB1.CPU_shared != 0 and env.MB1.energy != 0:
        energy_required1 = int(math.floor((Mobile.TAU * Mobile.CPU_CYCLE_PER_UNIT * data_required1 * math.pow(
            env.MB1.CPU_shared * Mobile.CPU_UNIT, 2)) / Mobile.ENERGY_OF_UNIT))
        energy_required1 = min(energy_required1, env.MB1.energy)
    else:
        energy_required1 = 0
    if env.MB2.CPU_shared != 0 and env.MB2.energy != 0:
        energy_required2 = min(int(math.floor((Mobile.TAU * Mobile.CPU_CYCLE_PER_UNIT * data_required2 * math.pow(
            env.MB2.CPU_shared * Mobile.CPU_UNIT, 2)) / Mobile.ENERGY_OF_UNIT)), env.MB2.energy)
    else:
        energy_required2 = 0
    if env.MB3.CPU_shared != 0 and env.MB3.energy != 0:
        energy_required3 = min(int(math.floor((Mobile.TAU * Mobile.CPU_CYCLE_PER_UNIT * data_required3 * math.pow(
            env.MB3.CPU_shared * Mobile.CPU_UNIT, 2)) / Mobile.ENERGY_OF_UNIT)), env.MB3.energy)
    else:
        energy_required3 = 0

    action = tuple([data_required1, energy_required1, data_required2, energy_required2, data_required3, energy_required3])
    observation, reward, done, info = env.step(action)

    episode_reward += reward
    episode_step += 1
    step += 1

    if done:
        sheet.write(episode + 1, 0, str(episode))
        sheet.write(episode + 1, 1, str(episode_reward[0]))
        sheet.write(episode + 1, 2, str(episode_reward[1]))
        sheet.write(episode + 1, 3, str(episode_reward[2]))
        sheet.write(episode + 1, 4, str(episode_reward[3]))
        print("Step:" + str(step) + ",Episode:" + str(episode) + ",Episode steps:" + str(episode_step)
              + ",Reward:" + str(episode_reward))
        episode += 1
        episode_step = np.int16(0)
        episode_reward = np.float32(0)
        env.reset()

file_name = 'greedy_v' + version + '.xls'
workbook.save('../results/' + file_name)