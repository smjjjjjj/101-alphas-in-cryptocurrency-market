import matplotlib.pyplot as plt
import pandas as pd

def plot_active_coin(data, start_year, end_year):
    valid_counts = (
    data["close"]
    .notna()
    .groupby(level="date")
    .sum()
)

# --- 3. Plot ---
    plt.figure(figsize=(12, 6))
    plt.plot(valid_counts.index, valid_counts.values)

    plt.title("Number of Active Coins Over Time from " + start_year + " to " + end_year)
    plt.xlabel("Date")
    plt.ylabel("Number of Coins with Valid Prices")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

def coins_lifecycle(data):
    # Plot the lifecycle of each coin accordingly.
    close = data["close"]

# Compute lifecycle
    lifecycle = close.groupby("symbol").apply(
    lambda x: pd.Series({
        "start": x.first_valid_index()[0] if x.first_valid_index() else None,
        "end": x.last_valid_index()[0] if x.last_valid_index() else None
    })).unstack()

# Drop coins that never had data (just in case)
    lifecycle = lifecycle.dropna()
# Sort by start date (nicer visualization)
    lifecycle = lifecycle.sort_values("start")

    plt.figure(figsize=(12, 8))

    for i, (symbol, row) in enumerate(lifecycle.iterrows()):
        plt.plot([row["start"], row["end"]], [i, i])

    plt.yticks(range(len(lifecycle)), lifecycle.index)
    plt.xlabel("Date")
    plt.ylabel("Coin")
    plt.title("Crypto Coin Lifecycles" )
    plt.grid(True)
    plt.tight_layout()
    plt.show()

