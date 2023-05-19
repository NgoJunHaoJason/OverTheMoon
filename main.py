import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from stonks.signals import get_signal

load_dotenv()


TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_BOT_BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
SEND_MESSAGE_URL = f"{TELEGRAM_BOT_BASE_URL}/sendMessage"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastAPI()
client = httpx.AsyncClient()


@app.get("/hello")
async def hello():
    logging.info("Hello")
    return "Hello"


@app.post("/")
async def webhook(request: Request):
    request_body = await request.json()
    logging.info(f"request: {request_body}")

    chat_id: int = request_body["message"]["chat"]["id"]
    symbol: str = request_body["message"]["text"]

    try:
        (
            fso_signal,
            pb_signal,
            pwma_signal,
            main_signal,
            last_close,
            date,
        ) = get_signal(symbol)

        text = (
            f"{symbol.upper()} is {main_signal} at ${last_close:.2f}"
            f" as of {date.strftime('%d %b %Y')}\n\n"
            f"fast stochastic oscillator:\n{fso_signal}\n\n"
            f"%B:\n{pb_signal}\n\n"
            f"price / weighted moving average:\n{pwma_signal}\n\n"
        )
    except Exception as error:
        text = f"Failed to get signal for '{symbol}'"
        logging.error(f"{text} due to {error}")

    bot_message = {"chat_id": chat_id, "text": text}
    logging.info(f"bot message: {bot_message}")

    result = await client.post(SEND_MESSAGE_URL, json=bot_message)
    logging.info(f"telegram post status: {result.status_code}")

    return bot_message
