# Alpha#43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8)) 
from src.metrics.alpha_calculations import adv
def alpha43(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    adv20 = adv(data, 20)

    ind = vol_mat / adv20
    rank1 = ind.rolling(20).rank(pct=True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    delta = -clo_mat + clo_mat.shift(7)
    rank2 = delta.rolling(8).rank(pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = rank1 * rank2
    return alpha.T.values