import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv('data.csv')
df = df.drop(columns=['row.names','home.dest','name','room','boat','embarked','ticket'])
df = df.dropna()

df['pclass'] = df['pclass'].map(lambda x: float(x[:-2])) # drop sufix 


def transform_to_num(df):
    l = list({i for i in df})
    return df.map(lambda x: l.index(x))

df['sex'] = transform_to_num(df['sex']) 

def score(X, Y):
    train_size = 230 

    model = GaussianNB()
    model.fit(X[train_size:],Y[train_size:])

    y = model.predict(X[:train_size])
    y_score = accuracy_score(Y[:train_size], y)

    print(y_score)

for column in df.columns.values:
    print('Column "%s":' % column)
    score(df[column].values.reshape(-1,1),df['survived'])

score(df.drop(columns=['survived']),df['survived'])