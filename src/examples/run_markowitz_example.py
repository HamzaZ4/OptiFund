import numpy as np
import pandas as pd
from src.analytics.optimization.markowitz import prepare_portfolio_inputs,compute_min_var_portfolio,portfolio_stats,maximize_sharpe_ratio
from src.data.fetch_data import get_close_prices
from src.visualization.plot import plot_efficiency_frontier
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
out_dir = BASE_DIR / "src" / "plots" / "optim" / "example"
out_dir.mkdir(parents=True, exist_ok=True)

def generate_portfolios(mu, cov, n_portfolios=5000, rf=0.02):
    results = {"ret": [], "risk": [], "sharpe": []}
    n = len(mu)

    for _ in range(n_portfolios):
        w = np.random.random(n)
        w /= np.sum(w)
        ret = np.dot(w, mu)
        risk = np.sqrt(w.T @ cov @ w)
        sharpe = (ret - rf) / risk

        results["ret"].append(ret)
        results["risk"].append(risk)
        results["sharpe"].append(sharpe)

    return pd.DataFrame(results)

tickers = ["GM", "GOOG", "XOM", "GLD"]

prices = get_close_prices(tickers, period="1y")

ann_ret, ann_cov = prepare_portfolio_inputs(prices)

marko_w = compute_min_var_portfolio(ann_ret, ann_cov, 0.07)
marko_stats = portfolio_stats(marko_w, ann_ret, ann_cov)
max_sharpe_w = maximize_sharpe_ratio(ann_ret, ann_cov, 0.07)
max_sharpe_stats = portfolio_stats(max_sharpe_w, ann_ret, ann_cov)

portfolios = generate_portfolios(ann_ret, ann_cov, n_portfolios=5000)

backtest_dir = out_dir
backtest_dir.mkdir(parents=True, exist_ok=True)
fname = f"optim_{'_'.join(tickers)}.png"

print(f"{backtest_dir}/{fname}")
plot_efficiency_frontier(
    portfolios,
    marko_stats,
    max_sharpe_stats,
    0.05,
    path=backtest_dir / fname,
)
