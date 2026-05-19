# Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) -0.5) 
import numpy as np
def alpha1(data):
    col_mat = data['close'].unstack('symbol')
    ret = (col_mat - col_mat.shift(1))/col_mat.shift(1)
    std20 = ret.rolling(20).std(ddof=0)
    expr = std20.where(ret < 0, col_mat)
    expr = np.sign(expr) * expr * expr
    argmax = expr.rolling(5).apply(lambda x: len(x) - 1 - np.argmax(x), raw=True)
    rank = argmax.rank(axis = 1, pct = True)
    rank1 = rank.reindex(columns = data.index.get_level_values("symbol").unique()) - 0.5
    return rank1.T.values