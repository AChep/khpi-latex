import pandas

data = pandas.read_csv('data.csv')

# Calculate a mean fare to determine what is
# a high price.
fare_mean = data.Fare.mean()
result = data.Embarked[data.Fare > fare_mean][data.Embarked == 'Q'].count()
