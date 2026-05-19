# Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open -delay(low, 1)))) 
def alpha20(data):
    open_mat = data['open'].unstack('symbol')
    high_mat = data['high'].unstack('symbol')
    low_mat = data['low'].unstack('symbol')
    clo_mat = data['close'].unstack('symbol')

    ind1 = open_mat - high_mat.shift(1)
    rank1 = ind1.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    ind2 = open_mat - clo_mat.shift(1)
    rank2 = ind2.rank(axis = 1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())

    ind3 = open_mat - low_mat.shift(1)
    rank3 = ind3.rank(axis = 1, pct = True)
    rank3 = rank3.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = - rank1 * rank2 * rank3
    return alpha.T.values