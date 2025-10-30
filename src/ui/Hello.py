import streamlit as st

st.set_page_config(page_title="OptiFund", layout="centered")

st.title("OptiFund")
st.markdown("""
Welcome to **OptiFund**, a sandbox for testing out risk-avert (kinda) portfolio strategies.

This app is designed for investors and learners who want to:
- **Optimize portfolios carefully** (Markowitz Optimizer),
- **Backtest simple trading rules** (SMA Strategy),
- Focus on approaches that **balance return and risk**.

Think of it as a **safe lab** to explore how "safe" strategies behave over time.
""")
st.sidebar.title("Learning some Theory about the proposed concepts")
page = st.sidebar.radio("Go to:", ["Home", "Markowitz Optimizer", "SMA Strategy"])

st.sidebar.header("Test for yourself")
page = st.sidebar.radio(
    "Choose a module:",
    ["Home", "Markowitz Optimizer", "SMA Strategy", "Markowitz Theory", "SMA Strategy Theory"]
)
if page == "🏠 Home":
    st.subheader("🚀 Getting Started")
    st.markdown("""
    Use the sidebar to explore:
    - **Markowitz Optimizer** → Simulate portfolios, visualize the Efficient Frontier, 
      and test backtests in practice.
    - **SMA Strategy** → Compare Buy & Hold vs an SMA crossover trading strategy.
    - **Markowitz Theory** → Learn the math and ideas behind Modern Portfolio Theory.
    - **SMA Strategy Theory** → Understand how moving averages guide decision-making.

    👉 Start by picking a strategy or theory page in the sidebar!
    """)

elif page == "Markowitz Optimizer":
    st.switch_page("pages/1_markowitz_app.py")

elif page == "SMA Strategy":
    st.switch_page("pages/2_smaStrat.py")

elif page == "Markowitz Theory":
    st.switch_page("pages/markowitz_theory.py")

elif page == "SMA Strategy Theory":
    st.switch_page("pages/smaStratTheory.py")