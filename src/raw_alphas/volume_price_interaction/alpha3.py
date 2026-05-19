# Alpha#3: (-1 * correlation(rank(open), rank(volume), 10)) 
from src.metrics.alpha_calculations import rollingcorrelation
def alpha3(data):
    open_mat = data['open'].unstack('symbol')
    rank_mat = open_mat.rank(axis=1, pct=True)
    rank_mat = rank_mat.reindex(columns=data.index.get_level_values("symbol").unique())

    vol_mat = data['volume'].unstack('symbol')
    vrank_mat = vol_mat.rank(axis=1, pct=True)
    vrank_mat = vrank_mat.reindex(columns=data.index.get_level_values("symbol").unique())

    alpha = -rollingcorrelation(rank_mat, vrank_mat, 10)

    return alpha.T.values