import logging

from stonks.signals import get_signal


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


def follow_command(chat_id: int, command: str, params: list[str]) -> str:
    if command == "/list":
        outgoing_text = _show_watchlist(chat_id)

    elif command == "/watch":
        outgoing_text = _watch_stocks(chat_id, symbols=params)

    elif command == "/unwatch":
        outgoing_text = _unwatch_stocks(chat_id, symbols=params)

    else:
        outgoing_text = f"'{command}' is not a valid command"

    return outgoing_text


def _show_watchlist(chat_id: int):
    outgoing_text = f"showed watchlist to {chat_id}"

    return outgoing_text


def _watch_stocks(chat_id: int, symbols: list[str]):
    symbols_text = ", ".join(symbols)
    outgoing_text = f"added {symbols_text} to watchlist for {chat_id}"

    return outgoing_text


def _unwatch_stocks(chat_id: int, symbols: list[str]):
    symbols_text = ", ".join(symbols)
    outgoing_text = f"removed {symbols_text} from watchlist for {chat_id}"

    return outgoing_text
