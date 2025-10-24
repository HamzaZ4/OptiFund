from pathlib import Path
from src.analytics.strategies.sma_strategy import run_sma_strategy
from src.visualization.plot import plot_strategy_comparison, plot_price_with_sma

BASE_DIR = Path(__file__).resolve().parents[3]
out_dir = BASE_DIR / "src" / "plots" / "strategies"
out_dir.mkdir(parents=True, exist_ok=True)

ticker = "NFLX"
res = run_sma_strategy(ticker, start="2021-01-01", end="2021-12-31", window=20)

plot_strategy_comparison(
    res["strategy_cumu"],
    res["bh_cumu"],
    title=f"{ticker} — SMA Strategy vs Buy & Hold",
    path=out_dir / f"{ticker}_strat_vs_bh.png",
)

plot_price_with_sma(
    res["prices"],
    res["sma"],
    title=f"{ticker} — Price with SMA",
    path=out_dir / f"{ticker}_price_sma.png",
)
