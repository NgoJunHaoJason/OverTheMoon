# Over the Moon

A telegram bot that tells you if a stock is overbought or oversold

With this, hopefully your returns (and you!) would be over the moon 🚀🌔

## Prerequisites

- Python 3.10
- render.com integration

## Set-up

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

## Run

```bash
source venv/bin/activate
python main.py
```

## Deploy

1. Push to main branch
2. Set webhook by calling: `https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={APP_BASE_URL}`
3. Confirm that webhook was set successfully by calling: `https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/getWebhookInfo`

## Usage

1. Start a chat session with [OverTheMoonBot](https://t.me/OverTheMoonBot) on Telegram
2. Enter a stock symbol (e.g. `SPY`) to check if it is overbought or oversold
