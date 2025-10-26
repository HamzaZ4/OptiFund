import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kurtosis
import seaborn as sns

def clean_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
        Convert price dataframe to clean daily returns.
        Drops NaNs and resets index for easy analysis.
    """
    prices = prices.pct_change().dropna()
    prices.columns.name = None
    return prices


def compute_covariance(prices):
    return prices.cov()

def plot_covariance_heat_map(covariance):
    masked_cov_matrix = np.triu(np.ones_like(covariance, dtype=bool), k=1)
    plt.figure(figsize=(10,6))

    sns.heatmap(covariance, mask=masked_cov_matrix, cmap="coolwarm", annot=True,
                fmt=".7f", cbar_kws={"label": "Covariance"})

    plt.title("Covariance Matrix")
    print(covariance)
    plt.show()

def compute_kurtosis(returns):
    """Computing the curtosis of returns for each asset"""
    kurt = kurtosis(returns, fisher = False)
    return pd.Series(kurt,index=returns.columns, name="Kurtosis")


def compute_sharpe_ratio(returns: pd.Series, rf: float = 0.02) -> float:
    """
    Compute annualized Sharpe ratio given daily returns and risk-free rate.

    Args:
        returns: Pandas Series of daily returns.
        rf: annual risk-free rate (default 2%).
    """
    rf_daily = rf / 252
    excess = returns - rf_daily
    return (excess.mean() / excess.std()) * np.sqrt(252)



def compute_annualized_covariance(daily_returns):
    """
    Annualized covariance from daily returns.
    """
    cov_daily = daily_returns.cov()
    return cov_daily * 252



