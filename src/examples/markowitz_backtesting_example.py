import numpy as np
from pathlib import Path
from src.analytics.optimization.markowitz_backtesting import run_backtest

BASE_DIR = Path(__file__).resolve().parents[3]
out_dir = BASE_DIR / "src" / "plots" / "optim" / "backtesting"
out_dir.mkdir(parents=True, exist_ok=True)

tickers = ["JPM", "AAPL", "TSLA", "GLD"]

result = run_backtest(
    tickers=tickers,
    train_start="2023-01-01",
    train_end="2023-12-31",
    test_start="2024-01-01",
    test_end="2024-12-31",
    rf=0.03,
    n_random=500,
    save_plot=True,
    plot_path= out_dir / f"backtest_{'_'.join(tickers)}.png",
)

print("Weights:")
for name, w in result["weights"].items():
    print(f"  {name}: {np.round(w,4).tolist()}")

max_sharpe_curve = result["curves"]["max_sharpe"]
print("Max Sharpe curve start/end:", max_sharpe_curve.index[0], max_sharpe_curve.iloc[0], max_sharpe_curve.index[-1], max_sharpe_curve.iloc[-1])

