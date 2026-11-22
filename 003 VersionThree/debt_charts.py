import numpy as np
import matplotlib.pyplot as plt
from debt_model import decompose_changes

# Plotting functions for debt path and decomposition
def stacked_bars(ax, x, components, labels, colors):
    """Stack positive parts upward and negative parts downward."""
    pos_base = [0.0] * len(x)
    neg_base = [0.0] * len(x)
    for values, label, color in zip(components, labels, colors):
        bottoms = [pos_base[i] if v >= 0 else neg_base[i] for i, v in enumerate(values)]
        ax.bar(x, values, bottom=bottoms, color=color, label=label)
        for i, v in enumerate(values):
            if v >= 0:
                pos_base[i] += v
            else:
                neg_base[i] += v

def plot_results(history, initial_debt, interest_rate, growth_rate, primary_deficit, years):
    year_list = list(range(len(history)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})

    # DP vs. Initial
    ax1.plot(year_list, history, linewidth=2, label="Debt Path")
    ax1.axhline(initial_debt, color="gray", linestyle="--", label="Initial Debt")
    ax1.annotate(f"{history[-1]:.1f}%", xy=(years, history[-1]), xytext=(5, 0),
                 textcoords="offset points", va="center")
    ax1.set_ylabel("Debt-to-GDP Ratio (%)")
    ax1.set_title(f"Debt Path: r = {interest_rate}%, g = {growth_rate}%, "
                  f"Primary Deficit = {primary_deficit}% of GDP")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # What drove each year's change
    interest, growth, deficit = decompose_changes(history, interest_rate, growth_rate, primary_deficit)
    x = year_list[1:]
    stacked_bars(ax2, x, [interest, growth, deficit],
                 ["Interest", "Growth", "Primary deficit"],
                 ["tab:red", "tab:green", "tab:orange"])
    net = [i + g + d for i, g, d in zip(interest, growth, deficit)]
    ax2.plot(x, net, "ko", markersize=3, label="Net change")
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("Contribution (pp)")
    ax2.set_xlabel("Years since start")
    ax2.legend(loc="upper left", fontsize=8, ncol=4)
    ax2.grid(alpha=0.3)
  
    plt.tight_layout()
    plt.show()

def plot_comparison(scenarios):
    plt.figure(figsize=(9, 5))
    for s in scenarios:
        plt.plot(range(len(s["history"])), s["history"], linewidth=2, label=s["name"])
        plt.annotate(f"{s['history'][-1]:.1f}%", xy=(len(s["history"]) - 1, s["history"][-1]),
                     xytext=(5, 0), textcoords="offset points", va="center")
    plt.title("Debt-to-GDP: Scenario Comparison")
    plt.xlabel("Years since start")
    plt.ylabel("Debt-to-GDP (%)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_fan_chart(paths, baseline, threshold, name):
    x = np.arange(paths.shape[1])
    p5, p25, p50, p75, p95 = np.percentile(paths, [5, 25, 50, 75, 95], axis=0)

    plt.figure(figsize=(9, 5))
    plt.fill_between(x, p5, p95, color="tab:blue", alpha=0.15, label="90% range")
    plt.fill_between(x, p25, p75, color="tab:blue", alpha=0.35, label="50% range")
    plt.plot(x, p50, color="tab:blue", linewidth=2, label="Median")
    plt.plot(x, baseline, color="tab:orange", linewidth=2, label="Baseline")
    plt.axhline(threshold, color="red", linestyle="--", label=f"Threshold: {threshold}%")
    plt.title(f"Monte Carlo Simulation: {name}")    
