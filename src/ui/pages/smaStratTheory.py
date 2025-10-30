import streamlit as st
from pathlib import Path

img_path = Path("src/plots/strategies/AAPL_strat_vs_bh.png")
img_path2 = Path("src/plots/strategies/AAPL_strat_vs_bh2.png")
st.title("OptiFund | SMA Strategy")

st.markdown("""
### 🤔 WHAT EVEN IS SMA?! (Simple Moving Average)

At its core, an **SMA** is just the *average price* of an asset (like a stock) over a chosen time window.  
Take the last N days' prices, add them up, divide by N and BOOM, \b
you’ve got your SMA for that window of size N.

#### Why should you care?
- **Smooths out noise** → daily price wiggles get averaged away, so they matter less if price is always around a certain value
- **Reveals trends** →  
  - Rising SMA → likely uptrend 
  - Falling SMA → likely downtrend  
- **Support & resistance** → prices often bounce around SMA levels like invisible guardrails.

In other words: the SMA is a simple lens that helps investors **filter out chaos** and focus on the *bigger picture trend*.
""")


st.markdown(f"""
ok MR..., but how do I use this info ??
Traders don't just look at an SMA for fun... they use it as a **signal**

**The basic rule:*
- If price is **above** the SMA -> assume an uptrend, might want to hold/buy
- If price is **below** the SMA -> assume an downtrend, probably would want to sell

that's it, simple ain't it?

-------------

### Applying this to a trading strategy:

We test this rule by:
1. Looking at daily stock prices,
2. Computing the SMA,
3. Generating a "signal":
    - `1` = in position (you own the stock, portfolio tracks its returns)  
    - `0` = out of position (you sit in cash, portfolio earns 0 until re-entry)

    
4. Building a portfolio that only earns returns **while in position**,
5. Comparing it to a simple **buy-and-hold** strategy

Essentially this strategy is just *“Does timing the market with SMA signals beat just holding?”*

### Example
If you take Apple (AAPL):
- SMA(20) says "buy" when price breaks above the 20day average -> you're in position
- It flips "sell" when price dips back below -> you're out of position, sitting on cash (sold)

Sometimes this avoids big drawdowns, sometimes it makes you miss upside,
That's the experiment we run here where we plot the returns from buy and hold (in orange vs from 
applying the SMA strat ( in blue ) from January 1, 2024 to october 20th 2025 :
""")

st.markdown("""
### Example 1: Bull Market (2024–2025)
Here, Apple was trending upward. The SMA kept kicking us out of the market whenever price dipped below the average, which made us **lag behind buy-and-hold**.
""")
st.image(str(img_path), caption="SMA Strategy Example")


st.markdown("""
### Example 2: Bear Market (2022)
Now the tables turn. During Apple’s sharp decline in 2022, the SMA strategy **cut losses fast**, 
keeping returns close to zero while buy-and-hold sank almost –25%.
""")

st.image(str(img_path2), caption="SMA Strategy Example")


st.markdown(""" 
### Sources
- [Fidelity: SMA Guide](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/sma)  
- [Investopedia: Simple Moving Average (SMA)](https://www.investopedia.com/terms/s/sma.asp)  
""")

