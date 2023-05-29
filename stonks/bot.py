import logging

from deta import Deta

from stonks.commands import Command
from stonks.signals import get_signals, show_signals
from stonks.watchlist import (
    check_watchlist_signals,
    show_watchlist,
    unwatch_stocks,
    watch_stocks,
)


def check_stock_signal(symbol: str) -> str:
    try:
        signals = get_signals(symbol)
        outgoing_text = show_signals(symbol, **signals)

    except Exception as error:
        outgoing_text = f"Failed to retrieve data for '{symbol}' due to {error}"
        logging.error(outgoing_text)

    return outgoing_text


def follow_command(
    deta: Deta,
    chat_id: str,
    command: str,
    params: list[str],
) -> str:
    if command == Command.CHECK:
        outgoing_text = check_watchlist_signals(deta, chat_id)
    elif command == Command.LIST:
        outgoing_text = show_watchlist(deta, chat_id)
    elif command == Command.WATCH:
        outgoing_text = watch_stocks(deta, chat_id, symbols=params)
    elif command == Command.UNWATCH:
        outgoing_text = unwatch_stocks(deta, chat_id, symbols=params)
    else:
        outgoing_text = f"'{command}' is not a valid command"

    return outgoing_text
