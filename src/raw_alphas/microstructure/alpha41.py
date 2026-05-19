# Alpha#41: (((high * low)^0.5) - vwap)
from src.metrics.alpha_calculations import vwap
def alpha41(data):
    high_mat = data['high'].unstack('symbol')
    low_mat = data['low'].unstack('symbol')
    vw = vwap(data)
    alpha = (high_mat * low_mat)**0.5 - vw

    return alpha.T.values