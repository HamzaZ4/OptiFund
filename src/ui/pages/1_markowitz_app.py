import streamlit as st
import numpy as np
from src.visualization.plot import plot_efficiency_frontier
from src.data.fetch_data import get_close_prices
from src.analytics.optimization.markowitz import (
    prepare_portfolio_inputs,
    compute_min_var_portfolio,
    portfolio_stats,
    maximize_sharpe_ratio,
)
from src.examples.run_markowitz_example import generate_portfolios

st.title("OptiFund | Markowitz Optimizer")
st.markdown("Analyze your portfolio efficiency and backtest its performance over time.")

st.header("Understanding Modern Portfolio Theory (MPT)")

st.markdown("""
Modern Portfolio Theory (MPT), which was introduced by **Harry Markowitz in 1952**, 
is the foundation of modern investing.

The big idea: **don’t mindlessly pick assets in isolation**, instead, 
optimize your **whole portfolio** by balancing *expected return* and *risk*.

In other words, investors should aim for portfolios that:
- **maximize return** for a given level of risk, or
- **minimize risk** for a given level of return.
""")

st.subheader("Expected Return and Risk")
with st.expander("Expected Return and Risk"):
    st.markdown("""
    Each asset has an expected return (μ) and risk (σ).
    For a portfolio, these combine as:
    
    - **Expected portfolio return**  
      \\( E[R_p] = w^T μ \\)
    
    - **Portfolio variance (risk)**  
      \\( σ_p^2 = w^T Σ w \\)
    
    where:
    - *w* = vector of portfolio weights  
    - *Σ* = covariance matrix of asset returns  
    """)

    st.markdown("""
    The covariance term (Σ) captures how assets move **together** — 
    this is why diversification matters.  
    Low or negative covariances reduce overall portfolio risk.
    """)

st.subheader("The Efficient Frontier")

with st.expander("Sharpe Ratio and Efficient Frontier"):
    st.markdown("""
    The **Efficient Frontier** represents all optimal portfolios — 
    those that offer the highest expected return for each level of risk.
    
    Portfolios below the frontier are **inefficient** (you could earn more return for the same risk).  
    Portfolios above it are **impossible** — they’d violate market assumptions.
    
    To estimate this frontier, we simulate thousands of random portfolios 
    and compute their return, risk, and Sharpe ratio.
    """)


# Efficiency Frontier Section
st.sidebar.header("Efficiency Frontier Parameters")
with st.sidebar.expander("Configure Efficient Frontier"):
    eff_tickers = st.text_input("Tickers (comma-separated)", value="AAPL,TSLA,TLT,GLD")
    eff_tickers = [t.strip().upper() for t in eff_tickers.split(",") if t.strip()]

    eff_rf = st.number_input("Risk-free rate (annual)", value=0.02, step=0.01)
    eff_n_portfolios = st.slider("Number of random portfolios", 500, 5000, 2000, 500)
    eff_period = st.selectbox("Data period", ["6mo", "1y", "2y", "5y"], index=2)

if st.sidebar.button("Run Efficiency Frontier"):
    st.markdown("""
    - The **blue cloud** shows feasible portfolios.  
    - The **orange star** marks the **Maximum Sharpe Ratio Portfolio** (tangent to the Capital Market Line).  
    - The **red star** marks the **Minimum Variance Portfolio** — the safest efficient portfolio.
    """)
    st.markdown("""
    The **Capital Market Line (CML)** connects the risk-free asset (e.g. treasury bills) 
    to the tangency portfolio (the Max Sharpe portfolio).

    All points along this line represent portfolios combining risk-free lending and risky investing.  
    No portfolio can lie above this line — those would imply returns higher than theoretically possible.
    """)

    st.subheader("Efficient Frontier Simulation")
    try:
        prices = get_close_prices(eff_tickers, period=eff_period)
        mu, cov = prepare_portfolio_inputs(prices)
        w_min_var = compute_min_var_portfolio(mu, cov)
        stats_min_var = portfolio_stats(w_min_var, mu, cov)

        w_max_sharpe = maximize_sharpe_ratio(mu, cov)
        stats_max_sharpe = portfolio_stats(w_max_sharpe, mu, cov)
        portfolios = generate_portfolios(mu, cov, eff_n_portfolios, rf=eff_rf)

        fig = plot_efficiency_frontier(
            portfolios,
            stats_min_var,
            stats_max_sharpe,
            eff_rf,
            path=None,
            return_fig=True,
        )
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error while running optimization: {e}")


# Backtesting ------------------------------------------------------------------------------------

st.sidebar.header("Backtesting Parameters")
with st.sidebar.expander("Configure Backtest"):

    backtest_tickers = st.text_input("Tickers for backtest", value="AAPL,TSLA,GLD")
    backtest_tickers = [t.strip().upper() for t in backtest_tickers.split(",") if t.strip()]

    train_start = st.date_input("Training Start Date")
    train_end = st.date_input("Training End Date")
    test_start = st.date_input("Test Start Date")
    test_end = st.date_input("Test End Date")

    backtest_rf = st.number_input("Risk-free rate (annual)", value=0.03, step=0.01)

if st.sidebar.button("Run Backtest"):
    st.subheader("Portfolio Backtest")
    try:
        train_prices = get_close_prices(backtest_tickers, start=train_start, end=train_end)
        test_prices = get_close_prices(backtest_tickers, start=test_start, end=test_end)

        mu, cov = prepare_portfolio_inputs(train_prices)

        w_max_sharpe = maximize_sharpe_ratio(mu, cov, backtest_rf)
        w_min_var = compute_min_var_portfolio(mu, cov, backtest_rf)
        w_equal = np.ones(len(backtest_tickers)) / len(backtest_tickers)

        st.write("#### Optimized Portfolio Weights")
        st.dataframe({
            "Ticker": backtest_tickers,
            "Min Var": w_min_var,
            "Max Sharpe": w_max_sharpe,
            "Equal Weight": w_equal
        })


    except Exception as e:
        st.error(f"Error during backtest: {e}")
