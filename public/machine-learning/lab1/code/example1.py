import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv('data.csv')
data.pivot_table('PassengerId', 'Pclass', 'Survived', 'count')\
    .plot(kind='bar', stacked=True)

plt.show()