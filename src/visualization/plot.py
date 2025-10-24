from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

def plot_strategy_comparison(strat_returns, bh_returns, title, path):
    plt.figure(figsize=(10, 6))
    plt.plot(strat_returns, label="SMA Strategy", linestyle="--")
    plt.plot(bh_returns, label="Buy & Hold", linestyle=":")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_price_with_sma(prices, sma, title, path):
    plt.figure(figsize=(10, 4))
    plt.plot(prices, label="Price", linewidth=1.5)
    plt.plot(sma, label=f"SMA({sma.dropna().index.size})", linestyle="--")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def plot_covariance_heatmap(cov: np.ndarray, labels=None, path=None):
    mask = np.triu(np.ones_like(cov, dtype=bool), k=1)
    plt.figure(figsize=(10, 6))
    sns.heatmap(cov, mask=mask, cmap="coolwarm", annot=True, fmt=".2f",
                cbar_kws={"label": "Covariance"},
                xticklabels=labels, yticklabels=labels)
    plt.title("Covariance Matrix")
    plt.tight_layout()
    if path:
        plt.savefig(path)
    else:
        plt.show()
    plt.close()