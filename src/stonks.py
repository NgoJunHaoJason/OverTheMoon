import yfinance as yf

from .indicators import fast_stochastic_oscillator, percent_b, price_wma_ratio


def get_signal(symbol: str) -> tuple[str, float, float, float, float]:
    stock = yf.Ticker(symbol)

    history = stock.history(period="2mo")

    close = history["Close"]
    high = history["High"]
    low = history["Low"]

    fso = fast_stochastic_oscillator(close, high, low)
    pb = percent_b(close)
    pwma = price_wma_ratio(close)

    if _is_overbought(fso, pb, pwma):
        signal = "overbought"
    elif _is_oversold(fso, pb, pwma):
        signal = "oversold"
    else:
        signal = "neither overbought nor oversold"

    return signal, close.values[-1], fso, pb, pwma


def _is_overbought(
    fast_stochastic_oscillator: float,
    percent_b: float,
    price_wma_ratio: float,
    fso_overbought_threshold: float = 0.8,
    pb_overbought_threshold: float = 1,
    pwma_overbought_threshold: float = 1.05,
) -> bool:
    return (
        (fast_stochastic_oscillator > fso_overbought_threshold)
        and (percent_b > pb_overbought_threshold)
        and (price_wma_ratio > pwma_overbought_threshold)
    )


def _is_oversold(
    fast_stochastic_oscillator: float,
    percent_b: float,
    price_wma_ratio: float,
    fso_oversold_threshold: float = 0.2,
    pb_oversold_threshold: float = 0,
    pwma_oversold_threshold: float = 0.95,
) -> bool:
    return (
        (fast_stochastic_oscillator < fso_oversold_threshold)
        and (percent_b < pb_oversold_threshold)
        and (price_wma_ratio < pwma_oversold_threshold)
    )
