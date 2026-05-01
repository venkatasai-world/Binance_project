import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import requests

from bot.client import BinanceClient
from bot.logging_config import configure_logging
from bot.orders import build_order_payload, place_order
from bot.validators import (
    normalize_symbol,
    validate_order_type,
    validate_positive_decimal,
    validate_side,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Place BUY/SELL MARKET/LIMIT orders on Binance Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Order price (required for LIMIT)")
    return parser.parse_args()


def load_dotenv_file(dotenv_path: str = ".env") -> None:
    """Load BINANCE keys from a local .env file when present."""
    path = Path(dotenv_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in {"BINANCE_API_KEY", "BINANCE_API_SECRET"} and not os.getenv(key):
            os.environ[key] = value


def load_credentials() -> tuple[str, str]:
    load_dotenv_file()
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        raise ValueError(
            "Missing credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
            "in env or .env file."
        )
    return api_key, api_secret


def validate_inputs(args: argparse.Namespace) -> tuple[str, str, str, str, Optional[str]]:
    symbol = normalize_symbol(args.symbol)
    side = validate_side(args.side)
    order_type = validate_order_type(args.order_type)
    quantity = validate_positive_decimal("quantity", args.quantity)
    price = None

    if order_type == "LIMIT":
        if args.price is None:
            raise ValueError("price is required when --order-type LIMIT")
        price = validate_positive_decimal("price", args.price)
    elif args.price is not None:
        raise ValueError("price must not be sent for MARKET orders")

    return symbol, side, order_type, quantity, price


def main() -> int:
    configure_logging()
    try:
        args = parse_args()
        symbol, side, order_type, quantity, price = validate_inputs(args)
        api_key, api_secret = load_credentials()

        request_summary = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "price": price,
        }
        print("Order Request Summary:")
        for key, value in request_summary.items():
            if value is not None:
                print(f"  {key}: {value}")

        client = BinanceClient(api_key=api_key, api_secret=api_secret)
        payload = build_order_payload(symbol, side, order_type, quantity, price)
        response = place_order(client, payload)

        print("\nOrder Response:")
        print(f"  orderId: {response.get('orderId')}")
        print(f"  status: {response.get('status')}")
        print(f"  executedQty: {response.get('executedQty')}")
        print(f"  avgPrice: {response.get('avgPrice', 'N/A')}")
        print("\nSuccess: order placed on Binance Futures Testnet.")
        return 0

    except ValueError as exc:
        print(f"Input Error: {exc}")
        return 2
    except requests.exceptions.RequestException as exc:
        print(f"API/Network Error: {exc}")
        return 3
    except Exception as exc:  # pragma: no cover - defensive fallback
        print(f"Unexpected Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

