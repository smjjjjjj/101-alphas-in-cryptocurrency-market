import numpy as np
# Given alphas on a certain dataset, build up the long-short portfolios with a daily rebalanced position.
# Percentage: the long-short proportions. e.g with default value 0.1 means go long top 10% and short top 10% based on the alpha results
# short: Boolean. True means can go short. False means cannot. Be careful: some cyptocurrencies markets do not allow short.
# cost: the proportional costs, based on the turnover weight of each day.

def portfolio_return_with_cost(data, alpha, percentage = 0.1, short = False, cost = 0.001):
    all_dates = data.index.get_level_values("date").unique()
    open_mat = data['open'].unstack('symbol').T.values
    close_mat = data['close'].unstack('symbol').T.values
    l = np.shape(open_mat)[1]
    daily_return = [0 for j in range(l)]

    prev_long = set()
    prev_short = set()

    for date in range(len(all_dates)-1):
        today_alpha = alpha[:, date]
        valid_count = np.sum(~np.isnan(today_alpha))

        if valid_count >= 10:
            choose_num = int(valid_count * percentage)

            valid_idx = np.where(~np.isnan(today_alpha))[0]
            sorted_idx = valid_idx[np.argsort(today_alpha[valid_idx])]

            indices_long = set(sorted_idx[-choose_num:])
            indices_short = set(sorted_idx[:choose_num])

            tmr_open = open_mat[:, date +1]
            tmr_close = close_mat[:, date +1]

            ss = 0

            for j in indices_long:
                if ~np.isnan(tmr_open[j]) and tmr_open[j] > 0:
                    ss += (tmr_close[j] - tmr_open[j])/tmr_open[j] * 1/choose_num

            if short:
                for j in indices_short:
                    if ~np.isnan(tmr_open[j]) and tmr_open[j] > 0:
                        ss += -(tmr_close[j] - tmr_open[j])/tmr_open[j] * 1/choose_num

            # --------- transaction cost part ----------
            turnover_long = len(indices_long.symmetric_difference(prev_long)) / max(choose_num, 1)

            if short:
                turnover_short = len(indices_short.symmetric_difference(prev_short)) / max(choose_num, 1)
                turnover = 0.5 * (turnover_long + turnover_short)
            else:
                turnover = turnover_long

            ss -= cost * turnover
            # -----------------------------------------

            prev_long = indices_long
            prev_short = indices_short

            daily_return[date + 1] = ss

    return np.array(daily_return)