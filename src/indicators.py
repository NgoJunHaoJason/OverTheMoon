import pandas as pd


def fast_stochastic_oscillator(
    close: pd.Series,
    high: pd.Series,
    low: pd.Series,
    window_num_days: int = 18,
) -> float:
    highest_high = high.rolling(window_num_days).max()
    lowest_low = low.rolling(window_num_days).min()

    percent_k = (close - lowest_low) / (highest_high - lowest_low)
    percent_d = percent_k.rolling(3).mean()

    return percent_d.values[-1]


def percent_b(stock_price: pd.Series) -> float:
    upper_band, lower_band = _bollinger_bands(stock_price)
    return ((stock_price - lower_band) / (upper_band - lower_band)).values[-1]


def _bollinger_bands(
    stock_price: pd.Series,
    num_stds_away: int = 2,
    window_num_days: int = 21,
) -> tuple[pd.Series, pd.Series]:
    rolling = stock_price.rolling(window_num_days)

    simple_moving_average = rolling.mean()
    band_distance = num_stds_away * rolling.std()

    upper_band = simple_moving_average + band_distance
    lower_band = simple_moving_average - band_distance

    return upper_band, lower_band


def price_wma_ratio(stock_price: pd.Series) -> float:
    return (stock_price / _weighted_moving_average(stock_price)).values[-1]


def _weighted_moving_average(
    stock_price: pd.Series,
    window_num_days: int = 22,
) -> pd.Series:
    weights = pd.Series(range(1, window_num_days + 1))
    total_weight: float = weights.sum()

    return stock_price.rolling(window_num_days).apply(
        lambda x: _weighted_average(x, weights, total_weight),
        raw=True,
    )


def _weighted_average(
    stock_price: pd.Series,
    weights: pd.Series,
    total_weight: float,
) -> pd.Series:
    return (stock_price * weights).sum() / total_weight
