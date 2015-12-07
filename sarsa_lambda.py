import numpy as np
import random
import time


class Agent(object):
    """A sarsa(lambda) agent for GridWorld"""

    def __init__(self):
        """
        :param rewards: a numpy array
        """
        self.alpha = 0.1
        self.gamma = 0.5
        self.lambd = 0.9
        self.epsilon = 0.9
        self.reset_etable()
        self.init_qtable()

    def reset_etable(self):
        """Zero out eligibility table"""
        self.etable = np.zeros((22, 22, 4))

    def init_qtable(self):
        """Initialize Q(s, a) table with random small values"""
        self.qtable = np.random.random_sample((22,22,4)) * 0.9 + 0.01

    def take_step(self, reward):
        (row_prime, col_prime) = self.move()
        print('{}'.format((self.row, self.col)))
        print('{}'.format((row_prime, col_prime)))
        action_prime = self.choose_action(row_prime, col_prime)
        delta = (
            reward +
            (self.gamma * self.qtable[row_prime][col_prime][self.action]) -
            self.qtable[self.row][self.col][self.action]
        )
        self.etable[self.row][self.col][self.action] += 1
        self.qtable += self.alpha * self.lambd * self.etable
        self.row = row_prime
        self.col = col_prime
        self.action = action_prime
        

    def spawn(self):
        """Initialize state and action for new episode"""
        random.seed()
        self.row = random.randint(0, 21)
        self.col = random.randint(0, 21)
        self.action = self.choose_action(self.row, self.col)
        self.reset_etable()

    def move(self):
        """
        0: UP
        1: DOWN
        2: LEFT
        3: RIGHT
        """
        if self.action == 0:
            return (self.row - 1, self.col)
        elif self.action == 1:
            return (self.row + 1, self.col)
        elif self.action == 2:
            return (self.row, self.col - 1)
        elif self.action == 3:
            return (self.row, self.col + 1)

    def choose_action(self, row, col):
        """Pick a move using epsilon-greedy"""
        random.seed()
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        else:
            return self.best_action(row, col)

    def best_action(self, row, col):
        q = self.qtable[row][col]
        best = np.max(q)
        for i in range(4):
            if best == q[i]:
                return i

