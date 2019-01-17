import pandas as pd

from sklearn.metrics import r2_score
from sklearn.svm import SVR

MAX_AGE = 71
MAX_PCLASS = 3


def process_df(df):
    df = df[['pclass', 'survived', 'age', 'sex']]
    df = df.dropna()

    df['pclass'] = df['pclass'].map(lambda x: float(x[:-2]) / MAX_PCLASS)  # drop sufix
    df['age'] = df['age'].map(lambda x: x / MAX_AGE)

    def transform_to_num(df):
        l = list({i for i in df})
        return df.map(lambda x: l.index(x))

    df['sex'] = transform_to_num(df['sex'])
    return df


test = process_df(pd.read_csv('titanic_test.csv'))
train = process_df(pd.read_csv('titanic_train.csv'))

test_X, test_Y = test.drop(columns=['survived']), test['survived']
train_X, train_Y = train.drop(columns=['survived']), train['survived']


def score(kernel):
    regr = SVR(kernel=kernel)
    regr.fit(train_X, train_Y)

    pred_Y = regr.predict(test_X)
    print('%s, R2 score: %f' % (kernel, r2_score(test_Y, pred_Y)))
    print('%s, Intercept: %f' % (kernel, regr.intercept_))


score('linear')
score('poly')
score('rbf')
