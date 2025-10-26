from src.analytics.optimization.markowitz import *
from src.analytics.returns import *
from src.analytics.risk.risk_metrics import *
from src.visualization.plot import plot_cumulative_returns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
out_dir = BASE_DIR / "src" / "plots" / "optim"
out_dir.mkdir(parents=True, exist_ok=True)


def backtest_portfolio(weights, prices: pd.DataFrame) -> pd.Series:
    """
    Compute cumulative returns of a fixed-weight portfolio on given price data.
    """
    returns = prices.pct_change().dropna()
    port_daily = returns @ weights
    cumu = (1 + port_daily).cumprod()
    return cumu


def random_portfolio_returns(curves, prices, n_portfolios=100):
    n = len(tickers)
    results = []
    for _ in range(n_portfolios):
        w = np.random.random(n)
        w /= np.sum(w)
        curve = backtest_portfolio(w, prices)
        curves[f"curve{_}"] = curve


tickers = ["JPM","AAPL", "TSLA", "GLD"]

train_prices = get_close_prices(tickers, start="2023-01-01", end="2023-12-31")
test_prices  = get_close_prices(tickers, start="2024-01-01", end="2024-12-31")

train_ann_ret, train_ann_cov = prepare_portfolio_inputs(train_prices)
w_sharpe = maximize_sharpe_ratio(train_ann_ret, train_ann_cov)
w_equal = np.ones(len(tickers)) / len(tickers)

sharpe_curve = backtest_portfolio(w_sharpe, test_prices)
equal_curve = backtest_portfolio(w_equal, test_prices)

curves = {"Max Sharpe Portfolio": sharpe_curve, "Equal Weight": equal_curve}
random_portfolio_returns(curves, test_prices, n_portfolios=500)


plot_cumulative_returns(path=out_dir / f"optim{tickers}.png", curves=curves)




