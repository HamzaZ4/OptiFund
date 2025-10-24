## Random Variables

Random variable is just a way to like assign a variable to some random outcome

EX: Toss a fair die, X = number it ends up showin', possible values: 1,2,3,4,5,6
Each has probability 1/6

A random variable is not random by itself, it's a function of an underlying random process


## Expectation (Expected Value)

The expected value is the "long run average" of a random variable 
Given the probabilities of all events and all, the expected value is the value we would
most likely get.

Computation varies between discrete vs continuous values:

**E[X]=∑x⋅P(X=x) (discrete case)**

**E[X]=∫x f(x) dx (continuous case)**

An example for a fair die: 

**E[X]=(1+2+3+4+5+6)/6 = 3.5**

## Variance 
Variance is a measure of how much a variable spreads out from its mean  
--> Basically the average squared deviation from the mean  
--> Standard deviation is just the square root of variance  

Var(X)=E[(X−E[X])²]

Die roll example:  
**Var(X)=(1/6)∑(i−3.5)² for i=1..6 = 35/12 ≈ 2.92**

How to interpret this --> Average SQUARED deviation from the mean (3.5) is approximately 2.92.  
The average deviation or standard deviation would be √2.92 ≈ 1.7.  
We square it to punish further values from the mean more—that's all.

## Covariance
Measures how two random variables vary TOGETHER

**Cov(X,Y)=E[(X−E[X])(Y−E[Y])]**

If positive → when X is above its mean, Y tends to be above its mean  
If negative → when X is above its mean, Y tends to be below its mean  
If zero → they don't have a linear relationship (not necessarily independent, however).  

**Cov(X,Y)=E[XY]−E[X]E[Y]**

Example: Height vs Weight  
X = person’s height, Y = person’s weight.  
Generally: taller people weigh more → covariance is positive.  
If Y were something unrelated (like shoe size), covariance could be near zero.

## The Covariance Matrix

For 2 random variables, Cov(X,Y) = E[(X−μX)(Y−μY)].

Now suppose we have a vector of random variables: X = [X1,X2,...,Xn].  

Covariance matrix is an n×n matrix that captures covariance between every pair of variables.  

Properties:  
- Diagonal = Variance of each variable  
- Off-diagonal = Covariances  
- Symmetric: Cov(Xi,Xj) = Cov(Xj,Xi)

Random Variable vector is basically an array of features that can vary randomly
in the population or dataset.

(E.g.) Finance:  
We use the covariance matrix to determine covariance between stocks.  
Diagonal (variance) → volatility of a stock.  
Off-diagonal → how stocks move together.

Why it matters:  
Investors hold portfolios. Portfolio risk depends not only on variances of individual assets but on their covariances.  

- High positive covariance → stocks move together → little diversification.  
  Example: AAPL + MSFT (both big tech).  
- Low/negative covariance → offsets → diversification.  
  Example: Oil company vs Airline. Oil up → Airlines down, but holding both smooths returns.

Example covariance matrix: JPM, BAC, TLT, XOM over 5 years  

![img.png](img.png)

Key takeaways:  
1. **Volatility (diagonal)**: BAC & XOM highest, TLT lowest, JPM in between.  
2. **Covariances (off-diagonal):**  
   - Positive: BAC–JPM = 0.000236 (banks move together), BAC–XOM = 0.000145 (banks & energy).  
   - Negative: BAC–TLT = -0.000021 (banks vs bonds). Explained by rate moves and credit risk.  

## Sharpe Ratio

Measure of risk-adjusted return compared to risk-free rate.

$$
\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
$$

Where Rp = portfolio return, Rf = risk-free rate, σp = portfolio stdev.

---

### Resources used:
- https://investopedia.com  
- https://wire.insiderfinance.io/introduction-to-quant-investing-with-python-c215d1014a25  
- https://wire.insiderfinance.io/the-science-of-smart-investing-portfolio-evaluation-with-python-3e2e977c8b79  
- https://medium.com/latinxinai/portfolio-optimization-the-markowitz-mean-variance-model-c07a80056b8a  
- https://www.kaggle.com/code/lusfernandotorres/data-science-for-financial-markets#building-portfolio  
