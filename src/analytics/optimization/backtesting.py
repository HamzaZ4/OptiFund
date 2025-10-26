from src.analytics.optimization.markowitz import *
from src.analytics.returns import *
from src.analytics.risk.risk_metrics import *


tickers = ["AAPL", "TSLA", "TLT", "GLD"]

def random_portfolio_returns(mu, n_portfolios=5000):
    n = len(tickers)
    results = []
    for _ in range(n_portfolios):
        w = np.random.random(n)
        w /= np.sum(w)
        ret = np.dot(w, mu)
        
        results.append({"ret": ret, "w": w})

    return pd.DataFrame(results)

train_prices = get_close_prices(tickers, start="2023-01-01", end="2023-12-31")
test_prices  = get_close_prices(tickers, start="2024-01-01", end="2024-12-31")

train_ann_ret, train_ann_cov = prepare_portfolio_inputs(train_prices)

w_sharpe = maximize_sharpe_ratio(train_ann_ret, train_ann_cov)

returns_2024 = clean_returns(test_prices)
port_daily = returns_2024 @ w_sharpe

