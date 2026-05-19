# Import area
from src.data import data_loader, data_split
from src.visualizations import alpha_related_plots, other_plots, portfolio_related_plots
from src.metrics.alpha_calculations import normalreturn
from src.metrics.alpha_load import load_all_alphas
from src.super_alphas.alphas_combinations import equal_weight_combining, ic_weight_combining, corr_adj_weight_combining
#-----------------------------------------------------------------------------------------
# Hyperparameters
train_start_year = '2020'
train_end_year = '2024'

test_start_year = '2025'
test_end_year = '2025'

cost_level = 0.001

#---------------------------------------Start here----------------------------------------------
# Data import 
data = data_loader.load_data()

data_train, data_test = data_split.split_data(data, train_start_year, train_end_year, test_start_year, test_end_year)
# Plot the active coins through training dataset
other_plots.plot_active_coin(data_train, train_start_year, train_end_year)
other_plots.coins_lifecycle(data_train)

# Calculate all the 20 alpha realizations on the training and test dataset
alpha_train = load_all_alphas(data_train)
alpha_test = load_all_alphas(data_test)
ret_train = normalreturn(data_train)
ret_test = normalreturn(data_test)

# Choose alphas according to criterium: its IC's minimal tstatistics is 1 (in absolute value).
chosen_alphas = alpha_related_plots.plot_ic(alpha_train, ret_train, min_tstats = 1)

# Methods to combine chosen alphas into a super alpha
methods = {'Equally-weighted rank': equal_weight_combining, 
           'IC-weighted rank': ic_weight_combining,
           'Corr-weighted rank': corr_adj_weight_combining}

for method in methods:
    if method == 'Corr-weighted rank':
        alpha_train[method] = methods[method](alpha_train,chosen_alphas, ret_train, regularize=0.1)
        alpha_test[method] = methods[method](alpha_test,chosen_alphas, ret_test, regularize=0.1)
    else:
        alpha_train[method] = methods[method](alpha_train,chosen_alphas, ret_train)
        alpha_test[method] = methods[method](alpha_test,chosen_alphas, ret_test)

# Some metrics about this super alpha
alpha_related_plots.IS_OOS_IC_tstats(alpha_train, alpha_test, ret_train, ret_test, methods, chosen_alphas)

alpha_related_plots.alpha_decay(alpha_train, ret_train, methods)

alpha_related_plots.ic_turnover_plot(alpha_train, ret_train, methods)

# Build portfolio (long/short, with/without costs) according to this superalpha
# Calculate its daily return
daily_return_short_nocost = portfolio_related_plots.super_alphas_sharpe_ratio_plot(alpha_train, alpha_test, data_train, data_test, methods, short = True)

daily_return_long_nocost = portfolio_related_plots.super_alphas_sharpe_ratio_plot(alpha_train, alpha_test, data_train, data_test, methods, short = False)

daily_return_short_cost = portfolio_related_plots.super_alphas_sharpe_ratio_plot(alpha_train, alpha_test, data_train, data_test, methods, short = True, cost = cost_level)

# visualize the cumulative pnl plot in the test data.
portfolio_related_plots.cumulative_pnl_plot(daily_return_short_nocost, name = ' long-short without cost')

portfolio_related_plots.cumulative_pnl_plot(daily_return_short_cost, name = ' long-short with cost ' + str(100 * cost_level) + '%')








