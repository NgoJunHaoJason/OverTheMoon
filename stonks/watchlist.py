import logging

import yfinance as yf
from deta import _Base
from fastapi import HTTPException


def show_watchlist(deta_base: _Base, chat_id: str) -> str:
    try:
        fetch_response = deta_base.fetch({"chat_id": chat_id})
        watched_stocks: list[dict[str, str]] = fetch_response.items

        symbols = sorted([stock["symbol"] for stock in watched_stocks])
        symbols_text = "\n".join(symbols)

        outgoing_text = f"Your watchlist:\n{symbols_text}"

    except Exception as error:
        outgoing_text = "Failed to fetch watchlist"
        logging.error(f"{outgoing_text} due to {error}")

    return outgoing_text


def watch_stocks(deta_base: _Base, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

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
        outgoing_text = f"Failed to add {symbols} to watchlist"
        logging.error(f"{outgoing_text} due to {error}")

    return outgoing_text


def unwatch_stocks(deta_base: _Base, chat_id: str, symbols: list[str]) -> str:
    symbols = [symbol.upper() for symbol in symbols]

    try:
        for symbol in symbols:
            deta_base.delete(_get_deta_base_key(chat_id, symbol))

        outgoing_text = f"Removed {symbols} from watchlist"

    except Exception as error:
        outgoing_text = f"Failed to remove {symbols} from watchlist"
        logging.error(f"{outgoing_text} due to {error}")

    return outgoing_text


def _get_deta_base_key(chat_id: str, symbol: str) -> str:
    return f"{chat_id}-{symbol}".upper()
