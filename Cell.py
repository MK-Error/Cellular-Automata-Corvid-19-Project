import numpy as np
from random import randint


class Cell:
    def __init__(self):
        self.state = 0  # 0 -> susceptible | 1 -> exposed | 2 -> infected | 3 -> recovered
        self.positionX = round(np.random.uniform() * 200) #field is 100 x 100
        self.positionY = round(np.random.uniform() * 200)
        self.time_since_infection = 0
