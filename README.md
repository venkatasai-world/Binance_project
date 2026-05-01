# Binance Futures Testnet Trading Bot (Python)

This project is a simplified Python trading bot for the Binance USDT-M Futures Testnet.
It supports `BUY`/`SELL` with `MARKET` and `LIMIT` order types via CLI, with input validation,
structured modules, and API logging.

## Features

- Place `MARKET` and `LIMIT` orders on Binance Futures Testnet
- Supports both `BUY` and `SELL`
- CLI input validation (`symbol`, `side`, `order type`, `quantity`, `price`)
- Clear request/response terminal output
- Logs API requests, responses, and errors to `logs/trading_bot.log`
- Handles invalid input, API failures, and network errors

## Project Structure

```text
.
├── bot
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── cli.py
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export your Binance testnet credentials as environment variables:

```powershell
$env:BINANCE_API_KEY="your_api_key"
$env:BINANCE_API_SECRET="your_api_secret"
```

Base URL used by this app: `https://testnet.binancefuture.com`

## Usage Examples

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 90000
```

## Output

The CLI prints:

- order request summary
- order response details (`orderId`, `status`, `executedQty`, `avgPrice`)
- success/failure message

## Logs

All API request/response/error logs are written to:

- `logs/trading_bot.log`

Run at least one successful MARKET and one successful LIMIT order to generate the two required log examples for submission.

## Assumptions

- You are using Binance Futures Testnet credentials (not production keys).
- Symbol and quantity precision are valid for the selected instrument.
- API credentials are supplied via environment variables for safety.

