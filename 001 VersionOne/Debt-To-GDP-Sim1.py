import matplotlib.pyplot as plt

def simulate_debt(
    initial_debt,
    interest_rate,
    growth_rate,
    primary_deficit,
    years,
):
    print("\n=== Sovereign Debt Simulation ===")
    print(f"Initial Debt-to-GDP: {initial_debt}%")
    print(f"Interest Rate:       {interest_rate}%")
    print(f"GDP Growth Rate:     {growth_rate}%")
    print(f"Primary Deficit:     {primary_deficit}%")
    print(f"Simulation Length:   {years} years")
    print("=" * 33)

    debt = initial_debt
    history = [debt]

    # Rates as percentages. 
    interest_factor = 1 + interest_rate / 100
    growth_factor = 1 + growth_rate / 100

    for _ in range(years):
        debt = debt * interest_factor / growth_factor + primary_deficit
        history.append(debt)

    return history
def stabilizing_primary_balance(initial_debt, interest_rate, growth_rate):
    interest_factor = 1 + interest_rate / 100
    growth_factor = 1 + growth_rate / 100
    return initial_debt * (interest_factor / growth_factor - 1)

scenarios = {
    "United States": {
        "initial_debt": 120,
        "interest_rate": 4,
        "growth_rate": 2.5,
        "primary_deficit": 5,
    },
    "Japan": {
        "initial_debt": 250,
        "interest_rate": 1,
        "growth_rate": 1,
        "primary_deficit": 3,
    },
    "Debt Crisis": {
        "initial_debt": 100,
        "interest_rate": 10,
        "growth_rate": 0,
        "primary_deficit": 6,
    },
    
}

for name, assumptions in scenarios.items():
    print(f"\n--- {name} (Illustrative Scenario) ---")
    results = simulate_debt(**assumptions, years=30)
    print(f"Year 0:  {results[0]:.2f}%")
    print(f"Year 1:  {results[1]:.2f}%")
    print(f"Year 30: {results[30]:.2f}%")

for name, assumptions in scenarios.items():
    results = simulate_debt(**assumptions, years=30)
    plt.plot(range(len(results)), results, label=name)
    balance = stabilizing_primary_balance(
        assumptions["initial_debt"],
        assumptions["interest_rate"],
        assumptions["growth_rate"],
    )
    print(f"{name} — stabilizing primary balance: {balance:+.2f}% of GDP")
    current_balance = -assumptions["primary_deficit"]
    fiscal_gap = balance - current_balance

    print(f"Current primary balance: {current_balance:+.2f}% of GDP")
    print(f"Fiscal gap: {fiscal_gap:+.2f} percentage points of GDP")

plt.title("Sovereign Debt-to-GDP Under Illustrative Scenarios")
plt.xlabel("Years since start")
plt.ylabel("Debt-to-GDP (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
