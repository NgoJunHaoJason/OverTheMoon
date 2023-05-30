# Over the Moon

A telegram bot that tells you if a stock is overbought or oversold

With this, hopefully your returns (and you!) would be over the moon 🚀🌔

## Usage

1. Start a chat session with [OverTheMoonBot](https://t.me/OverTheMoonBot) on Telegram
2. Enter a stock symbol (e.g. `SPY`) to check if it is overbought or oversold

## Development Prerequisites

Python 3.10

## Set-up

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

Create a `.env` file in the project root directory with the following keys:

```
DETA_PROJECT_KEY=<your_key>
TELEGRAM_API_TOKEN=<your_token>
```

## Run

```bash
source venv/bin/activate
uvicorn main:app --reload
```

## Deploy

1. Push to main branch
2. Set webhook by calling: `https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={APP_BASE_URL}`
3. Confirm that webhook was set successfully by calling: `https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/getWebhookInfo`

## Render integration

under Environment:

- set Python version in environment variables
- set .env in secret files

under Settings:

- set `uvicorn main:app --host 0.0.0.0 --port 10000` as start command

## Deta Base integration

under Collections settings:

- create new data keys

## cron-job integration

TODO

## TODO

1. notification
2. /backtest
3. codecov
