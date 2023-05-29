import logging

import yfinance as yf
from deta import Deta
from fastapi import HTTPException

from stonks.commands import Command


def show_watchlist(deta: Deta, chat_id: str) -> str:
    try:
        watched_symbols = get_watched_symbols(deta, chat_id)

        if watched_symbols:
            symbols_text = "\n".join(watched_symbols)
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


def get_watched_symbols(deta: Deta, chat_id: str) -> list[str]:
    watchlist_base = deta.Base("watchlist")
    fetch_response = watchlist_base.fetch({"chat_id": chat_id})
    watched_tickers = fetch_response.items
    return sorted([stock["symbol"] for stock in watched_tickers])


def watch_stocks(deta: Deta, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

    if symbols:
        try:
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                history = ticker.history(period="2mo")

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

            watchlist_base = deta.Base("watchlist")
            watchlist_base.put_many(watched_stocks)
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


def unwatch_stocks(deta: Deta, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

    if symbols:
        try:
            watchlist_base = deta.Base("watchlist")
            for symbol in symbols:
                watchlist_base.delete(_get_deta_base_key(chat_id, symbol))

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
