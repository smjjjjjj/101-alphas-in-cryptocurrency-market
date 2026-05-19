from src.metrics.alpha_metrics import IC, summaryic, alpha_corr_matrix
import numpy as np

# Given several alphas, flipping those with negative ic mean and return as a list. 
def alpha_flipping(alpha_list_ind, alpha_dic, ret):
    alpha_list_train = []
    for alpha_num in alpha_list_ind:
        ic = IC(alpha_dic[alpha_num], ret)
        if summaryic(ic)[0] > 0:
            alpha_list_train.append(alpha_dic[alpha_num])
        else: # Flipping alphas
            alpha_list_train.append(-alpha_dic[alpha_num])
    return alpha_list_train

# Given an alpha result (on a certain dataset), return its rank normalized alpha
def rank_normalize(alpha_res):
    result = np.full_like(alpha_res, np.nan, dtype=float)
    
    for t in range(alpha_res.shape[1]):  # loop over time
        col = alpha_res[:, t]
        mask = ~np.isnan(col)
        
        if np.sum(mask) > 1:
            ranks = np.argsort(np.argsort(col[mask]))
            ranks = ranks / (len(ranks) - 1)
            result[mask, t] = ranks - 0.5
            
    return result

# Equal weight normalized alphas combination
def equal_weight_combining(alpha_dic, alpha_list_ind, ret):
    ss = 0
    for alpha_num in alpha_list_ind:
        if summaryic(IC(alpha_dic[alpha_num], ret))[-1] < 0: # Flipping
            ss -= rank_normalize(alpha_dic[alpha_num])
        else:
            ss += rank_normalize(alpha_dic[alpha_num])
    return ss / len(alpha_list_ind)

# IC weight normalized alphas combination
def ic_weight_combining(alpha_dic, alpha_list_ind, ret):
    ss = 0
    for alpha_num in alpha_list_ind:
        ss += np.nanmean(IC(alpha_dic[alpha_num], ret)) * rank_normalize(alpha_dic[alpha_num])
    return ss

# Correlated weighted normalized alphas combinaition (with regularization)
def corr_adj_weight_combining(alpha_dic, alpha_list_ind, ret, regularize=0.1):
    alpha_list = []
    ic_list = []

    for alpha_num in alpha_list_ind:
        ic_series = IC(alpha_dic[alpha_num], ret)
        ic_mean = summaryic(ic_series)[0]

        if ic_mean > 0:
            aligned_alpha = alpha_dic[alpha_num]
        else:
            aligned_alpha = -alpha_dic[alpha_num]

        alpha_list.append(aligned_alpha)
        ic_list.append(abs(ic_mean))  

    IC_vec = np.array(ic_list)

    # compute correlation matrix
    Sigma = alpha_corr_matrix(alpha_list)

    # regularization
    N = len(alpha_list_ind)
    Sigma_reg = Sigma + regularize * np.eye(N)

    # compute weights using matrix inversion
    w = np.linalg.inv(Sigma_reg) @ IC_vec

    # normalize weights
    w = w / np.sum(np.abs(w))

    # build combined signal
    combined_signal = 0
    for i in range(N):
        combined_signal += w[i] * rank_normalize(alpha_list[i])

    return combined_signal

