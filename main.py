import logging
import os

import httpx
from deta import Deta
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from stonks.bot import check_stock_signal, follow_command

load_dotenv()

DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_BOT_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}"
SEND_MESSAGE_URL = f"{TELEGRAM_BOT_BASE_URL}/sendMessage"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = FastAPI()
client = httpx.AsyncClient()
deta = Deta(DETA_PROJECT_KEY)


@app.get("/hello")
async def hello():
    logging.info("Hello")
    return "Hello"


@app.post("/")
async def webhook(request: Request):
    request_body = await request.json()
    logging.info(f"request: {request_body}")

    chat_id: int = request_body["message"]["chat"]["id"]
    incoming_text: str = request_body["message"]["text"]

    if incoming_text.startswith("/"):
        command, *params = incoming_text.split()
        outgoing_text = follow_command(deta, str(chat_id), command, params)
    else:
        outgoing_text = check_stock_signal(symbol=incoming_text)

    bot_message = {"chat_id": chat_id, "text": outgoing_text}
    logging.info(f"bot message: {bot_message}")

    result = await client.post(SEND_MESSAGE_URL, json=bot_message)
    logging.info(f"telegram post status: {result.status_code}")

    return bot_message
