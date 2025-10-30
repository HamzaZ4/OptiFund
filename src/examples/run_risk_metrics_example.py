from pathlib import Path

from analytics.risk.risk_metrics import compute_correlation
from src.data.fetch_data import get_close_prices
from src.analytics.risk.risk_metrics import (
    clean_returns, compute_covariance, compute_kurtosis, compute_sharpe_ratio
)
from src.visualization.plot import plot_covariance_heatmap
from visualization.plot import plot_correlation_heatmap

BASE_DIR = Path(__file__).resolve().parents[2]
out_dir = BASE_DIR / "src" / "plots" / "risk"
out_dir.mkdir(parents=True, exist_ok=True)


tickers = ["JPM", "XEQT.TO", "VEQT.TO", "TSLA", "TLT"]

prices = get_close_prices(tickers, period="5y")
returns = clean_returns(prices)

cov = compute_covariance(returns)
corr = compute_correlation(returns)
kurt = compute_kurtosis(returns)
sharpe_jpm = compute_sharpe_ratio(returns["JPM"])
print("prices", prices)
print("returns", returns)

print("Covariance:\n", cov)
print("Correlation:\n", corr)
print(f"\nJPM Sharpe Ratio: {sharpe_jpm:.2f}")

plot_covariance_heatmap(cov, path=out_dir / "covariance_heatmap.png", return_fig=False)
plot_correlation_heatmap(corr, path=out_dir / "correlation_heatmap.png", return_fig=False)
