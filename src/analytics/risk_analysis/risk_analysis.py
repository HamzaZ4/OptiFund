import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kurtosis, norm
import seaborn as sns
from src.data.fetch_data import get_close_prices

companies = yf.Tickers(["JPM","BAC","TLT","XOM"])

prices = companies.history(period="5y")["Close"]


def clean_prices(prices):
    prices = prices.pct_change().dropna()
    prices = prices.reset_index(drop= True)
    prices.columns.name = None
    return prices


def compute_covariance(prices):
    return prices.cov()

def plot_covariance(covariance):
    masked_cov_matrix = np.triu(np.ones_like(covariance, dtype=bool), k=1)
    plt.figure(figsize=(10,6))

    sns.heatmap(covariance, mask=masked_cov_matrix, cmap="coolwarm", annot=True,
                fmt=".7f", cbar_kws={"label": "Covariance"})

    plt.title("Covariance Matrix")
    print(covariance)
    plt.show()

def compute_kurtosis(prices):
    returns = clean_prices(prices)
    kurt = kurtosis(returns, fisher=False)
    return pd.Series(kurt,index=returns.columns, name="Kurtosis")


def compute_sharpe_ratio(ticker):
    """
    We are trying to compute how much extra return for every unit of total risk i take,
    compared to a risk-free asset.
    Args:
        ticker: string, the ticker symbol for the stock

    Returns:
        The Sharpe ratio value over the period of the past year (int)
    """
    returns = get_close_prices(ticker, "5y")

    # Using ^IRX as the basis for a "risk-free asset":
    # ^IRX is the ticker symbol that represents the 13-week us treasury bill yield
    # (interest rate that the us gov pays on short term)
    benchmark_data = get_close_prices("^IRX", "5y")


    annual_returns_bench = benchmark_data/100
    daily_ret_ben = annual_returns_bench / 252
    rf_daily = daily_ret_ben.reindex(returns.index, method="fill")

    excess = returns - rf_daily

    return (excess.mean() / excess.std()) * np.sqrt(252)



print(compute_sharpe_ratio("NVDA"))





