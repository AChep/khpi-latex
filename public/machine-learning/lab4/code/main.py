from som import SOM
from matplotlib import pyplot as plt
from matplotlib import patches as patches
import matplotlib.lines as mlines

import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

agri_som = SOM(3,3,3)

df = pd.read_csv('data.csv')
df = df.drop(columns=['row.names','home.dest','name','room','boat','embarked','ticket'])
df = df.dropna()

df['pclass'] = df['pclass'].map(lambda x: float(x[:-2])) # drop sufix 
df['pclass'] = df['pclass'].map(lambda x: x / 3.0) # normalize 

def transform_to_num(df):
    l = list({i for i in df})
    return df.map(lambda x: l.index(x) / len(l))

df['sex'] = transform_to_num(df['sex']) 

age_max = max(df['age'])
df['age'] = df['age'].map(lambda x: x / age_max) # normalize 
X = df.drop(columns=['survived'])

agri_som.train(X.values,num_epochs=250,init_learning_rate=0.01)

init_fig = plt.figure()
agri_som.show_plot(init_fig, 1, 0)
plt.show()

def predict(df):
    bmu, bmu_idx = agri_som.find_bmu(df.values)
    df['bmu'] = bmu
    df['bmu_idx'] = bmu_idx
    return df

X = X.apply(predict, axis=1)
X = X.join(df, rsuffix="_norm")

fig = plt.figure()
# setup axes
ax = fig.add_subplot(111)
scale = 50
ax.set_xlim((0, agri_som.net.shape[0]*scale))
ax.set_ylim((0, agri_som.net.shape[1]*scale))

for x in range(0, agri_som.net.shape[0]):
    for y in range(0, agri_som.net.shape[1]):
        ax.add_patch(patches.Rectangle((x*scale, y*scale), scale, scale,
                     facecolor='white',
                     edgecolor='grey'))
legend_map = {}
        
for index, row in X.iterrows():
    x_cor = row['bmu_idx'][0] * scale
    y_cor = row['bmu_idx'][1] * scale
    x_cor = np.random.randint(x_cor, x_cor + scale)
    y_cor = np.random.randint(y_cor, y_cor + scale)
    color = row['bmu'][0]
    marker = "$\\ " + str(row['survived'])[0]+"$"
    marker = marker.lower()
    ax.plot(x_cor, y_cor, color=color, marker=marker, markersize=10)
    label = 'survived' if row['survived'] > 0.5 else 'died'
    if not label in legend_map:
        legend_map[label] =  mlines.Line2D([], [], color='black', marker=marker, linestyle='None',
                          markersize=10, label=label)
plt.legend(handles=list(legend_map.values()), bbox_to_anchor=(1, 1))
plt.show()