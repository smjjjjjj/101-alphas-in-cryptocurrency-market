# Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap))))) 
from src.metrics.alpha_calculations import vwap
def alpha5(data):
    open_mat = data['open'].unstack('symbol')
    clo_mat = data['close'].unstack('symbol')
    vwap_mat = vwap(data)

    sum_vwap_10 = vwap_mat.rolling(10).mean()
    diff = open_mat - sum_vwap_10
    rank1 = diff.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    diff2 = clo_mat - vwap_mat
    rank2 = diff2.rank(axis = 1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = - rank1 * abs(rank2)
    return alpha.T.values