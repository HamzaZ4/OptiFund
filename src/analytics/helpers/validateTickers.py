import pandas as pd
import yfinance as yf


def validateTicker(ticker: str) -> bool:
    try:
        info = yf.Ticker(ticker).info

        return info.get("currency") == "USD"
    except Exception:
        return False
