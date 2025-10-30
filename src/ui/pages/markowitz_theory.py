import streamlit as st
from pathlib import Path

covariance_heatmap = Path("src/plots/risk/covariance_heatmap.png")
correlation_heatmap = Path("src/plots/risk/correlation_heatmap.png")
st.title("OptiFund | Modern Portfolio Theory")


st.markdown("""
### Understanding modern portfolio theory (MPT)

Is there really such thing as the "OPTIMAL PORTFOLIO" ???

In essence, that's what modern portfolio theory is sort of a mathematically trying to approach.
The objective is building an optimal portfolio of assets, by maximizing expected returns for the collective level of risk.

-- 📜 A BIT OF HISTORY 📜 -- 
Harry Markowitz, in 1952, pioneered this theory in his paper "Portfolio Selection", for which he was later awarded a 
Nobel Prize in Economics.

The big idea:  
- Most investments are either **high-risk/high-return** or **low-risk/low-return**.  
- But by **diversifying** across assets that don’t move in lockstep (low correlation), investors can actually reduce overall portfolio risk *without* sacrificing returns.  

In MPT:  
- **Risk = variance (or standard deviation) of returns**  
- **Return = expected average return**  
- The “optimal” portfolio depends on a person's risk tolerance.

""")

st.markdown("""
            To understand MPT, we must first understand the following concepts""")

with st.expander("Covariance"):
    st.markdown("""
    Ok so what’s covariance? Basically it tells you if two stocks usually move together (go up or down together) or not.  

    - Positive → they usually go the same way (think AAPL and MSFT, both big tech, often affected by similar market conditions or public sentiment (more or less)).  
    - Negative → one goes up when the other goes down (like oil companies vs airlines).  
    - Around zero → they don’t really care about each other.
    
   ### Example: How events create (negative) covariance

    Imagine the Fed lowers interest rates:

        - Banks: They make money by lending. If rates drop, loans get cheaper, margins shrink → earnings fall → stock prices might go down.  
        - Tech companies: They borrow money to fund projects. Cheaper borrowing = more investment in growth → earnings rise → stock prices might go up.  
    
        So in the same event, banks drop while tech rises.  
        That’s negative covariance in action — one sector zigs, the other zags.
                
        Obviously, in the real world, there is much more that goes into this but this example is made just to paint a picture.
                
    Why do we care? 
    - Because if everything in your portfolio moves together, you’re not really reducing risk.  
    - Diversification only works when things **don’t** all tank at the same time.
    """)


with st.expander("The Covariance Matrix"):
    st.markdown("""
    So the covariance between two stocks is cool... but what if you're holding **5, 10, 50 stocks** in your portfolio??
    You don't just want pairwise comparisons, you need a bigger, fuller picture.
    
    That's where the **covariance matrix** comes in:
    - The diagonal (top-left → bottom-right) = each stock’s own variance (its volatility).  
    - The off-diagonal = how every pair of stocks move together.  
        
        
    """)

    st.image(str(covariance_heatmap), caption="Covariance Matrix")

    st.markdown("""
        Notice how all the values are really tiny decimals, that’s because we’re working with **daily returns**, which are already small numbers.

        Examples of daily returns:
        - JPM daily return = `+0.008` (0.8%)
        - BAC daily return = `+0.012` (1.2%)
        - Multiply = `0.008 × 0.012 = 0.000096`
        - Average that across all days = the covariance entry you see.

        So when you look at this heatmap, the *size* of the number depends on both:
        1. How volatile each stock is (bigger moves = bigger values).
        2. Whether they usually move in the same direction or not.

        The problem: covariance values are hard to compare because every stock has its own scale of returns.
        In a covariance matrix such as this one, since it's only relevant to know about the relative
        covariance between the stocks in portfolio, we could use the colors from the heat map to see 
        which move stronger together and which tend to have a much smaller correlation.
        """)

    st.markdown("""
    SOOO.... small decimals aren’t that intuitive.  
    That’s why we often switch to **correlation**, which is just a scaled version of covariance.

    Correlation is always between **-1 and +1**:
    - +1 = perfect positive relationship (move exactly together)
    - -1 = perfect opposite (one up and the other down)
    - 0 = no clear linear relationship

    Much easier to read at a glance:
    """)
    st.image(str(correlation_heatmap), caption="Correlation Matrix")

    st.markdown("""
        In this example:
        - **XEQT & VEQT ≈ 0.98** → basically moving together (redundant exposure). Not surprising, since they’re both mutual funds with almost identical holdings
        - **JPM & TLT ≈ -0.15** → slightly opposite, good for diversification. This also makes sense: When rates go up, bonds like TLT usually drop in price on the secondary market, while banks like JPM tend to benefit from higher lending margins 
        - **JPM & VEQT ≈ +0.58** → moderately correlated, so holding both means their ups and downs reinforce each other

        So: covariance shows the raw math, correlation shows the *story* in a way that’s actually useful for portfolio design.
        """)



with st.expander("The Sharpe Ratio"):
    st.markdown("""
    
    Alright so we know how to measure **risk**.

    But here’s the big question:  
    > “Am I actually getting paid enough for the risk I’m taking?”

    That’s what the **Sharpe Ratio** is going to help us answer.
    
    The Sharpe Ratio was developed in 1966 by William F. Sharpe, which compares an investment's return with its risk.

    ---
    ### Formula
    $$
    Sharpe = \\frac{R_p - R_f}{\\sigma_p}
    $$

    Where:
    - **Rp** = portfolio return  
    - **Rf** = risk-free rate (like US T-Bills)  
    - **σp** = portfolio volatility (standard deviation)
    
    What do these variables represent and where do we get them from ?
    
    **Rp**: This represents the return that the portfolio yielded over a given period\n
    **Rf**: This represents the risk-free rate, so the gains we could have made with our capital,
    investing in risk-free assets that guarantee a certain return, like government bonds
    #### σp: Represents the portfolio's volatility which is derived from the covariance matrix
    """)

    with st.expander("Deep dive: how σp comes from covariance"):
        st.markdown("""
        If you’ve got weights for each asset in your portfolio (say 50% JPM, 50% TLT),  
        then your weight vector is:  
        $$
        w = 
        \\begin{bmatrix}
        0.5 \\\\
        0.5
        \\end{bmatrix}
        $$

        Suppose your covariance matrix (just 2×2 here) is:  
        $$
        \\Sigma = 
        \\begin{bmatrix}
        0.00025 & -0.000025 \\\\
        -0.000025 & 0.00010
        \\end{bmatrix}
        $$

        Portfolio variance is:  
        $$
        Var(p) = w^T \\Sigma w
        $$

        Plugging in → ≈ **0.000075**.  
        Square root (since the variance is the square of the standard deviations and we would like to track back to more interpretable units "% of returns" in this case) → σp ≈ **0.87% daily volatility**.

        This is why covariance matters so much, it literally defines portfolio risk when you combine assets.
        """)

    st.markdown("""
    - A high Sharpe Ratio = you’re earning **a lot of return for each unit of risk** you take
    - A low Sharpe Ratio = you’re taking on risk but not being rewarded much for it

    Think of it like: “How much am I being paid at work per unit of stress im being induced?”

    ---
    ### Example:
    - Portfolio A: Return = 8%, Volatility = 10% → Sharpe ≈ 0.8  
    - Portfolio B: Return = 8%, Volatility = 5% → Sharpe ≈ 1.6  

    Both earn 8%, but Portfolio B is way more efficient (same return, half the stress).

    ---
    So in portfolio optimization, we don’t just chase **maximum return**,  
    we chase the portfolio that gives us the **best Sharpe Ratio** —  
    the best bang for your buck in risk-adjusted terms.
    """)

st.markdown("""
Having now delved into risk, covariance and Sharpe, we can now see HOW these concepts are used to build portfolios.

We’ll focus on 2 classic optimization approaches:
### 1. Minimum Variance Portfolio
This one isn't too complicated: 
It's simply the portfolio yielding the LEAST POSSIBLE RISK
Mathematically, we find the weights that minimize **σp** (portfolio volatility)

Therefore we would simply look to minimize σp

### 2. Maximum Sharpe Ratio Portfolio

Here, the goal kinda flips... 
It's not just about safety, but more about **efficiency**
We find the weights that minimize the Sharpe Ratio (most return per unit of risk)

### The efficient frontier

Now imagine graphing *every possible portfolio* (all possible weight combinations) with:
    - X-axis = Risk (σp)  
    - Y-axis = Return (Rp)

Everything on the curve is considered the most Efficient for that unit of risk.
Everything below that curve Suboptimal.  

The “tangent” portfolio with the best Sharpe Ratio? That’s your sweet spot.
""")
    


