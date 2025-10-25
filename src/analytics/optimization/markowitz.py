
from src.analytics.returns import *
from src.analytics.risk.risk_metrics import *


def prepare_portfolio_inputs(prices):
    """
    Converts prices to returns and then annualizes coveraince and annualized returns
    """

    daily_returns  = clean_returns(prices)
    mu = compute_annulaized_returns(daily_returns)
    cov = compute_annualized_covariance(daily_returns)

    return mu, cov


def compute_portfolio_return(w, mu):
    np.dot(w, mu)


def compute_porfolio_risk(w, cov):
    return np.sqrt(w.T @ cov @ w)



