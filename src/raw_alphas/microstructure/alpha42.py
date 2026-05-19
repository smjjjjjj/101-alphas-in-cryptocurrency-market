# Alpha#42: (rank((vwap - close)) / rank((vwap + close)))
from src.metrics.alpha_calculations import vwap
def alpha42(data):
    clo_mat = data['close'].unstack('symbol')
    vw = vwap(data)

    rank1 = (vw - clo_mat).rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    rank2 = (vw + clo_mat).rank(axis = 1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())
    alpha = rank1/rank2

    return alpha.T.values