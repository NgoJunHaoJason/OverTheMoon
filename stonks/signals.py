import datetime as dt
from enum import Enum

import pandas as pd
import yfinance as yf

from .indicators import (
    fast_stochastic_oscillator,
    percent_b,
    price_weighted_moving_average_ratio,
)


def get_signal(symbol: str) -> tuple[str, str, str, str, float, dt.date]:
    stock = yf.Ticker(symbol)
    history = stock.history(period="2mo")

    # already adjusted for stock splits (and dividends?)
    close = history["Close"]
    high = history["High"]
    low = history["Low"]

    fso_value = fast_stochastic_oscillator(close, high, low)
    pb_value = percent_b(close)
    pwma_value = price_weighted_moving_average_ratio(close)

    fso_signal = _get_fso_signal(fso_value)
    pb_signal = _get_pb_signal(pb_value)
    pwma_signal = _get_pwma_signal(pwma_value)

    main_signal = _get_main_signal(fso_value, pb_value, pwma_value)
    last_close = close.values[-1]

    dates = pd.DatetimeIndex(history.index)
    date: dt.date = dates.date[-1]

    return fso_signal, pb_signal, pwma_signal, main_signal, last_close, date


def _get_fso_signal(fso_value: float) -> str:
    if fso_value > _FastStochasticOscillator.OVERBOUGHT_THRESHOLD.value:
        signal = (
            f"{fso_value:.3f}"
            f" > {_FastStochasticOscillator.OVERBOUGHT_THRESHOLD.value}"
        )
    elif fso_value < _FastStochasticOscillator.OVERSOLD_THRESHOLD.value:
        signal = (
            f"{fso_value:.3f}"
            f" < {_FastStochasticOscillator.OVERSOLD_THRESHOLD.value}"
        )
    else:
        signal = (
            f"{_FastStochasticOscillator.OVERSOLD_THRESHOLD.value}"
            f" <= {fso_value:.3f}"
            f" <= {_FastStochasticOscillator.OVERBOUGHT_THRESHOLD.value}"
        )

    return signal


def _get_pb_signal(pb_value: float) -> str:
    if pb_value > _PercentB.OVERBOUGHT_THRESHOLD.value:
        signal = f"{pb_value:.3f} > {_PercentB.OVERBOUGHT_THRESHOLD.value}"
    elif pb_value < _PercentB.OVERSOLD_THRESHOLD.value:
        signal = f"{pb_value:.3f} < {_PercentB.OVERSOLD_THRESHOLD.value}"
    else:
        signal = (
            f"{_PercentB.OVERSOLD_THRESHOLD.value}"
            f" <= {pb_value:.3f}"
            f" <= {_PercentB.OVERBOUGHT_THRESHOLD.value}"
        )

    return signal


def _get_pwma_signal(pwma_value: float) -> str:
    if pwma_value > _PriceWeightedMovingAverageRatio.OVERBOUGHT_THRESHOLD.value:
        signal = (
            f"{pwma_value:.3f}"
            f" > {_PriceWeightedMovingAverageRatio.OVERBOUGHT_THRESHOLD.value}"
        )
    elif pwma_value < _PriceWeightedMovingAverageRatio.OVERSOLD_THRESHOLD.value:
        signal = (
            f"{pwma_value:.3f}"
            f" < {_PriceWeightedMovingAverageRatio.OVERSOLD_THRESHOLD.value}"
        )
    else:
        signal = (
            f"{_PriceWeightedMovingAverageRatio.OVERSOLD_THRESHOLD.value}"
            f" <= {pwma_value:.3f}"
            f" <= {_PriceWeightedMovingAverageRatio.OVERBOUGHT_THRESHOLD.value}"
        )

    return signal


def _get_main_signal(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> str:
    if _is_overbought(fso_value, pb_value, pwma_value):
        signal = "overbought"
    elif _is_oversold(fso_value, pb_value, pwma_value):
        signal = "oversold"
    else:
        signal = "neither overbought nor oversold"

    return signal


def _is_overbought(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> bool:
    return (
        (fso_value > _FastStochasticOscillator.OVERBOUGHT_THRESHOLD.value)
        and (pb_value > _PercentB.OVERBOUGHT_THRESHOLD.value)
        and (pwma_value > _PriceWeightedMovingAverageRatio.OVERBOUGHT_THRESHOLD.value)
    )


def _is_oversold(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> bool:
    return (
        (fso_value < _FastStochasticOscillator.OVERSOLD_THRESHOLD.value)
        and (pb_value < _PercentB.OVERSOLD_THRESHOLD.value)
        and (pwma_value < _PriceWeightedMovingAverageRatio.OVERSOLD_THRESHOLD.value)
    )


class _FastStochasticOscillator(Enum):
    OVERBOUGHT_THRESHOLD = 0.8
    OVERSOLD_THRESHOLD = 0.2


class _PercentB(Enum):
    OVERBOUGHT_THRESHOLD = 1.0
    OVERSOLD_THRESHOLD = 0.0


class _PriceWeightedMovingAverageRatio(Enum):
    OVERBOUGHT_THRESHOLD = 1.05
    OVERSOLD_THRESHOLD = 0.95
