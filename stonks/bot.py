import logging

from deta import _Base

from stonks.signals import get_signal
from stonks.watchlist import show_watchlist, unwatch_stocks, watch_stocks


def check_stock_signal(symbol: str) -> str:
    try:
        (
            fso_signal,
            pb_signal,
            pwma_signal,
            main_signal,
            last_close,
            date,
        ) = get_signal(symbol)

        outgoing_text = (
            f"{symbol.upper()} is {main_signal} at ${last_close:.2f}"
            f" as of {date.strftime('%d %b %Y')}\n\n"
            f"fast stochastic oscillator:\n{fso_signal}\n\n"
            f"%B:\n{pb_signal}\n\n"
            f"price / weighted moving average:\n{pwma_signal}\n\n"
        )
    except Exception as error:
        outgoing_text = f"Failed to retrieve data for '{symbol}'"
        logging.error(f"{outgoing_text} due to {error}")

    return outgoing_text


def follow_command(
    deta_base: _Base,
    chat_id: str,
    command: str,
    params: list[str],
) -> str:
    if command == "/list":
        outgoing_text = show_watchlist(deta_base, chat_id)

    elif command == "/watch":
        outgoing_text = watch_stocks(deta_base, chat_id, symbols=params)

    elif command == "/unwatch":
        outgoing_text = unwatch_stocks(deta_base, chat_id, symbols=params)

    else:
        outgoing_text = f"'{command}' is not a valid command"

    return outgoing_text
