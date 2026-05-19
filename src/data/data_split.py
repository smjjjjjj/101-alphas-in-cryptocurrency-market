import pandas as pd
def split_data(data, train_start_year, train_end_year, test_start_year, test_end_year):
    data_t = data.loc[(train_start_year + '-01-01'):(train_end_year + '-12-31')]
    all_dates = data_t.index.get_level_values("date").unique()
    all_symbols = data_t.index.get_level_values("symbol").unique()

    full_index = pd.MultiIndex.from_product(
    [all_dates, all_symbols],
    names=["date", "symbol"])
    data_train = data_t.reindex(full_index)

    data_te = data.loc[(test_start_year + '-01-01'):(test_end_year + '-12-31')]
    all_date_test =data_te.index.get_level_values("date").unique()
    all_symbols_test = data_te.index.get_level_values("symbol").unique()

    full_index = pd.MultiIndex.from_product(
    [all_date_test, all_symbols_test],
    names=["date", "symbol"])
    data_test = data_te.reindex(full_index)
    return data_train, data_test