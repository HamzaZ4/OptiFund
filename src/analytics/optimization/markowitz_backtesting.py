import numpy as np
import pandas as pd
from src.analytics.optimization.markowitz import prepare_portfolio_inputs, maximize_sharpe_ratio, compute_min_var_portfolio
from src.analytics.returns import get_close_prices
from src.visualization.plot import plot_cumulative_returns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
out_dir = BASE_DIR / "src" / "plots" / "optim"
out_dir.mkdir(parents=True, exist_ok=True)


def backtest_portfolio(weights: np.ndarray, prices: pd.DataFrame) -> pd.Series:
    """
    Compute cumulative returns of a fixed-weight portfolio on given price data.

    Args:
        weights: 1d array of portfolio weights (len == prices.shape[1]).
        prices: price dataframe with columns matching tickers.

    Returns:
        cumulative returns series (index = prices.index).
    """
    returns = prices.pct_change().dropna(how="all")
    port_daily = returns @ weights
    cumu = (1 + port_daily).cumprod()
    return cumu


def random_portfolio_returns(prices: pd.DataFrame, n_portfolios: int = 100, seed: int | None = None) -> dict[str, pd.Series]:
    """
    Generate random equal-weighted-sum portfolios and return their cumulative curves.

    Args:
        prices: price dataframe.
        n_portfolios: number of random portfolios to generate.
        seed: optional RNG seed.

    Returns:
        dict mapping "random_i" -> cumulative returns series.
    """
    rng = np.random.default_rng(seed)
    n = prices.shape[1]
    curves: dict[str, pd.Series] = {}
    for i in range(n_portfolios):
        w = rng.random(n)
        w /= w.sum()
        curves[f"random_{i}"] = backtest_portfolio(w, prices)
    return curves


def run_backtest(
    tickers: list[str],
    train_start: str,
    train_end: str,
    test_start: str,
    test_end: str,
    rf: float = 0.03,
    n_random: int = 100,
    save_plot: bool = False,
    plot_path: Path | None = None,
):
    """
    Args:
        tickers: list of tickers to use (case-insensitive).
        train_start/train_end: date range for training (to compute mu, cov).
        test_start/test_end: date range for backtest.
        rf: risk-free rate passed to Sharpe optimizer.
        n_random: how many random portfolios for comparison.
        save_plot: whether to save a plot of curves.
        plot_path: target path for saved plot (if save_plot True).

    Returns:
        dict with keys:
          - "weights": {"max_sharpe": np.ndarray, "min_var": np.ndarray, "equal": np.ndarray}
          - "curves": {"max_sharpe": Series, "min_var": Series, "equal": Series, "random_*": Series...}
    """
    tickers = [t.upper().strip() for t in tickers]

    train_prices = get_close_prices(tickers, start=train_start, end=train_end)
    mu, cov = prepare_portfolio_inputs(train_prices)


    w_max_sharpe = maximize_sharpe_ratio(mu, cov, rf)
    w_min_var = compute_min_var_portfolio(mu, cov)
    w_equal = np.ones(len(tickers)) / len(tickers)

    test_prices = get_close_prices(tickers, start=test_start, end=test_end)
    curves = {
        "Max Sharpe Portfolio": backtest_portfolio(w_max_sharpe, test_prices),
        "Min Var Portfolio": backtest_portfolio(w_min_var, test_prices),
        "Equal Weight": backtest_portfolio(w_equal, test_prices),
    }
    rand_curves = random_portfolio_returns(test_prices, n_portfolios=n_random)
    curves.update(rand_curves)

    if save_plot:
        plot_cumulative_returns(path=plot_path, curves=curves)
    return {
        "weights": {"max_sharpe": w_max_sharpe, "min_var": w_min_var, "equal": w_equal},
        "curves": curves,
    }


