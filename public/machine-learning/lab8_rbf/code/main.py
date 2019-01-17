import numpy as np
import matplotlib.pyplot as plt

from RBFN import RBFN


def gen(begin, end, p):
    x = np.linspace(begin, end, p)
    y = np.sin(x)
    return x, y


x_train, y_train = gen(0, 20, 20)
model = RBFN(hidden_shape=15, sigma=1.)
model.fit(x_train, y_train)
x_test, y_test = gen(0, 20, 100)
y_pred = model.predict(x_test)

plt.plot(x_train, y_train, 'b-', label='real')
plt.plot(x_test, y_pred, 'r-', label='fit')
plt.legend(loc='upper right')
plt.show()
