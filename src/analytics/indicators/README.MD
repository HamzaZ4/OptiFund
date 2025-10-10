## Difference Between Daily Return and Cumulative Return

### Daily Return
The daily return represents the total returns of a stock based on yesterday's price measured against today's price.  

Formula:  
**rₜ = (Pₜ − Pₜ₋₁) / Pₜ₋₁**

---

### Cumulative Return
The cumulative return represents the total returns of an investment since inception.  

Formula:  
**Rₜ = ∏(1 + rᵢ) − 1, for i=1..t**

---

### Simple Moving Average (SMA)
The SMA is the arithmetic average of asset prices over a specified period.  
Calculated by summing the prices of recent data points and dividing by the number of periods.

#### Why it matters to investors:
- Smooths out daily price fluctuations  
- Reduces noise, helps identify trends  
  - Rising SMA → uptrend  
  - Falling SMA → downtrend  
- Support and resistance: prices often bounce near SMA levels  

---

### Exponential Moving Average (EMA)
The EMA tracks the price of a financial asset by giving more weight to recent price data, making it more responsive to current market fluctuations.  

#### Why it matters to investors:
- EMA reacts faster to changes than SMA  
- Smooths noise but stays closer to current price  
- Acts as **dynamic support or resistance**  
- Useful for setting stop-losses or scaling entries  

---

#### Example: EMA Pullback Entry Strategy

Suppose you want to invest **$3,000** in Company X.

**Going all in:**  
- Buy $3,000 at once at $100.  
- If the price dips immediately, you suffer full drawdown.  

**Scaling with EMA:**  
- Split $3,000 into 3 × $1,000.  
- Enter at breakout and scale in at EMA pullbacks.  

Steps:  
1. **Breakout buy:** $1,000 at $100. Early exposure to the trend.  
2. **Pullback to EMA:** Price dips to 21-EMA at $98. Add $1,000.  
3. **EMA respected again:** Price retests EMA at $99. Add final $1,000.  

This method smooths entry and uses EMA as dynamic support.

---

### Extra Concept: Moving Average Ribbon
A **Moving Average Ribbon** layers multiple EMAs (e.g., 10, 21, 50, 100, 200) to visualize trend strength and momentum.  

More info: [TrendSpider – Moving Average Ribbon](https://trendspider.com/learning-center/what-is-a-moving-average-ribbon/)
