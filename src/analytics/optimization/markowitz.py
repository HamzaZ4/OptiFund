from src.analytics.returns import *
from src.analytics.risk.risk_metrics import *
from scipy.optimize import minimize


def prepare_portfolio_inputs(prices):
    """
    converts prices to returns and then annualizes coveraince and annualized returns
    """
    daily_returns  = clean_returns(prices)
    mu = compute_annulaized_returns(daily_returns)
    cov = compute_annualized_covariance(daily_returns)

    return mu, cov


def compute_portfolio_return(w, mu):
    return np.dot(w, mu)


def compute_porfolio_risk(w, cov):
    """compute the portfolio risk ( represented by the standard dev of the porfolio expected return) """
    return np.sqrt(w.T @ cov @ w)


def compute_sharpe_ratio(w, mu, cov, rf=0.05):
    """compute the Sharpe ratio for a portfolio"""
    return (compute_portfolio_return(w, mu) - rf) / compute_porfolio_risk(w, cov)

# now we're aiming for
def compute_min_var_portfolio(mu, cov):
    # our constraings
        # sum of weights must amount to 1
        # weights must be positive ( no short selling )
    n = len(mu)
    w0 = np.ones(n) / n # start with equal weights
    target_fct = lambda w: w.T @ cov @ w
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}, {"type": "ineq", "fun": lambda w: w}]
    bounds = [(0,1)] * n
    res = minimize(target_fct, w0, bounds=bounds, constraints=constraints)
    w_opt = res.x

    return w_opt

def maximize_sharpe_ratio(mu, cov):
    n = len(mu)
    w0 = np.ones(n) / n
    target_fct = lambda w: -compute_sharpe_ratio(w, mu, cov)
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}, {"type": "ineq", "fun": lambda w: w}]
    bounds = [(0,1)] * n
    res = minimize(target_fct, w0, bounds=bounds, constraints=constraints)
    w_opt = res.x
    return w_opt

def portfolio_stats(w, mu, cov):
    return {
        "Return": compute_portfolio_return(w, mu),
        "Risk": compute_porfolio_risk(w, cov),
        "Sharpe Ratio": compute_sharpe_ratio(w, mu, cov),
    }

