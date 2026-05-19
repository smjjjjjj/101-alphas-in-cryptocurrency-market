import numpy as np

def sharpe_ratio(timeseries, days = 365):
    return np.mean(timeseries)/np.std(timeseries) * np.sqrt(days)

def cumulative_pnl(daily_return, initial_capital=1.0):
    wealth = np.zeros_like(daily_return)
    wealth[0] = initial_capital

    for t in range(1, len(daily_return)):
        wealth[t] = wealth[t-1] * (1 + daily_return[t])

    return wealth


def max_drawdown(curve):
    curve = np.array(curve)
    peak = np.maximum.accumulate(curve)
    drawdown = (curve - peak) / peak
    return np.min(drawdown), drawdown  # return both MDD and full series
