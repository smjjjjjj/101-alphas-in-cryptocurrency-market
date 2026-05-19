import numpy as np
# Some basic functions for alpha calculations
def adv(data, window):
    vol_mat = data['volume'].unstack('symbol')
    return vol_mat.rolling(window).mean()

def vwap(data):
    clo_mat = data['close'].unstack('symbol')
    high_mat = data['high'].unstack('symbol')
    low_mat = data['low'].unstack('symbol')
    # Originally, the Volume Weighted Average Price is calculated as the sum of prices * volumes / the sum of volumes
    # Here we made an approximation
    vwap_mat = (clo_mat + high_mat + low_mat) / 3
    return vwap_mat
def rollingcovariance(series1, series2, window):
    # A sliding window way to calculate the rolling covariance
    mean_x = series1.rolling(window).mean()
    mean_y = series2.rolling(window).mean()
    mean_xy = (series1 * series2).rolling(window).mean()
    return mean_xy - mean_x * mean_y

def rollingcorrelation(series1, series2, window):
    # A sliding window way to calculate the rolling correlation
    # The rolling window methods' std has default ddof = 1, we need to manually send them into 0
    std_x = series1.rolling(window).std(ddof = 0)
    std_y = series2.rolling(window).std(ddof = 0)
    corr = rollingcovariance(series1, series2, window) / (std_x * std_y)
    
    # Only compute correlation when both std is not 0, otherwise just go nan.
    corr[(std_x == 0) | (std_y == 0)] = np.nan
    return corr

def normalreturn(data):
    col_mat = data['close'].unstack('symbol')
    ret = (col_mat - col_mat.shift(1))/col_mat.shift(1)
    return ret.T.values

def logreturn(data):
    col_mat = data['close'].unstack('symbol')
    ret = np.log((col_mat/col_mat.shift(1)))
    return ret.T.values