import pandas as pd

from src.returns import *


def test_daily_returns():
    prices = pd.Series([100,103, 106.09])
    expected = pd.Series([None, 0.03, 0.03])
    result = compute_daily_returns(prices)
    pd.testing.assert_series_equal(result.round(4), expected.round(4))


def test_cumulative_returns():
    prices = pd.Series([100,103, 106.09])
    expected = pd.Series([None, 0.03, 0.0609])
    result = compute_cumulative_returns(prices)
    pd.testing.assert_series_equal(result.round(4), expected.round(4))


def test_compute_sma():
    prices = pd.Series([1,2,3,4,5])
    expected = pd.Series([None,None, 2,3,4])
    result = compute_sma(prices)
    pd.testing.assert_series_equal(expected.round(4), result.round(4))

def test_compute_ema():
    prices = pd.Series([1,2,3,4,5])
    expected = prices.ewm(span=3).mean()
    result = compute_ema(prices, 2)
    pd.testing.assert_series_equal(expected.round(4), result.round(4))