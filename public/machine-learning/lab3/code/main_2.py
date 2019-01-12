import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture

from matplotlib import pyplot as plt

df = pd.read_csv('data.csv')
df = df.drop(columns=['row.names','home.dest','name','room','boat','embarked','ticket'])
df = df.dropna()

df['pclass'] = df['pclass'].map(lambda x: float(x[:-2])) # drop sufix 


def transform_to_num(df):
    l = list({i for i in df})
    return df.map(lambda x: l.index(x))

df['sex'] = transform_to_num(df['sex']) 
X = df.drop(columns=['survived'])

def score(X):
	model = GaussianMixture(n_components=2, covariance_type='full')
	model.fit(X) 
	y = model.predict(X)

	s = [1 if int(df.iloc[i]['survived']) == v else 0 for i, v in enumerate(y)]
	s_sum = sum(s)
	r = max(len(s) - s_sum, s_sum)
	print(r / len(s))

for column in df.columns.values:
    print('Column "%s":' % column)
    score(df[column].values.reshape(-1,1))

score(df.drop(columns=['survived']))