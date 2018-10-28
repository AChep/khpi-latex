import pandas
import matplotlib.pyplot as plt

fig, axes = plt.subplots(ncols=2)

data = pandas.read_csv('data.csv')
data.pivot_table('PassengerId', ['SibSp'], 'Survived', 'count')\
    .plot(ax=axes[0], title='SibSp')
data.pivot_table('PassengerId', ['Parch'], 'Survived', 'count')\
    .plot(ax=axes[1], title='Parch')

plt.show()