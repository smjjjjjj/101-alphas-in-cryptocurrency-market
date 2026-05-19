# Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1))) 
import numpy as np
def alpha12(data):
    clo_mat = data['close'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    alpha = np.sign(vol_mat - vol_mat.shift(1)) * (-1) * (clo_mat - clo_mat.shift(1))
    return alpha.T.values