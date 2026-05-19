# Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))
from src.metrics.alpha_calculations import adv, vwap
def alpha25(data):
    clo_mat = data['close'].unstack('symbol')
    ret = (clo_mat - clo_mat.shift(1))/clo_mat.shift(1)
    adv20 = adv(data, 20)
    vwap_mat = vwap(data)

    high_mat = data['high'].unstack('symbol')
    ind = -1 * ret * adv20 * vwap_mat * (high_mat - clo_mat)
    rank = ind.rank(axis = 1, pct = True)
    alpha = rank.reindex(columns = data.index.get_level_values("symbol").unique())
    return alpha.T.values