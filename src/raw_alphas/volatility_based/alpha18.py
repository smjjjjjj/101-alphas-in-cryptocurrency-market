# Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open,10))))
from src.metrics import alpha_calculations
def alpha18(data):
    clo_mat = data['close'].unstack('symbol')
    open_mat = data['open'].unstack('symbol')
    diff = (clo_mat - open_mat)
    abs_diff = abs(diff)
    stddev = abs_diff.rolling(5).std(ddof = 0)
    corr = alpha_calculations.rollingcorrelation(clo_mat, open_mat, 10)
    ind = corr + stddev + clo_mat - open_mat
    
    rank = ind.rank(axis = 1, pct = True)
    rank = rank.reindex(columns = data.index.get_level_values("symbol").unique())
    alpha = -rank
    return alpha.T.values