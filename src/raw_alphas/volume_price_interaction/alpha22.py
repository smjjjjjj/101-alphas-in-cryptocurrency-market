# Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))
from src.metrics.alpha_calculations import rollingcorrelation
def alpha22(data):
    high_mat = data['high'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    clo_mat = data['close'].unstack('symbol')

    corr = rollingcorrelation(high_mat, vol_mat, 5)
    delta = corr - corr.shift(5)
    
    stddev = clo_mat.rolling(20).std(ddof = 0)
    rank = stddev.rank(axis = 1, pct = True)
    rank = rank.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = - delta * rank
    return alpha.T.values