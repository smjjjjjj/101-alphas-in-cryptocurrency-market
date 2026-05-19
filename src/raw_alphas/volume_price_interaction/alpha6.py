# Alpha#6: (-1 * correlation(open, volume, 10)) 
from src.metrics import alpha_calculations
def alpha6(data):
    open_mat = data['open'].unstack('symbol')
    vol_mat = data['volume'].unstack('symbol')
    alpha = -alpha_calculations.rollingcorrelation(open_mat, vol_mat, 10)
    return alpha.T.values