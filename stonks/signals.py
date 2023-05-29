import datetime as dt
from enum import Enum
from typing import Any

import pandas as pd
import yfinance as yf
from fastapi import HTTPException

from stonks.indicators import (
    FastStochasticOscillatorThreshold,
    PercentBThreshold,
    PriceWeightedMovingAverageRatioThreshold,
    fast_stochastic_oscillator,
    percent_b,
    price_weighted_moving_average_ratio,
)


def show_signals(
    symbol: str,
    main_signal: str,
    fso_signal: str,
    pb_signal: str,
    pwma_signal: str,
    last_close: float,
    date: dt.date,
) -> str:
    return (
        f"{symbol.upper()} is {main_signal} at ${last_close:.2f}"
        f" as of {date.strftime('%d %b %Y')}\n\n"
        f"fast stochastic oscillator:\n{fso_signal}\n\n"
        f"%B:\n{pb_signal}\n\n"
        f"price / weighted moving average:\n{pwma_signal}\n\n"
    )


def get_signals(symbol: str) -> dict[str, Any]:
    stock = yf.Ticker(symbol)
    history = stock.history(period="2mo")

    if history.empty:
        raise HTTPException(404, f"'{symbol}' not found")

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
    last_close = float(close.values[-1])

    dates = pd.DatetimeIndex(history.index)
    date: dt.date = dates.date[-1]

    return {
        "main_signal": main_signal,
        "fso_signal": fso_signal,
        "pb_signal": pb_signal,
        "pwma_signal": pwma_signal,
        "last_close": last_close,
        "date": date,
    }


def _get_main_signal(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> str:
    if _is_overbought(fso_value, pb_value, pwma_value):
        signal = MainSignal.OVERBOUGHT
    elif _is_oversold(fso_value, pb_value, pwma_value):
        signal = MainSignal.OVERSOLD
    else:
        signal = MainSignal.NEITHER

    return str(signal)


def _is_overbought(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> bool:
    return (
        (fso_value > FastStochasticOscillatorThreshold.OVERBOUGHT)
        and (pb_value > PercentBThreshold.OVERBOUGHT)
        and (pwma_value > PriceWeightedMovingAverageRatioThreshold.OVERBOUGHT)
    )


def _is_oversold(
    fso_value: float,
    pb_value: float,
    pwma_value: float,
) -> bool:
    return (
        (fso_value < FastStochasticOscillatorThreshold.OVERSOLD)
        and (pb_value < PercentBThreshold.OVERSOLD)
        and (pwma_value < PriceWeightedMovingAverageRatioThreshold.OVERSOLD)
    )


def _get_fso_signal(fso_value: float) -> str:
    if fso_value > FastStochasticOscillatorThreshold.OVERBOUGHT:
        signal = (
            f"{FastStochasticOscillatorThreshold.OVERBOUGHT}" f" < [{fso_value:.3f}]"
        )
    elif fso_value < FastStochasticOscillatorThreshold.OVERSOLD:
        signal = f"[{fso_value:.3f}]" f" < {FastStochasticOscillatorThreshold.OVERSOLD}"
    else:
        signal = (
            f"{FastStochasticOscillatorThreshold.OVERSOLD}"
            f" <= [{fso_value:.3f}]"
            f" <= {FastStochasticOscillatorThreshold.OVERBOUGHT}"
        )

    return signal


def _get_pb_signal(pb_value: float) -> str:
    if pb_value > PercentBThreshold.OVERBOUGHT:
        signal = f"{PercentBThreshold.OVERBOUGHT} < [{pb_value:.3f}]"
    elif pb_value < PercentBThreshold.OVERSOLD:
        signal = f"[{pb_value:.3f}] < {PercentBThreshold.OVERSOLD}"
    else:
        signal = (
            f"{PercentBThreshold.OVERSOLD}"
            f" <= [{pb_value:.3f}]"
            f" <= {PercentBThreshold.OVERBOUGHT}"
        )

    return signal


def _get_pwma_signal(pwma_value: float) -> str:
    if pwma_value > PriceWeightedMovingAverageRatioThreshold.OVERBOUGHT:
        signal = (
            f"{PriceWeightedMovingAverageRatioThreshold.OVERBOUGHT}"
            f" < [{pwma_value:.3f}]"
        )
    elif pwma_value < PriceWeightedMovingAverageRatioThreshold.OVERSOLD:
        signal = (
            f"[{pwma_value:.3f}]"
            f" < {PriceWeightedMovingAverageRatioThreshold.OVERSOLD}"
        )
    else:
        signal = (
            f"{PriceWeightedMovingAverageRatioThreshold.OVERSOLD}"
            f" <= [{pwma_value:.3f}]"
            f" <= {PriceWeightedMovingAverageRatioThreshold.OVERBOUGHT}"
        )

    return signal


class MainSignal(Enum):
    OVERBOUGHT = "overbought"
    OVERSOLD = "oversold"
    NEITHER = "neither overbought nor oversold"

    def __eq__(self, __value: object) -> bool:
        return self.value == str(__value)

    def __str__(self) -> str:
        return self.value
