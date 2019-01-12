import numpy as np


class Network:

    def __init__(self, structure, eta=0.01, n_iter=100):
        self.eta = eta
        self.n_iter = n_iter

        self.n = len(structure)

        self.W = []
        for i in range(self.n - 1):
            self.W.append(np.random.randn(structure[i], structure[i + 1]) * 0.1)

        self.B = []
        for i in range(1, self.n):
            self.B.append(np.random.randn(structure[i]) * 0.1)

        self.O = []
        for i in range(self.n):
            self.O.append(np.zeros([structure[i]]))

        self.D = []
        for i in range(1, self.n):
            self.D.append(np.zeros(structure[i]))

    def fit(self, A, y, a=0.5, iterations_num=200):
        self.act_f = []
        self.df = []

        for i in range(self.n):
            self.act_f.append(lambda x: 1 / (1 + np.exp(-x)))
            self.df.append(np.vectorize(lambda y: y * (1 - y)))

        for c in range(iterations_num):
            for i in range(len(A)):
                t = y[i, :]
                self.O[0] = A[i, :]
                for j in range(self.n - 1):
                    self.O[j + 1] = self.act_f[j](np.dot(self.O[j], self.W[j]) + self.B[j])
                self.D[-1] = np.multiply((t - self.O[-1]), self.df[-1](self.O[-1]))
                for j in range(self.n - 2, 0, -1):
                    self.D[j - 1] = np.multiply(np.dot(self.D[j], self.W[j].T), self.df[j](self.O[j]))
                for j in range(self.n - 1):
                    self.W[j] = self.W[j] + a * np.outer(self.O[j], self.D[j])
                    self.B[j] = self.B[j] + a * self.D[j]

    def predict(self, A):
        for i in range(len(A)):
            self.O[0] = A[i, :]
            for j in range(self.n - 1):
                self.O[j + 1] = self.act_f[j](np.dot(self.O[j], self.W[j]) + self.B[j])
            return self.O[-1]