import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from action_space import ActionSpace
from state_space import StateSpace
from gym.spaces import Discrete
from mobile import Mobile

class FederatedLearningEnv(gym.Env):
    TIME_LIMIT = 10000
    DATA_LIMIT = 1500
    def __init__(self):

        # System parameters
        self.nb_MB = 3
        self.state_size = 2 * self.nb_MB
        self.nb_actions = (Mobile.MAX_DATA + 1) ** self.nb_MB * (Mobile.MAX_ENERGY + 1) ** self.nb_MB

        self.action_space = ActionSpace((Discrete(Mobile.MAX_DATA + 1), Discrete(Mobile.MAX_ENERGY + 1),
                                         Discrete(Mobile.MAX_DATA + 1), Discrete(Mobile.MAX_ENERGY + 1),
                                         Discrete(Mobile.MAX_DATA + 1), Discrete(Mobile.MAX_ENERGY + 1)
                                         ))

        self.observation_space = StateSpace((Discrete(Mobile.MAX_CPU), Discrete(Mobile.MAX_ENERGY),
                                             Discrete(Mobile.MAX_CPU), Discrete(Mobile.MAX_ENERGY),
                                             Discrete(Mobile.MAX_CPU), Discrete(Mobile.MAX_ENERGY)))

        # initialize Second Transmitters
        self.MB1 = Mobile()
        self.MB2 = Mobile()
        self.MB3 = Mobile()

        self.max_data = self.nb_MB * Mobile.MAX_DATA
        self.max_energy = self.nb_MB * Mobile.MAX_ENERGY
        self.max_latency = Mobile.MAX_LATENCY

        self.training_time = 0
        self.training_data = 0

        self.viewer = None
        self.state = None
        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        data_required1 = action[0]
        energy_required1 = action[1]
        data_required2 = action[2]
        energy_required2 = action[3]
        data_required3 = action[4]
        energy_required3 = action[5]

        data1, latency1, energy_consumption1, fault1 = self.MB1.update(data_required1, energy_required1)
        data2, latency2, energy_consumption2, fault2 = self.MB2.update(data_required2, energy_required2)
        data3, latency3, energy_consumption3, fault3 = self.MB3.update(data_required3, energy_required3)

        data = data1 + data2 + data3
        latency = max(latency1, latency2, latency3)
        energy_consumption = energy_consumption1 + energy_consumption2 + energy_consumption3
        fault = fault1 + fault2 + fault3

        state = [self.MB1.CPU_shared, self.MB1.energy, self.MB2.CPU_shared, self.MB2.energy, self.MB3.CPU_shared,
                 self.MB3.energy]
        # print (state)
        self.state = tuple(state)
        self.training_data += data
        self.training_time += latency
        reward = 10 * (5 * data/self.max_data - latency/self.max_latency - energy_consumption/self.max_energy) + fault

        if (self.training_data > FederatedLearningEnv.DATA_LIMIT):
            done = True
        else:
            done = False
        # if (fault < 0):
        #     print (fault)
            # print(np.array(self.state), action, [reward, data, latency, energy_consumption, fault], done)
        reward /= 10
        return np.array(self.state), [reward, data, latency, energy_consumption, data1, data2, data3], done, {}

    def reset(self):
        self.state = []
        self.MB1.reset()
        self.MB2.reset()
        self.MB3.reset()
        state = [self.MB1.CPU_shared, self.MB1.energy, self.MB2.CPU_shared, self.MB2.energy, self.MB3.CPU_shared, self.MB3.energy]
        self.state = tuple(state)
        self.training_time = 0
        self.training_data = 0
        print(self.state)
        self.steps_beyond_done = None
        return np.array(self.state)

    def updateObservation(self):
        return

    def render(self, mode='human', close=False):
       return

    def close(self):
        """Override in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        raise NotImplementedError()

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        # Returns
            Returns the list of seeds used in this env's random number generators
        """
        raise NotImplementedError()

    def configure(self, *args, **kwargs):
        """Provides runtime configuration to the environment.
        This configuration should consist of data that tells your
        environment how to run (such as an address of a remote server,
        or path to your ImageNet data). It should not affect the
        semantics of the environment.
        """
        raise NotImplementedError()

# env = FederatedLearningEnv()
# env.reset()
# for index in range(0, 100):
#     env.step(env.action_space.sample())