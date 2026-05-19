# Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5))) 
from src.metrics import alpha_calculations
def alpha13(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    rank1 = clo_mat.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    rank2 = vol_mat.rank(axis = 1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())
    cov = alpha_calculations.rollingcovariance(rank1, rank2, 5)
    rank3 = cov.rank(axis = 1, pct = True)
    rank3 = rank3.reindex(columns = data.index.get_level_values("symbol").unique())
    alpha = -rank3
    return alpha.T.values