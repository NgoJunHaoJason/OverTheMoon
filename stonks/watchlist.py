import logging

import yfinance as yf
from deta import _Base
from fastapi import HTTPException

from stonks.commands import Command


def show_watchlist(deta_base: _Base, chat_id: str) -> str:
    try:
        symbols = get_watched_symbols(deta_base, chat_id)

        if symbols:
            symbols_text = "\n".join(symbols)
            outgoing_text = f"Your watchlist:\n{symbols_text}"
        else:
            outgoing_text = (
                "Your watchlist is empty.\n"
                f"Start watching tickers with the {Command.LIST} command."
            )

    except Exception as error:
        outgoing_text = f"Failed to fetch your watchlist due to {error}"
        logging.error(outgoing_text)

    return outgoing_text


def get_watched_symbols(deta_base: _Base, chat_id: str) -> list[str]:
    fetch_response = deta_base.fetch({"chat_id": chat_id})
    watched_stocks = fetch_response.items
    return sorted([stock["symbol"] for stock in watched_stocks])


def watch_stocks(deta_base: _Base, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

    if symbols:
        try:
            for symbol in symbols:
                stock = yf.Ticker(symbol)
                history = stock.history(period="2mo")

                if history.empty:
                    raise HTTPException(404, f"'{symbol}' not found")

            watched_stocks = [
                {
                    "chat_id": chat_id,
                    "symbol": symbol,
                    "key": _get_deta_base_key(chat_id, symbol),
                }
                for symbol in symbols
            ]

            deta_base.put_many(watched_stocks)
            outgoing_text = f"Added {symbols} to watchlist"

        except Exception as error:
            outgoing_text = f"Failed to add {symbols} to watchlist due to {error}"
            logging.error(outgoing_text)
    else:
        outgoing_text = (
            "No ticker was given.\n"
            f"Please use the {Command.WATCH} command in the following form:\n"
            f"{Command.WATCH} <ticker>"
        )

    return outgoing_text


def unwatch_stocks(deta_base: _Base, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

    if symbols:
        try:
            for symbol in symbols:
                deta_base.delete(_get_deta_base_key(chat_id, symbol))

            outgoing_text = f"Removed {symbols} from watchlist"

        except Exception as error:
            outgoing_text = f"Failed to remove {symbols} from watchlist due to {error}"
            logging.error(outgoing_text)
    else:
        outgoing_text = (
            "No ticker was given.\n"
            f"Please use the {Command.UNWATCH} command in the following form:\n"
            f"{Command.UNWATCH} <ticker>"
        )

    return outgoing_text


def _get_deta_base_key(chat_id: str, symbol: str) -> str:
    return f"{chat_id}-{symbol}".upper()
