from __future__ import annotations
from typing import Dict
import pandas as pd

from src.data.fetch_data import get_close_prices
from src.analytics.returns import (
    compute_daily_returns,
    compute_cumulative_returns_from_returns,
    compute_sma,
)

def generate_signals(prices, sma):
    """Signal 1 if price > SMA, else 0 (computed at close of t, acted on at t+1)."""
    signals = (prices > sma).astype(int)
    return signals


def build_positions(signals):
    """Shift signals by one day to represent acting next session."""
    positions = signals.shift(1).fillna(0)
    return positions


def compute_strategy_returns(daily_returns, positions):
    """Daily strategy returns: market return when in position, 0 when out."""
    strategy_returns = daily_returns * positions
    return strategy_returns

def run_sma_strategy(ticker,window=20, period= "5y" , start=None, end = None):
    prices = (
        get_close_prices(ticker, start=start, end=end)
        if (start or end)
        else get_close_prices(ticker, period=period)
    )
    close_prices = prices.squeeze()
    
    sma = compute_sma(close_prices, window)
    signals = generate_signals(close_prices, sma)
    positions = build_positions(signals)

    daily_returns = compute_daily_returns(close_prices)
    strat_returns = compute_strategy_returns(daily_returns, positions)

    strat_cumulative = compute_cumulative_returns_from_returns(strat_returns)
    bh_cumulative = compute_cumulative_returns_from_returns(daily_returns)

    return {
        "prices": prices,
        "sma": sma,
        "signals": signals,
        "positions": positions,
        "strategy_returns": strat_returns,
        "strategy_cumu": strat_cumulative,
        "bh_cumu": bh_cumulative,
    }