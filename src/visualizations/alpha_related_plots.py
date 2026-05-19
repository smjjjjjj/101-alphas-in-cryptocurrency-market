import matplotlib.pyplot as plt
import numpy as np
from src.metrics.alpha_metrics import IC, summaryic, turnover_timeseries


def plot_ic(alpha, ret, min_tstats = 1):
# A summary of each alpha's IC, including mean, standard deviation and t-statistics.
# Thumb's Rule: Choose those alpha, whose IC has an absolute value of t-statistics >= 1 and return
    alpha_ids = []
    means = []
    stds = []
    tstats = []
    output = []
# compute IC statistics
    for j in alpha:
        s = summaryic(IC(alpha[j], ret))
        alpha_ids.append(j)
        means.append(s[0])
        stds.append(s[1])
        tstats.append(s[2])
        if abs(s[2]) >= min_tstats:
            output.append(j)

    alpha_ids = np.array(alpha_ids)
    means = np.array(means)
    stds = np.array(stds)
    tstats = np.array(tstats)

# Plot mean:
    order_mean = np.argsort(means)[::-1]

    plt.figure()
    plt.bar(alpha_ids[order_mean].astype(str), means[order_mean])
    plt.title("Alpha IC mean ranking")
    plt.xlabel("Alpha ID")
    plt.ylabel("Mean IC")
    plt.xticks(rotation=90)
    plt.show()

# Plot std
    order_std = np.argsort(stds)[::-1]

    plt.figure()
    plt.bar(alpha_ids[order_std].astype(str), stds[order_std])
    plt.title("Alpha IC std ranking")
    plt.xlabel("Alpha ID")
    plt.ylabel("Std IC")
    plt.xticks(rotation=90)
    plt.show()

# Plot t-stat
    order_t = np.argsort(tstats)[::-1]

    plt.figure()
    plt.bar(alpha_ids[order_t].astype(str), tstats[order_t])
    plt.title("Alpha IC T-statistics ranking")
    plt.xlabel("Alpha ID")
    plt.ylabel("T-stat")
    plt.axhline(1, linestyle='--', color='red')
    plt.axhline(-1, linestyle='--', color='red')
    plt.xticks(rotation=90)
    plt.show()
    return output

def IS_OOS_IC_tstats(alpha_train_dic, alpha_test_dic,ret_train, ret_test, methods, chosen_alphas, criterium = 2):
    super_alphas_ic_tstats = {}
    ss_train = 0
    ss_test = 0
    for num in chosen_alphas:
        ic_train_tstat = summaryic(IC(alpha_train_dic[num], ret_train))[-1]
        ic_test_tstat = summaryic(IC(alpha_test_dic[num], ret_test))[-1]

        super_alphas_ic_tstats['alpha' + str(num)] = (np.abs(ic_train_tstat), np.abs(ic_test_tstat))
        ss_train += np.sign(ic_train_tstat) * alpha_train_dic[num]
        ss_test += np.sign(ic_train_tstat) * alpha_test_dic[num]
    
    super_alphas_ic_tstats['Naiive addiction'] = (np.abs(summaryic(IC(ss_train, ret_train))[-1]), np.abs(summaryic(IC(ss_test, ret_test))[-1]))

    for method in methods:
        super_alphas_ic_tstats[method] = (summaryic(IC(alpha_train_dic[method], ret_train))[-1], summaryic(IC(alpha_test_dic[method], ret_test))[-1])
    
    
    methods = list(super_alphas_ic_tstats.keys())
    is_values = [v[0] for v in super_alphas_ic_tstats.values()]
    oos_values = [v[1] for v in super_alphas_ic_tstats.values()]

# Positions
    x = np.arange(len(methods))
    offset = 0.1  # controls spacing within each method

    plt.figure(figsize=(8, 5))

# Plot vertical lines
    for i in range(len(methods)):
        plt.vlines(x[i] - offset, 0, is_values[i], linewidth=10, color = 'lightskyblue', label='In-sample' if i == 0 else "")
        plt.vlines(x[i] + offset, 0, oos_values[i], linewidth=10, color = 'orange', label='Out-of-sample' if i == 0 else "")
    plt.axhline(criterium, linestyle='--', color='red')
# Formatting
    plt.xticks(x, methods)
    plt.ylabel('t-statistics')
    plt.title('IS vs OOS t-statistics of ICs, alphas vs super-alphas')
    plt.legend()

    plt.tight_layout()
    plt.show()
    return super_alphas_ic_tstats

def alpha_decay(alpha_dic, ret, methods, duration = 8):
    ic_curve = {}
    for day in range(duration):
        for method in methods:
            if day == 0:
                ic_curve[method] = [summaryic(IC(alpha_dic[method], ret, day + 1))[-1]]
            else:
                ic_curve[method].append(summaryic(IC(alpha_dic[method], ret, day + 1))[-1])

    # X-axis (e.g., periods or horizons)
    x = np.arange(len(next(iter(ic_curve.values())))) + 1

    plt.figure(figsize=(8, 5))

# Plot each method as a line
    for label, values in ic_curve.items():
        plt.plot(x, values, marker='o', linewidth=2, label=label)

# Formatting
    plt.xlabel('Days')
    plt.ylabel('t-statistics')
    plt.title('Alpha decay: t-statistics of ICs across Super-alphas')
    plt.legend()
    plt.axhline(1.5, linestyle='--', color='red')

    plt.tight_layout()
    plt.show()
    return ic_curve

def ic_turnover_plot(alpha_dic, ret, methods):
    ic_turnover_plott = {}
    for method in methods:
        ic_turnover_plott[method] = (IC(alpha_dic[method], ret), turnover_timeseries(alpha_dic[method]))
    for method in methods:
        plt.figure(figsize=(6,6))
        ic = ic_turnover_plott[method][0]
        to = ic_turnover_plott[method][1]
        mean_ic = np.nanmean(ic)
        mean_to = np.nanmean(to)
        plt.scatter(to, ic, alpha=0.4)
        plt.axhline(mean_ic, linestyle='--')
        plt.axvline(mean_to, linestyle='--')    
        plt.text(
        np.nanmax(to),
        mean_ic,
        f"  {mean_ic:.4f}",
        va='bottom',
        color = 'red')

        plt.text(
        mean_to,
        np.nanmax(ic),
        f" {mean_to:.4f}",
        ha='left',
        color = 'red')
        plt.xlabel("Turnover")
        plt.ylabel("IC")
        plt.title(f"IC vs Turnover Regime Map ({method} super-alpha)")

        plt.grid(alpha=0.3)
        plt.show()
    return ic_turnover_plott