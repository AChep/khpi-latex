import matplotlib.pyplot as plt
import seaborn

import pandas as pd

data = pd.read_csv('titanic_test.csv')
data = data[['age', 'sex']]
data = data.dropna()

data = data.sort_values(by='age')
data['sex'] = data['sex'].map(lambda x: 1 if x == 'male' else 0)

seaborn.pairplot(data)
plt.show()
