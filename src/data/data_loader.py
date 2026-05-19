import pandas as pd
import glob
# Use DFS to import every csv.file data from data/raw/*
# Each csv file represents one coin.
def load_data():

    files = glob.glob("data/raw/*.csv")

    dfs = []

    for file in files:
    
    # skip bad header rows by searching for real header line
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

    # find the row where actual header starts
        header_idx = None
        for i, line in enumerate(lines):
            if "Date" in line and "Open" in line and "Close" in line:
                header_idx = i
                break

        if header_idx is None:
            continue  # skip broken file

        # read correctly
        df = pd.read_csv(file, skiprows=header_idx)

    # normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

    # keep only required columns (ignore tradecount, etc.)
        required = ["date", "symbol", "open", "high", "low", "close"]

    # handle volume column name variations
        volume_col = None
        for c in df.columns:
            if "volume usdt" in c.lower() or "volume usd" in c.lower():
                volume_col = c

        if volume_col is None:
            continue  # skip if no volume

        df = df[required + [volume_col]]

        df = df.rename(columns={volume_col: "volume"})

    # convert date
        df["date"] = pd.to_datetime(df["date"])

    # drop rows where close is missing (extra safety)
        df = df.dropna(subset=["close"])

        dfs.append(df)

# combine all coins
    data = pd.concat(dfs, ignore_index=True)

# set index
    data = data.set_index(["date", "symbol"]).sort_index()
    return data