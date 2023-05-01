import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from src.stonks import get_signal

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


@app.get("/")
async def hello():
    logging.info("Hello")
    return "Hello"


@app.post("/")
async def webhook(request: Request):
    request_body = await request.json()
    logging.info(f"request:\n{request_body}")

    chat_id = request_body["message"]["chat"]["id"]
    symbol = request_body["message"]["text"]

    try:
        signal, close, fso, pb, pwma = get_signal(symbol)
        text = (
            f"{symbol} is {signal} at {close:.2f}\n"
            f"fast stochastic oscillator: {fso:.2f}\n"
            f"%B: {pb:.2f}\n"
            f"price / weighted moving average: {pwma:.2f}\n"
        )
    except Exception as error:
        text = f"Failed to get signal for '{symbol}'"
        logging.error(f"{text} due to {error}")

    bot_message = {"chat_id": chat_id, "text": text}
    logging.info(f"bot message:\n{bot_message}")

    response = await client.post(SEND_MESSAGE_URL, json=bot_message)
    logging.info(f"response:\n{response}")

    return bot_message
