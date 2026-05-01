from decimal import Decimal, InvalidOperation


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    normalized = symbol.strip().upper()
    if not normalized or not normalized.isalnum():
        raise ValueError("symbol must be alphanumeric, e.g. BTCUSDT")
    return normalized


def validate_side(side: str) -> str:
    normalized = side.strip().upper()
    if normalized not in VALID_SIDES:
        raise ValueError("side must be BUY or SELL")
    return normalized


def validate_order_type(order_type: str) -> str:
    normalized = order_type.strip().upper()
    if normalized not in VALID_ORDER_TYPES:
        raise ValueError("order_type must be MARKET or LIMIT")
    return normalized


def validate_positive_decimal(field_name: str, value: str) -> str:
    try:
        decimal_value = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{field_name} must be a valid decimal number") from exc

    if decimal_value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    # Return normalized string representation expected by API.
    return format(decimal_value, "f")

