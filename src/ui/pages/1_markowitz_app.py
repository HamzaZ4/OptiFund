import streamlit as st
import numpy as np
from src.visualization.plot import plot_efficiency_frontier, plot_cumulative_returns
from src.data.fetch_data import get_close_prices
from src.analytics.optimization.markowitz import (
    prepare_portfolio_inputs,
    compute_min_var_portfolio,
    portfolio_stats,
    maximize_sharpe_ratio,
)
from src.analytics.optimization.markowitz_backtesting import run_backtest
from src.analytics.helpers.validateTickers import validateTicker
from src.examples.run_markowitz_example import generate_portfolios
from matplotlib.figure import Figure

st.title("OptiFund | Markowitz Optimizer")
st.markdown("Analyze your portfolio efficiency and backtest its performance over time.")

st.header("Markowitz Optimizer (interactive)")
st.markdown(
    "This page focuses on the interactive optimizer and backtests. "
    "For background on MPT, covariance, Sharpe ratio and the efficient frontier, "
    "see the **Markowitz Theory** page."
)

with st.expander("Quick refresher"):
    st.markdown(
        "- Efficient frontier: set of portfolios that maximize return for a given risk.\n"
        "- Max Sharpe: best return per unit of risk (tangency portfolio).\n"
        "- Min variance: portfolio with the lowest possible volatility."
    )

st.subheader("The Efficient Frontier test")

with st.expander("How to use the efficient frontier Test"):
    st.markdown("""
                First, you must read the efficient frontier theory  on the **Markowitz theory** page
                to understand the meaning of the generated graph

                ### Understanding the parameters
                - Tickers : This is supposed to be a comma seperated list of all the tickers you want in the portfolio
                - Risk-free rate: This represents a decimal value of some guaranteed rate of return on your money
                - Number of random portfolios: This is the number of random portfolios you wish to generate in the graph
                - Data period is the historical window fetched from Yahoo Finance (e.g. '1y' = last 1 year of daily closes)
                to be used for the evaluation of the potfolio risks and returns
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
    - The **orange star** marks the **Maximum Sharpe Ratio Portfolio**.  
    - The **red star** marks the **Minimum Variance Portfolio** — the safest efficient portfolio.
    """)
    st.markdown("""
    For a full theory explanation (including the Capital Market Line), open the **Markowitz Theory** page.
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

st.subheader("Backtesting with modern portfolio theory")

with st.expander("How to use the backtest"):
    st.markdown("""
                First, you must read the backtesting theory on the **Markowitz theory** page
                to understand the meaning of the generated graph

                ### Understanding the parameters
                - Tickers : This is supposed to be a comma seperated list of all the tickers you want in the portfolio
                - Training Start/End Date : These dates outline the interval of time between which we want to compute what our "optimal portfolio" will be
                - Testing Start/End Date : These dates outline the interval of time between which we are going to test the returns for the protfolio given
                - Risk-free rate: This represents a decimal value of some guaranteed rate of return on your money
                - Data period is the historical window fetched from Yahoo Finance (e.g. '1y' = last 1 year of daily closes)
                to be used for the evaluation of the potfolio risks and returns
    """)

st.sidebar.header("Backtesting Parameters")




st.sidebar.header("Backtesting Parameters")
with st.sidebar.expander("Configure Backtest"):

    backtest_tickers = st.text_input("Tickers for backtest", value="AAPL,TSLA,GLD")
    backtest_tickers = list(dict.fromkeys(
        (t.strip().upper() for t in backtest_tickers.split(",") if t.strip())
    ))

    train_start = st.date_input("Training Start Date")
    train_end = st.date_input("Training End Date")
    test_start = st.date_input("Test Start Date")
    test_end = st.date_input("Test End Date")

    backtest_rf = st.number_input("Risk-free rate (annual)", value=0.03, step=0.01)




if st.sidebar.button("Run Backtest"):
    st.subheader("Portfolio Backtest")
    try:
        # validate tickers up-front
        for ticker in backtest_tickers:
            if not validateTicker(ticker):
                st.error(f"Invalid ticker: {ticker}, must only use existing tickers trading in USD")
                st.stop()

        # Run backtest and ask it to return the figure directly.
        result = run_backtest(
            tickers=backtest_tickers,
            train_start=train_start,
            train_end=train_end,
            test_start=test_start,
            test_end=test_end,
            rf=backtest_rf,
            n_random=50,
            save_plot=False,
            plot_path=None,
            return_fig=True,
        )

        # Use the figure returned by run_backtest directly (no re-plotting)
        if isinstance(result, Figure):
            st.pyplot(result)
        elif isinstance(result, dict):
            fig = result.get("fig")
            if fig is None:
                st.error("Backtest completed but did not return a figure.")
            else:
                st.pyplot(fig)

            weights = result.get("weights", {})
            if weights:
                st.write("#### Optimized Portfolio Weights")
                st.dataframe({
                    "Ticker": backtest_tickers,
                    "Min Var": np.round(weights["min_var"], 6),
                    "Max Sharpe": np.round(weights["max_sharpe"], 6),
                    "Equal Weight": np.round(weights["equal"], 6),
                })
        else:
            st.error(f"Unexpected result from run_backtest: {type(result)}")

    except Exception as e:
        st.error(f"Error during backtest: {e}")
