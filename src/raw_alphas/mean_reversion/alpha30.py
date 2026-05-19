# Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))
import numpy as np
def alpha30(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    sign1 = np.sign(clo_mat - clo_mat.shift(1))
    sign2 = np.sign(clo_mat.shift(1) - clo_mat.shift(2))
    sign3 = np.sign(clo_mat.shift(2) - clo_mat.shift(3))
    ind = sign1 + sign2 + sign3
    rank1 = ind.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    sum1 = vol_mat.rolling(5).sum()
    sum2 = vol_mat.rolling(20).sum()
    alpha = (1-rank1)  * sum1 / sum2
    return alpha.T.values