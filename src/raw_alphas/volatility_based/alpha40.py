# Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
from src.metrics import alpha_calculations
def alpha40(data):
    high_mat = data['high'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')

    stddev = high_mat.rolling(10).std(ddof = 0)
    rank1 = stddev.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    corr = alpha_calculations.rollingcorrelation(high_mat, vol_mat, 10)
    alpha = - rank1 * corr
    return alpha.T.values