import numpy as np

from debt_model import (
    simulate_debt,
    stabilizing_primary_balance,
    break_even_growth,
    decompose_changes,
    simulate_monte_carlo,
)
from debt_charts import plot_results, plot_comparison, plot_fan_chart
from user_inputs import ask_number, ask_yes_no, get_user_inputs

def print_debt_path(history):
    years = len(history) - 1
    # Show every year for sim length <=30; every 5 years for >30 (final year shown in all cases)
    step = 1 if years <= 30 else 5
    shown = list(range(0, years + 1, step))
    if shown[-1] != years:
        shown.append(years)

    print("\n=== Debt Path ===")
    print(f"{'Year':>4} {'Debt/GDP':>10} {'Change':>9}")
    for year in shown:
        change = "" if year == 0 else f"{history[year] - history[year - 1]:+8.2f}"
        print(f"{year:>4} {history[year]:>9.2f}% {change:>9}")


def print_sustainability(initial_debt, interest_rate, growth_rate, primary_deficit, years):
    print("\n=== Sustainability ===")

    # Fiscal gap: rate at which primary balance must improve to stabilize debt
    required_balance = stabilizing_primary_balance(initial_debt, interest_rate, growth_rate)
    fiscal_gap = required_balance + primary_deficit
    print(f"Primary balance needed to stabilize debt: {required_balance:+.2f}% of GDP")
    print(f"Current primary balance:                  {-primary_deficit:+.2f}% of GDP")
    print(f"Fiscal gap:                               {fiscal_gap:+.2f} pp of GDP")

    # Break-even growth: required nominal GDP growth rate which holds debt-to-GDP constant
    be = break_even_growth(initial_debt, interest_rate, primary_deficit)
    if be is None:
        print("Break-even growth: not defined (deficit is as large as or larger than the debt)")
    else:
        print(f"Break-even nominal GDP growth:            {be:.2f}%")
        print(f"Your growth assumption:                   {growth_rate:.2f}%")

# Print result functions for the Monte Carlo simulation
def print_decomposition(interest, growth, deficit):
    print("\n=== What Drove the Change (total over the run, pp of GDP) ===")
    print(f"Interest:         {sum(interest):+8.2f}")
    print(f"Growth:           {sum(growth):+8.2f}")
    print(f"Primary deficit:  {sum(deficit):+8.2f}")
    print(f"Net change:       {sum(interest) + sum(growth) + sum(deficit):+8.2f}")


def print_comparison(scenarios):
    print("\n=== Scenario Comparison ===")
    print(f"{'Scenario':<15} {'Start':>8} {'End':>9} {'Fiscal gap':>11} {'Break-even g':>13}")
    for s in scenarios:
        p, h = s["params"], s["history"]
        gap = stabilizing_primary_balance(p["initial_debt"], p["interest_rate"],
                                          p["growth_rate"]) + p["primary_deficit"]
        be = break_even_growth(p["initial_debt"], p["interest_rate"], p["primary_deficit"])
        be_text = "n/a" if be is None else f"{be:.2f}%"
        print(f"{s['name']:<15} {h[0]:>7.1f}% {h[-1]:>8.1f}% {gap:>+8.2f} pp {be_text:>13}")


def print_risk(paths, threshold):
    final = paths[:, -1]
    p5, p50, p95 = np.percentile(final, [5, 50, 95])
    prob_end = (final > threshold).mean() * 100
    prob_any = (paths[:, 1:] > threshold).any(axis=1).mean() * 100

    print("\n=== Monte Carlo Risk Assessment ===")
    print(f"Final debt-to-GDP (5th, 50th, 95th percentiles): {p5:.1f}%, {p50:.1f}%, {p95:.1f}%")
    print(f"Probability of exceeding {threshold}% at end: {prob_end:.1f}%")
    print(f"Probability of exceeding {threshold}% at any point: {prob_any:.1f}%")       

if __name__ == "__main__":
    print("\n=== Interactive Sovereign Debt Simulator ===")
    print("Press Enter to keep the value in brackets.\n")

    scenarios = []
    params = None
    while True:
        params = get_user_inputs(params)
        default_name = f"Scenario {len(scenarios) + 1}"
        name = input(f"Name this scenario [{default_name}]: ").strip() or default_name

        history = simulate_debt(**params)
        print_debt_path(history)
        print_sustainability(**params)
        parts = decompose_changes(history, params["interest_rate"],
                                  params["growth_rate"], params["primary_deficit"])
        print_decomposition(*parts)
        scenarios.append({"name": name, "params": params, "history": history})

        if len(scenarios) == 1:
            plot_results(history, **params)      # first scenario: detailed two-panel chart
        else:
            print_comparison(scenarios)
            plot_comparison(scenarios)           # later scenarios: all paths together

        if not ask_yes_no("\nRun another scenario?"):
            break

