from typing import Dict, Optional

from bot.client import BinanceClient


def build_order_payload(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
) -> Dict[str, str]:
    payload: Dict[str, str] = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }
    if order_type == "LIMIT":
        if not price:
            raise ValueError("price is required for LIMIT orders")
        payload["price"] = price
        payload["timeInForce"] = "GTC"
    return payload


def place_order(client: BinanceClient, payload: Dict[str, str]) -> Dict[str, str]:
    return client.place_order(payload)

