from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot as plt
from pandas.plotting import autocorrelation_plot

import pandas as pd
import numpy as np


def date_parse(date):
    return pd.datetime.strptime(date, '%d-%m-%y')

series = pd.read_csv('data.csv', header=0,  parse_dates=['date'], date_parser=date_parse, index_col=0)
series = series['price']
series_week = series.resample('W').mean()
series_week_log = np.log(series_week)
series_week_log_diff = series_week_log - series_week_log.shift()
series_week_log_diff.dropna(inplace=True)

model = ARIMA(series_week_log, order=(3, 1, 1))  
results_ARIMA = model.fit(disp=-1)  

euro_predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
euro_predictions_ARIMA_diff_cumsum = euro_predictions_ARIMA_diff.cumsum()
euro_predictions_ARIMA_log = pd.Series(series_week_log.iloc[0], index=series_week_log.index)
euro_predictions_ARIMA_log = euro_predictions_ARIMA_log.add(euro_predictions_ARIMA_diff_cumsum,fill_value=0)
euro_predictions_ARIMA = np.exp(euro_predictions_ARIMA_log)
plt.plot(series_week.index.to_pydatetime(), series_week.values)
plt.plot(series_week.index.to_pydatetime(), euro_predictions_ARIMA.values)
plt.title('RMSE: %.4f'% np.sqrt(sum((euro_predictions_ARIMA-series_week)**2)/len(series_week)))
plt.show()