import random
import math
import numpy as np

class Mobile():
    MAX_CPU = 3
    MAX_ENERGY = 3
    MAX_DATA = 3

    ENERGY_OF_UNIT = 1
    CPU_CYCLE_PER_UNIT = math.pow(10, 10)
    TAU = math.pow(10, -28)
    LAMBDA = 1
    CPU_UNIT = 0.6 * math.pow(10, 9)
    MAX_LATENCY = math.sqrt(TAU * pow(CPU_CYCLE_PER_UNIT * MAX_DATA, 3) / (1 * ENERGY_OF_UNIT))


    def __init__(self):
        self.CPU_shared = random.randint(0, Mobile.MAX_CPU)
        self.energy = random.randint(0, Mobile.MAX_ENERGY)

    def update(self, data_required, energy_required):
        if data_required != 0 and energy_required != 0:
            CPU_required = math.sqrt(energy_required * Mobile.ENERGY_OF_UNIT * 1.0 / (Mobile.TAU * Mobile.CPU_CYCLE_PER_UNIT * data_required)) / Mobile.CPU_UNIT
            if CPU_required <= self.CPU_shared and energy_required <= self.energy:
                data = data_required
                latency = Mobile.CPU_CYCLE_PER_UNIT * data_required / (CPU_required * Mobile.CPU_UNIT)
                energy_consumption = energy_required
                fault = 0
            else:
                data = 0
                latency = 0
                energy_consumption = 0
                fault = -5
        else:
            data = 0
            latency = 0
            energy_consumption = 0
            fault = 0

        self.CPU_shared = random.randint(0, Mobile.MAX_CPU)
        energy_charged = np.random.poisson(Mobile.LAMBDA)
        self.energy = min(self.energy - energy_consumption + energy_charged, Mobile.MAX_ENERGY)

        return data, latency, energy_consumption, fault

    def reset(self):
        self.CPU_shared = random.randint(0, Mobile.MAX_CPU)
        self.energy = random.randint(0, Mobile.MAX_ENERGY)