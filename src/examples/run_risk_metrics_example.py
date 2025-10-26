from pathlib import Path
from src.data.fetch_data import get_close_prices
from src.analytics.risk.risk_metrics import (
    clean_returns, compute_covariance, compute_kurtosis, compute_sharpe_ratio
)
from src.visualization.plot import plot_covariance_heatmap

out_dir = Path("src/plots/risk")
out_dir.mkdir(parents=True, exist_ok=True)

tickers = ["JPM", "BAC", "TLT", "XOM"]
prices = get_close_prices(tickers, period="5y")
returns = clean_returns(prices)

cov = compute_covariance(returns)
kurt = compute_kurtosis(returns)
sharpe_jpm = compute_sharpe_ratio(returns["JPM"])

print("Covariance:\n", cov)
print("\nKurtosis:\n", kurt)
print(f"\nJPM Sharpe Ratio: {sharpe_jpm:.2f}")

plot_covariance_heatmap(cov, labels=tickers, path=out_dir / "covariance_heatmap.png")
