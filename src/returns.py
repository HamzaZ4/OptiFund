import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt



def compute_daily_returns(prices: pd.Series) -> pd.Series:
    """
    Compute daily returns from a Pandas Series of prices.

    Params:
        prices (pd.series) : Daily stock prices indexed by date.

    Returns:
        pd.series: Daily returns as percentages (e.g., 0.02 = 2%)
    """

    # Operations on pandas SERIES !!!

    # what i want to do is for each element in the series, take the value divided by previous value and then substract 1

    returns = prices.pct_change()

    return returns



def compute_cumulative_returns(prices: pd.Series, as_percentage: bool = True) -> pd.Series:
    """
    Compute cumulative returns from a Pandas Series of prices.

    Params:
        prices (pd.series) : Daily stock prices indexed by date.

    Returns:
        pd.series: Cumulative returns as percentages (e.g., 0.02 = 2%)
    """

    cumulative = (1+compute_daily_returns(prices)).cumprod()

    return cumulative - 1 if as_percentage else cumulative


def get_company_returns(ticker: str ="AAPL"):
    """
    Compute company returns based on user demanded ticker

    Params:
        ticker (string) : Company ticker for which we compute
          the returns of past 5 days

    Returns:
        ret: The cumulative returns made over the week
    """

    try:
        ticker_obj = yf.Ticker(ticker)
        history = ticker_obj.history(period="5d")
    except Exception as e:
        raise ValueError(f'Could not fetch the data for ticker {ticker}')

    prices = history["Close"]

    return compute_daily_returns(prices)


def compute_sma(prices: pd.Series, window: int) -> pd.Series:
    # using the rolling method on series to get a rolling object, which then allows us to
    # compute a moving average as we extract the mean of each value using the window
    return prices.rolling(window=window).mean()


def compute_ema(prices, span):
    # now this is more complicated, because how do you define the weights ??
    # , we need to use weights that decay exponentially
    # That way recent prices are more important,
    # e.g span = 3, wights might be 0.5 ( most recent), 0.33, 0.17

    # FORMULA EMA(t) = aP(t) + (1-a)EMA(t-1) , 
    #- where a = 2/(span+1)
    #- P(t) today's price
    #- a is the smoothing factor
    #- EMA(t-1) yesterday's ema

    #--> Today's ema is a mix of A portion of today's price (axP(t))
    # The remaining weight carried oforward from yesterday's EMA((1-a)EMA)(t-1)
    # a is essentially what is controlling how fast EMA reacts to today's prices


    # IN PANDAS:
        # ewm = Exponential weighted moving
        # It creates an exponential window object which know how to apply weights to our data
        # , so I can then call .mean() (for ema), to then do the operation we describe on top
    return prices.ewm(span=span, adjust=False).mean()


def plot_MAs(prices, sma, ema, ticker):
    """
    Plot stock prices with SMA and EMA
    """

    plt.figure(figsize=(10,6))
    plt.plot(prices, label=f"{ticker} Price", linewidth=2)
    plt.plot(sma, label="SMA", linestyle = "--")
    plt.plot(ema, label="EMA", linestyle = ":")

    plt.title(f"{ticker} Price with SMA and EMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.legend(loc="best")
    plt.savefig(f"src/plots/{ticker}_ma.png")
    plt.close()


if __name__ == "__main__":
    ticker ="NFLX"
    ticker_obj = yf.Ticker(ticker)
    prices = ticker_obj.history(period="3mo")["Close"]

    sma = compute_sma(prices, 20)
    ema = compute_ema(prices, 20)

    print(sma)
    print(ema)
    print(prices)

    plot_MAs(prices, sma, ema, ticker)