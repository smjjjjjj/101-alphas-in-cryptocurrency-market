# Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6)) 
import numpy as np
from src.metrics import alpha_calculations
def alpha2(data):
    vol_mat = data['volume'].unstack('symbol')
    log_vol = np.log(vol_mat)
    delta_log_volume = log_vol - log_vol.shift(2)
    rank1 = delta_log_volume.rank(axis = 1, pct = True)
    rank1 = rank1.reindex(columns = data.index.get_level_values("symbol").unique())

    
    col_mat = data['close'].unstack('symbol')
    open_mat = data['open'].unstack('symbol')
    delta_price = (col_mat - open_mat)/open_mat
    rank2 = delta_price.rank(axis = 1, pct = True)
    rank2 = rank2.reindex(columns = data.index.get_level_values("symbol").unique())

    alpha = -alpha_calculations.rollingcorrelation(rank1, rank2, 6)

    return alpha.T.values