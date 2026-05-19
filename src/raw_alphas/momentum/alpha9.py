# Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ?delta(close, 1) : (-1 * delta(close, 1)))) 

def alpha9(data):
    clo_mat = data['close'].unstack('symbol')
    delta = clo_mat - clo_mat.shift(1)
    tsmin = delta.rolling(5).min()
    tsmax = delta.rolling(5).max()
    inn = delta.where(tsmax < 0, -1 * delta)
    alpha = delta.where(tsmin > 0, inn)
    return alpha.T.values