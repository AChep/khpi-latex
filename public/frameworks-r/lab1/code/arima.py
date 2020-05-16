import pandas as pd
import numpy as np
import pmdarima as pm

from statsmodels.tsa.arima_model import ARIMA

def arima(series):
    print(series)
    series_week = pd.DataFrame(series).GOLD
    series_week_log = np.log(series_week)
    series_week_log_diff = series_week_log - series_week_log.shift()
    series_week_log_diff.dropna(inplace=True)


    print(series_week_log_diff)
    model = ARIMA(series_week_log_diff, order=(1, 0, 0))  
    results_ARIMA = model.fit(disp=-1)  

    euro_predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    euro_predictions_ARIMA_diff_cumsum = euro_predictions_ARIMA_diff.cumsum()
    euro_predictions_ARIMA_log = pd.Series(series_week_log_diff.iloc[0], index=series_week_log_diff.index)
    euro_predictions_ARIMA_log = euro_predictions_ARIMA_log.add(euro_predictions_ARIMA_diff_cumsum,fill_value=0)
    euro_predictions_ARIMA = np.exp(euro_predictions_ARIMA_log)

    print(euro_predictions_ARIMA.values)
    return euro_predictions_ARIMA.values
    # return euro_predictions_ARIMA.values
