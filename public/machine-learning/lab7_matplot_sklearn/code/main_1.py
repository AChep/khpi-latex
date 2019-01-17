import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('titanic_test.csv')
data = data.sort_values(by='age')
data = data.groupby('age').size()
data.plot.bar(title='Distribution of age', figsize=(15, 4))
plt.show()
