import numpy as np
import pandas as pd

def IC(alpha, ret, window = 1):
    output = np.full(np.shape(alpha)[-1]-window, np.nan)
    for i in range(len(output)):
        alpha_i = alpha[:, i]
        ret_i = ret[:, i+window]
        
        # keep only valid pairs
        mask = ~np.isnan(alpha_i) & ~np.isnan(ret_i)
        
        x = alpha_i[mask]
        y = ret_i[mask]
        # need at least 2 points for correlation
        if len(x) > 1 and np.std(x) != 0 and np.std(y) != 0:
            output[i] = np.corrcoef(x, y)[0, 1]
    
    return output

def summaryic(ic_list):
    valid_value = []
    for j in ic_list:
        if ~np.isnan(j):
            valid_value.append(j)
    valid_value = np.array(valid_value)
    m = np.mean(valid_value)
    n = np.std(valid_value)
    t = m * np.sqrt(len(valid_value)) / n
    return [m, n, t]

# Given a list of alphas realizing on a certain dataset, return their correlation matrix.
def alpha_corr_matrix(alpha_list):
    n = len(alpha_list)
    corr_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            
            date_num = alpha_list[i].shape[1]
            corrs = []

            for t in range(date_num):
                x = alpha_list[i][:, t]
                y = alpha_list[j][:, t]

                mask = ~np.isnan(x) & ~np.isnan(y)

                if np.sum(mask) > 1:
                    corr = np.corrcoef(x[mask], y[mask])[0, 1]
                    corrs.append(corr)

            corr_matrix[i, j] = np.nanmean(corrs) if len(corrs) > 0 else np.nan
    return corr_matrix

# Given a realization of alpha on a dataset, return its turnover rate on average.
def turnover_rate(alpha):
    rank = pd.DataFrame(alpha).rank(axis=0, pct=True)
    diff = np.array(rank.iloc[:, :-1])- np.array(rank.iloc[:, 1:])
    return np.nanmean(np.abs(diff))

# Given a realization of alpha on a dataset, return its positive ratio
def positive_ratio(alpha):
    return np.mean(alpha > 0)

def rolling_ic(ic, window = 60):
    rolling_ic = pd.Series(ic).rolling(window).mean()
    return rolling_ic

def turnover_timeseries(alpha):
    rank = pd.DataFrame(alpha).rank(axis=0, pct=True)

    turnover_series = [np.nan for j in range(rank.shape[1] - 1)]

    for t in range(rank.shape[1] - 1):
        diff = np.array(rank.iloc[:, t]) - np.array(rank.iloc[:, t+1])
        if not np.all(np.isnan(diff)):
            turnover_t = np.nanmean(np.abs(diff))
            turnover_series[t] = turnover_t

    return np.array(turnover_series)