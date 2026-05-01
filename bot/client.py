import hashlib
import hmac
import logging
import time
from typing import Any, Dict
from urllib.parse import urlencode

import requests


class BinanceClient:
    """Thin Binance Futures Testnet REST client."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: int = 15,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def _sign(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _signed_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        signed = dict(params)
        signed["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(signed, doseq=True)
        signed["signature"] = self._sign(query_string)
        return signed

    def place_order(self, order_payload: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = "/fapi/v1/order"
        url = f"{self.base_url}{endpoint}"
        params = self._signed_params(order_payload)
        headers = {"X-MBX-APIKEY": self.api_key}

        self.logger.info("POST %s request=%s", endpoint, order_payload)
        try:
            response = requests.post(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            self.logger.info("POST %s status=%s", endpoint, response.status_code)
            response.raise_for_status()
            data = response.json()
            self.logger.info("POST %s response=%s", endpoint, data)
            return data
        except requests.exceptions.RequestException as exc:
            response_text = ""
            if getattr(exc, "response", None) is not None:
                try:
                    response_text = exc.response.text
                except Exception:  # pragma: no cover - defensive fallback
                    response_text = "<unable to read response body>"
            self.logger.exception(
                "POST %s failed error=%s response=%s",
                endpoint,
                str(exc),
                response_text,
            )
            raise

