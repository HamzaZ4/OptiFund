from turtledemo.penrose import start

import streamlit as st
import matplotlib.pyplot as plt
from src.analytics.strategies.sma_strategy import run_sma_strategy
from src.visualization.plot import plot_strategy_comparison, plot_price_with_sma

st.title("OptiFund | SMA Strategy Backtesting")
st.markdown("Compare **SMA Strategy** vs **Buy & Hold** performance interactively.")

st.sidebar.header("Strategy Parameters")

ticker = st.sidebar.text_input("Enter Ticker symbol", value="AAPL").upper().strip()
start = st.sidebar.date_input("Start Date")
end = st.sidebar.date_input("End Date")
window = int(st.sidebar.number_input("Window Size"))

if st.sidebar.button("Run Backtest"):
    st.write(f"### Results for {ticker} ({start} → {end})")
    results = run_sma_strategy(ticker, window=window, start=start, end=end)

    st.subheader("Performance Comparison")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(results["strategy_cumu"], label="SMA Strategy", linestyle="--")
    ax1.plot(results["bh_cumu"], label="Buy & Hold", linestyle=":")
    ax1.legend()
    ax1.set_title(f"{ticker} — SMA Strategy vs Buy & Hold")
    st.pyplot(fig1)

    st.subheader("Price with SMA Overlay")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(results["prices"], label="Price")
    ax2.plot(results["sma"], label="SMA", linestyle="--")
    ax2.legend()
    ax2.set_title(f"{ticker} — Price & SMA ({window}-day)")
    st.pyplot(fig2)

@st.cache_data
def get_results(ticker, window, start, end):
    return run_sma_strategy(ticker, window, start, end)



