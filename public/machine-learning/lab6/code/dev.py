# https://dataplatform.cloud.ibm.com/exchange/public/entry/view/815137c868b916821dec777bdc23013c

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


def check_stationarity(timeseries):
    # Determing rolling statistics
    rolling_mean = timeseries.rolling(window=3, center=False).mean()
    rolling_std = timeseries.rolling(window=3, center=False).std()

    # Plot rolling statistics:
    original = plt.plot(timeseries.index.to_pydatetime(), timeseries.values, color='blue', label='Original')
    mean = plt.plot(rolling_mean.index.to_pydatetime(), rolling_mean.values, color='red', label='Rolling Mean')
    std = plt.plot(rolling_std.index.to_pydatetime(), rolling_std.values, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dickey_fuller_test = adfuller(timeseries, autolag='AIC')
    dfresults = pd.Series(dickey_fuller_test[0:4],
                          index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dickey_fuller_test[4].items():
        dfresults['Critical Value (%s)' % key] = value
    print(dfresults)

series = pd.read_csv('data.csv', header=0,  parse_dates=['date'], date_parser=date_parse, index_col=0)
series = series['price']
series_week = series.resample('W').mean()

plt.plot(series_week)
plt.show()

#
# Apply a nonlinear log transformation
#

series_week_log = np.log(series_week)
check_stationarity(series_week_log)

#
# Decompose
#

series_week_dec = seasonal_decompose(series_week)

trend = series_week_dec.trend
seasonal = series_week_dec.seasonal
residual = series_week_dec.resid

plt.subplot(411)
plt.plot(series_week.index.to_pydatetime(), series_week.values, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(series_week.index.to_pydatetime(), trend.values, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(series_week.index.to_pydatetime(), seasonal.values,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(series_week.index.to_pydatetime(), residual.values, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

series_week_log_diff = series_week_log - series_week_log.shift()
series_week_log_diff.dropna(inplace=True)
plt.plot(series_week_log_diff)
plt.show()

check_stationarity(series_week_log_diff)

autocorrelation_plot(series_week_log_diff)
plt.show()

#ACF and PACF plots

lag_auto_corr = acf(series_week_log_diff, nlags=2)
lag_par_auto_corr = pacf(series_week_log_diff, nlags=2, method='ols')

#Plot ACF: 
plt.plot(lag_auto_corr)
plt.axhline(y=0,linestyle='--',color='black')
plt.axhline(y=-1.96/np.sqrt(len(series_week_log_diff)),linestyle='--',color='black')
plt.axhline(y=1.96/np.sqrt(len(series_week_log_diff)),linestyle='--',color='black')
plt.show()

#Plot PACF:
plt.plot(lag_par_auto_corr)
plt.axhline(y=0,linestyle='--',color='black')
plt.axhline(y=-1.96/np.sqrt(len(series_week_log_diff)),linestyle='--',color='black')
plt.axhline(y=1.96/np.sqrt(len(series_week_log_diff)),linestyle='--',color='black')
plt.show()

model = ARIMA(series_week_log, order=(3, 1, 1))  
results_ARIMA = model.fit(disp=-1)  
plt.plot(series_week_log_diff.index.to_pydatetime(), series_week_log_diff.values)
plt.plot(series_week_log_diff.index.to_pydatetime(), results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-series_week_log_diff)**2))
plt.show()

residuals = DataFrame(results_ARIMA.resid)
residuals.plot(kind='kde')
plt.show()

euro_predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
print (euro_predictions_ARIMA_diff.head())

euro_predictions_ARIMA_diff_cumsum = euro_predictions_ARIMA_diff.cumsum()
euro_predictions_ARIMA_log = pd.Series(series_week_log.iloc[0], index=series_week_log.index)
euro_predictions_ARIMA_log = euro_predictions_ARIMA_log.add(euro_predictions_ARIMA_diff_cumsum,fill_value=0)
euro_predictions_ARIMA = np.exp(euro_predictions_ARIMA_log)
plt.plot(series_week.index.to_pydatetime(), series_week.values)
plt.plot(series_week.index.to_pydatetime(), euro_predictions_ARIMA.values)
plt.title('RMSE: %.4f'% np.sqrt(sum((euro_predictions_ARIMA-series_week)**2)/len(series_week)))
plt.show()