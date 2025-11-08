import numpy as np
from src.analytics.helpers.returns import compute_annualized_returns
from src.analytics.risk.risk_metrics import clean_returns, compute_annualized_covariance
from scipy.optimize import minimize

from src.data.fetch_data import get_close_prices


def prepare_portfolio_inputs(prices):
    """
    converts prices to returns and then annualizes coveraince and annualized returns
    Args:
        prices: DF or array-like of close prices (columns are different assets)
    
    Returns:
        mu: 1D array of annyalized expected returns of each asset
        cov: annualized covariance matrix.
    """
    daily_returns  = clean_returns(prices)
    mu = compute_annualized_returns(daily_returns)
    cov = compute_annualized_covariance(daily_returns)

    return mu, cov


def compute_portfolio_return(w, mu):
    """
    Computes the portfolio's expected return.

    Args:
        w: 1D array of portfolio weights
        mu: 1D array of the each asset's expected portfolio returns
    Returns:
        Scalar expected portfolio return
    """
    return np.dot(w, mu)


def compute_porfolio_risk(w, cov):
    """
    compute the portfolio risk ( represented by the standard dev of the porfolio expected return)
    Args:
        w: 1D array of portfolio weights
        cov: covariance matrix of asset returns.
    
    Returns:
        Scalar portfolio standard deviation
    """
    return np.sqrt(w.T @ cov @ w)


def compute_sharpe_ratio(w, mu, cov, rf=0.05):
    """
    Computes the Sharpe ratio = (return - rf) / volatility
    Args:
        w: array of portfolio asset weights
        mu: expected returns array
        cov: covariance matrix
        rf: annual risk-free rate ( e.g standard gov bond yield )
    
    Returns:
        Scalar Sharpe ratio
    """
    return (compute_portfolio_return(w, mu) - rf) / compute_porfolio_risk(w, cov)

# now we're aiming for
def compute_min_var_portfolio(mu, cov, rf = 0.02):
    """
    Finding the minimum-variance portfolio under:
        - weights sum up to 1 ( allocate all ressources given )
        - no short selling, so the weights must be >= 0
    Args:
        mu: expected returns
        cov: covariance matrix

    Returns:
        Optimized weights as a 1D array
    """
    n = len(mu)
    w0 = np.ones(n) / n # start with equal weights
    target_fct = lambda w: w.T @ cov @ w
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}, {"type": "ineq", "fun": lambda w: w}]
    bounds = [(0,1)] * n
    res = minimize(target_fct, w0, bounds=bounds, constraints=constraints)
    w_opt = res.x

    return w_opt

def maximize_sharpe_ratio(mu, cov, rf=0.02):
    """
    Maximize portfolio sharpe ratio with same constraints as min-variance
        -full allocation of all ressources and no short selling
    Args:
        mu: expected returns
        cov: covariance matrix
    Returns:
        Optimized weights as a 1D array
    """
    n = len(mu)
    w0 = np.ones(n) / n
    target_fct = lambda w: -compute_sharpe_ratio(w, mu, cov, rf)
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}, {"type": "ineq", "fun": lambda w: w}]
    bounds = [(0,1)] * n
    res = minimize(target_fct, w0, bounds=bounds, constraints=constraints)
    w_opt = res.x
    return w_opt

def portfolio_stats(w, mu, cov):
    """
    Return a small summary of portfolio metrics
    Args:
        w: weights array
        mu: expected returns
        cov: covariance matrix
    
    Returns:
        Dict with the keys "Return, "Risk" and "Sharpe Ratio".
    """
    return {
        "Return": compute_portfolio_return(w, mu),
        "Risk": compute_porfolio_risk(w, cov),
        "Sharpe Ratio": compute_sharpe_ratio(w, mu, cov),
    }


def run_optimization(tickers, rf = 0.03):
    """
    Run full optimization pipeline for given tickers:
      - fetch prices
      - compute mu and cov
      - compute min-variance and max-Sharpe portfolios
      - return their stats
    """
    prices = get_close_prices(tickers)
    mu, cov = prepare_portfolio_inputs(prices)
    w_min_var = compute_min_var_portfolio(mu, cov, rf)
    w_max_sharpe = maximize_sharpe_ratio(mu, cov, rf)
    stats_min_var = portfolio_stats(w_min_var, mu, cov)
    stats_max_sharpe = portfolio_stats(w_max_sharpe, mu, cov)
    return stats_min_var, stats_max_sharpe