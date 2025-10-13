import yfinance as yf
import pandas as pd


def get_close_prices(
        tickers: list[str] | str,
        start: str | None = None,
        end: str | None = None,
        period: str = "1d"):
    """
    Fetched the daily close prices for one or more tickers
    and returns a clean dataframe ready for analysis
    Args:
        tickers: single or multiple tickers
        start: start date (optional)
        end: end data (optional)
        period: fallback period if no start and end are provided

    Returns:
        Dataframe with datatime index and 1 close price column per ticker

    """

    if start or end:
        hist = yf.download(tickers, start=start, end=end)
    else:
        hist = yf.download(tickers, period=period)

    if isinstance(hist.columns, pd.MultiIndex):
        close_prices = hist["Close"]
    else:
        close_prices = hist[["Close"]]
        close_prices.columns = [tickers] if isinstance(tickers, str) else tickers

    close_prices = close_prices.sort_index()
    # removing timezone info to only consider calendar dates...
    close_prices.index = close_prices.index.tz_localize(None)
    close_prices.dropna(how="all", inplace=True)
    close_prices.columns = [c.upper() for c in close_prices.columns]

    return close_prices


if __name__ == "__main__":
    df = get_close_prices(["AAPL","MSFT"], start="2020-01-01", end="2025-01-01")
    print(df.info())
    print(df.head())
    print(df.head())