# Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) *rank(delta(volume, 3))) 
from src.metrics.alpha_calculations import vwap
def alpha11(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    vwap_mat = vwap(data)

    diff1 = vwap_mat - clo_mat
    tsmax = diff1.rolling(3).max()
    rank1 = tsmax.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    tsmin = diff1.rolling(3).min()
    rank2 = tsmin.rank(axis=1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())

    delta = vol_mat - vol_mat.shift(3)
    rank3 = delta.rank(axis = 1, pct = True)
    rank3 = rank3.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = (rank1 + rank2) * rank3
    return alpha.T.values