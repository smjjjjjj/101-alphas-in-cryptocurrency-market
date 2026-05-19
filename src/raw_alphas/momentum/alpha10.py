# Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0)? delta(close, 1) : (-1 * delta(close, 1)))))

def alpha10(data):
    clo_mat = data['close'].unstack('symbol')
    delta = clo_mat - clo_mat.shift(1)
    tsmin = delta.rolling(4).min()
    tsmax = delta.rolling(4).max()
    inn = delta.where(tsmax < 0, -1 * delta)
    alpha = delta.where(tsmin > 0, inn)
    alpha = alpha.rank(axis=1, pct=True)
    return alpha.T.values