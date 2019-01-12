from network import Network

import matplotlib.pyplot as plt
import numpy as np
import math


class Experiment:

    def __init__(self, structure):
        self.net = Network(np.array(structure))

    def run(self):
        self.train()

        # Visualize the comparison between sin(x) and
        # a simulated sin(x).

        offset = 1
        r = range(150)

        plt.plot(r, [Experiment._y(Experiment._x(i) + offset) for i in r], marker='o')
        plt.plot(r, [self.net.predict(np.matrix([[(Experiment._x(i) + offset) % (2.0 * math.pi)]]))[0, 0] for i in r], marker='o')
        plt.show()

    def train(self):
        X, y = Experiment._make_train_data(0, 1000)
        X, y = np.matrix(X), np.matrix(y)
        self.net.fit(X, y)

    @staticmethod
    def _x(x):
        return 0.1 * x

    @staticmethod
    def _y(x):
        return (math.sin(x) + 1) / 2

    @staticmethod
    def _make_pairs(x):
        return [x % (2.0 * math.pi)], [Experiment._y(x)]

    @staticmethod
    def _make_train_data(offset, n):
        X = []
        y = []

        for i in range(n):
            a, b = Experiment._make_pairs(Experiment._x(i) + offset)
            X.append(a)
            y.append(b)

        return X, y