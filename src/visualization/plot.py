import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

def plot_strategy_comparison(strat_returns, bh_returns, title, path, return_fig=False):
    plt.figure(figsize=(10, 6))
    plt.plot(strat_returns, label="SMA Strategy", linestyle="--")
    plt.plot(bh_returns, label="Buy & Hold", linestyle=":")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    if path:
        plt.savefig(path)
    plt.close()

def plot_price_with_sma(prices, sma, title, path, return_fig=False):
    plt.figure(figsize=(10, 4))
    plt.plot(prices, label="Price", linewidth=1.5)
    plt.plot(sma, label=f"SMA({sma.dropna().index.size})", linestyle="--")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    if path:
        plt.savefig(path)
    plt.close()


def plot_covariance_heatmap(df, path=None, return_fig=False):
    """
    Plots a covariance heatmap using the DataFrame's own labels.
    """
    mask = np.triu(np.ones_like(df, dtype=bool), k=1)  # keep lower triangle
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        df, mask=mask, cmap="coolwarm", annot=True, fmt=".6f",
        cbar_kws={"label": "Covariance"}
    )
    plt.title("Covariance Matrix")
    plt.tight_layout()

    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    if path:
        plt.savefig(path)
    plt.close()


def plot_correlation_heatmap(df, path=None, return_fig=False):
    mask = np.triu(np.ones_like(df, dtype=bool), k=1)
    plt.figure(figsize=(10,6))
    sns.heatmap(
        df, mask=mask, cmap="coolwarm", annot=True, fmt=".4f",
        cbar_kws={"label": "Correlation"}
    )
    plt.title("Correlation Matrix")
    plt.tight_layout()
    if return_fig:
        fig = plt.gcf()
        return fig
    if path:
        plt.savefig(path)
    plt.close()




def plot_efficiency_frontier(portfolios,marko_stats, max_sharpe_stats, rf, path, return_fig=False):
    plt.figure(figsize=(10,6))
    plt.title("Efficiency Frontiers")
    plt.scatter(portfolios["risk"], portfolios["ret"], c=portfolios["sharpe"], cmap="Blues")
    plt.scatter(marko_stats["Risk"], marko_stats["Return"], c="red", marker="*", s=200, label="Min Var")
    plt.scatter(max_sharpe_stats["Risk"], max_sharpe_stats["Return"], c="orange", marker="*", s=200, label="Max Sharpe")
    plt.colorbar(label="Sharpe Ratio")

    plt.xlabel("Risk")
    plt.ylabel("Returns")
    plt.legend()
    plt.tight_layout()
    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    if path:
        print(path)
        plt.savefig(path)
    plt.close()


def plot_cumulative_returns(path, curves: dict[str, pd.Series], title: str = "Portfolio Backtest", return_fig=False ):
    plt.figure(figsize=(12,6))
    for label, series in curves.items():
        if label == "Max Sharpe Portfolio":
            plt.plot(series.index, series.values, label=label, c="red", linewidth=2.5, zorder=4)
        elif label == "Equal Weight":
            plt.plot(series.index, series.values, label=label, c="blue", linestyle="--", linewidth=2, zorder=2)
        elif label == "Min Var Portfolio":
            plt.plot(series.index, series.values, label=label, c="green", linewidth=2.5, zorder=3)
        else:
            plt.plot(series.index, series.values, c="gray", alpha=0.3, linewidth=1, zorder=1)


    plt.legend()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns")
    plt.show()
    if return_fig:
        fig = plt.gcf()
        plt.close()
        return fig
    if path:
        plt.savefig(path)
    plt.close()