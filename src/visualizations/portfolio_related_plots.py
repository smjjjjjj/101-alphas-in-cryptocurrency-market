from src.portfolios.portfolios_building import portfolio_return_with_cost
from src.metrics.portfolio_metrics import sharpe_ratio, max_drawdown, cumulative_pnl
import matplotlib.pyplot as plt
import numpy as np
from src.metrics.alpha_metrics import IC, summaryic, turnover_timeseries

def super_alphas_sharpe_ratio_plot(alpha_train_dic, alpha_test_dic,data_train, data_test, methods, bucket = 0.1, short = False, cost = 0):
    benchmark_train = portfolio_return_with_cost(data_train, alpha_train_dic['Equally-weighted rank'], 1, short = False, cost = cost)
    benchmark_test = portfolio_return_with_cost(data_test, alpha_test_dic['Equally-weighted rank'], 1, short = False, cost = cost)

    daily_return_dic =  {'Benchmark': (benchmark_train, benchmark_test)}
    for method in methods:
        daily_return_dic[method] = (portfolio_return_with_cost(data_train, alpha_train_dic[method], bucket, short = short, cost = cost), 
                                    portfolio_return_with_cost(data_test, alpha_test_dic[method], bucket, short = short, cost = cost))
    sharpe_ratio_dic = {}
    for method in daily_return_dic: 
        sharpe_ratio_dic[method] = (sharpe_ratio(daily_return_dic[method][0]), 
                                    sharpe_ratio(daily_return_dic[method][1]))
    
    is_values = [v[0] for v in sharpe_ratio_dic.values()]
    oos_values = [v[1] for v in sharpe_ratio_dic.values()]
# Positions
    x = np.arange(len(sharpe_ratio_dic))
    offset = 0.05  # controls spacing within each method

    plt.figure(figsize=(10, 5))

# Plot vertical lines
    for i in range(len(methods) +1):
        plt.vlines(x[i] - offset, 0, is_values[i], linewidth=15, color = 'lightskyblue', label='In-sample' if i == 0 else "")
        plt.vlines(x[i] + offset, 0, oos_values[i], linewidth=15, color = 'orange', label='Out-of-sample' if i == 0 else "")
    plt.axhline(0, linestyle='--', color='red')
# Formatting
    plt.xticks(x, ['Benchmark'] + list(methods.keys()))
    plt.ylabel('Sharpe-ratio')
    if short:
        if cost == 0:
            plt.title('Sharpe ratio of long-short portfolios based on super-alphas and benchmark (equally-weighted all coins), without cost')
        else:
            plt.title('Sharpe ratio of long-short portfolios based on super-alphas and benchmark (equally weighted), with cost ' + str(100 * cost) + '%')
    else:
        if cost == 0:
            plt.title('Sharpe ratio of long-only portfolios based on super-alphas and benchmark (equally-weighted all coins), without cost')
        else:
            plt.title('Sharpe ratio of long-only portfolios based on super-alphas and benchmark (equally weighted), with cost ' + str(100 * cost) + '%')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return daily_return_dic

def cumulative_pnl_plot(daily_return_dic, initial_capital=1.0, name = ''):
    pnl_curve = {}
    mdd_dict = {}
    dd_curve_dict = {}

    for method in daily_return_dic:
        pnl_curve[method] = cumulative_pnl(daily_return_dic[method][-1], initial_capital = initial_capital)
    
        mdd, dd = max_drawdown(pnl_curve[method])
        mdd_dict[method] = mdd
        dd_curve_dict[method] = dd

# --------- Plot PnL ----------
    plt.figure(figsize=(10, 6))

    for method, curve in pnl_curve.items():
        plt.plot(curve, label=f"{method} (MDD={mdd_dict[method]:.2%})")

    plt.title("Cumulative PnL Comparison" + name)
    plt.xlabel("Time")
    plt.ylabel("Wealth")
    plt.legend()
    plt.grid(True)
    plt.show()