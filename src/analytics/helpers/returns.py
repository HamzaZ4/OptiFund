import pandas as pd
import matplotlib.pyplot as plt
from src.data.fetch_data import get_close_prices



def compute_daily_returns(prices):
    """
    Compute daily returns from a Pandas Series of prices.

    Params:
        prices : Pandas series or dataframe of daily stock prices indexed by date

    Returns:
         Daily returns as percentages (e.g., 0.02 = 2%) for each stock
    """

    returns = prices.pct_change()

    return returns.fillna(0)



def compute_cumulative_returns(prices, as_percentage: bool = True) -> pd.Series:
    """
    Compute cumulative returns from a Pandas Series of prices.

    Params:
        prices: Pandas Series or DataFrame of daily stock prices indexed by date for different stocks

    Returns:
        pandas series or dataframe of cumulative returns
    """

    cumulative = (1 + compute_daily_returns(prices)).cumprod() - 1
    return cumulative


def compute_cumulative_returns_from_returns(daily_returns) -> pd.Series:
    """
    Compute cumulative returns from a Pandas Series of prices.

    Params:
        prices: Pandas Series or DataFrame of daily stock prices indexed by date for different stocks

    Returns:
        pandas series or dataframe of cumulative returns
    """

    cumulative = (1 + daily_returns).cumprod() - 1
    return cumulative



def get_company_returns(ticker: str ="AAPL"):
    """
    Compute company returns based on user demanded ticker

    Params:
        ticker (string) : Company ticker for which we compute
          the returns of past 5 days

    Returns:
        ret: The cumulative returns made over the week
    """

    prices = get_close_prices(ticker, period="5d")

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

def compute_annualized_returns(daily_returns):
    """
    Annualizing daily returns for each asset
    """
    mean_daily = daily_returns.mean()
    annualized = (1+ mean_daily) ** 252 - 1
    return annualized

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
    print(compute_daily_returns(get_close_prices("AAPL", start="2023-01-01", end="2023-12-31")))