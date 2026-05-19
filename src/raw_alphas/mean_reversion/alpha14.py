# Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10)) 
from src.metrics.alpha_calculations import rollingcorrelation
def alpha14(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    corr = rollingcorrelation(clo_mat, vol_mat, 10)
    ret = (clo_mat - clo_mat.shift(1))/clo_mat.shift(1)
    delta = ret - ret.shift(3)
    rank = delta.rank(axis = 1, pct = True)
    rank = rank.reindex(columns = data.index.get_level_values("symbol").unique())
    alpha = -rank* corr
    return alpha.T.values