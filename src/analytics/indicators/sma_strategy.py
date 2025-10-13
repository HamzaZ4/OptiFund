from pathlib import Path

from returns import *
import matplotlib.pyplot as plt
from src.data.fetch_data import get_close_prices


project_root = Path(__file__).resolve().parents[3]  # up twice from indicators/
plot_dir = project_root / "src" / "plots" / "strategies"
plot_dir.mkdir(parents=True, exist_ok=True)

def generate_signals(prices, sma):

    # signals is like "Based on today's price vs SMA, should I ben IN(1) or OUT (0)"
    # we should be in because that is following the "uptrend" so we get in "early"
    signals = (prices > sma).astype(int)
    return signals


def build_positions(signals):
    positions = signals.shift(1).fillna(0)
    return positions


def compute_strategy_returns(daily_returns, positions):

    strategy_returns = daily_returns * positions
    return strategy_returns



def plot_strategy_vs_bh(strat_cumulative, bh_cumulative,prices,sma, ticker="AAPL"):
    fig, (ax1, ax2) = plt.subplots(
        2,1, figsize=(10,8), sharex=True, gridspec_kw={"height_ratios":[3,1]}
    )

    ax1.plot(strat_cumulative, label="SMA STRAT", linestyle="--")
    ax1.plot(bh_cumulative, label="BH STRAT", linestyle=":")
    ax1.set_title("SMA Strategy vs Buy & Hold")
    ax1.set_ylabel("Cumulative Return")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="best")

    ax2.plot(prices, label=f"{ticker} Price", linewidth=1.5)
    ax2.plot(sma, label=f"{ticker} {len(sma.dropna())}-day SMA", linestyle="--")
    ax2.set_ylabel("Price")
    ax2.set_xlabel("Date")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(loc="best")

    plt.tight_layout()
    plt.savefig(plot_dir / f"{ticker}_strat_vs_bh.png")
    plt.close()




def run_sma_strategy(ticker,window=20, period= "5y" , start=None, end = None):
    if start or end:
        close_prices = get_close_prices(ticker, start=start, end=end)
    else:
        close_prices = get_close_prices(ticker, period=period)

    sma = compute_sma(close_prices, window)
    signals = generate_signals(close_prices, sma)
    positions = build_positions(signals)

    daily_returns = compute_daily_returns(close_prices)
    strat_returns = compute_strategy_returns(daily_returns, positions)

    strat_cumulative = compute_cumulative_returns_from_returns(strat_returns)
    bh_cumulative = compute_cumulative_returns_from_returns(daily_returns)


    plot_strategy_vs_bh(strat_cumulative, bh_cumulative,close_prices,sma, ticker)

    return {
        "signals": signals,
        "positions": positions,
        "strategy_returns": strat_returns,
        "strategy_cumu": strat_cumulative,
        "bh_cumu": bh_cumulative
    }


results = run_sma_strategy("AAPL", start="2021-01-01",end="2021-12-31", window=20)





