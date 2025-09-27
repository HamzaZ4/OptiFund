from returns import *
import matplotlib.pyplot as plt

def sma_strat(sma, prices):
    # my first step is to want to get the signals
    # this identifies when the prices and sma are crossing

    # signals is like "Based on today's price vs SMA, should I ben IN(1) or OUT (0)"
    # we should be in because that is following the "uptrend" so we get in "early"
    signals = (prices>sma).astype(int)

    # on day t, after the market closes, you compare today's price vs SMA
    # if price > SMA -> signal = 1 we want in
    # if price < SMA -> signal = 0 we want out

    # but the signal is only known at the end of the day, so we ACT ON IT ON DAY t+1
    # so position[t] is the signal we generated using yesterday's closing price.

    # tells us, coming into day t, are we holding stock (1) or not (0)
    positions = signals.shift(1).fillna(0)



#COMPUTING RETURNS:

    # if positions[t] = 1, it means that we bought at close the day of t-1
    #  and are holding through day t
    # our gain/loss is just the daily return of day t
    # it positions[t] = 0, we're in cash, daily return = 0

    strategy_returns = compute_daily_returns(prices) * positions

    # cumulative returns from strat
    strat_returns = (1 + strategy_returns).cumprod() - 1
    bh_returns = compute_cumulative_returns(prices)

    plt.plot(strat_returns, label="SMA STRAT", linestyle="--")
    plt.plot(bh_returns, label="BH STRAT", linestyle=":")
    plt.title("SMA Strategy vs Buy & Hold")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"src/plots/_maSTRAT.png")

    return strat_returns, bh_returns, signals, positions

    

aapl = yf.Ticker("AAPL")
prices = aapl.history(period="10y")["Close"]
sma = compute_sma(prices, 20)

sma_strat(sma, prices)

