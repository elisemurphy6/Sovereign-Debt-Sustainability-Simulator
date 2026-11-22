import matplotlib.pyplot as plt

def simulate_debt(
    initial_debt,
    interest_rate,
    growth_rate,
    primary_deficit,
    years,
    *,
    starting_rate=None,
    refinancing_share=1.0,
):
   
    if years < 0:
        raise ValueError("Simulation length must be zero or more years.")
    if growth_rate <= -100:
        raise ValueError("GDP growth must be greater than -100%.")   


    debt = initial_debt
    history = [debt]

    # Rates as percentages. 
    growth_factor = 1 + growth_rate / 100
    effective_rate = interest_rate if starting_rate is None else starting_rate

    for _ in range(years):
        effective_rate += refinancing_share * (interest_rate - effective_rate)
        interest_factor = 1 + effective_rate / 100
        debt = debt * interest_factor / growth_factor + primary_deficit
        history.append(debt)

    return history
def stabilizing_primary_balance(initial_debt, interest_rate, growth_rate):
    interest_factor = 1 + interest_rate / 100
    growth_factor = 1 + growth_rate / 100
    return initial_debt * (interest_factor / growth_factor - 1)

#Debt-to-GDP if 2025 Conditions Persist 
scenarios = {
    "United States": {
        "initial_debt": 123.9,
        "interest_rate": 3.08,
        "growth_rate": 4.5,
        "primary_deficit": 3.2,
    },
    "France": {
        "initial_debt": 116.0,
        "interest_rate": 1.80,
        "growth_rate": 1.9,
        "primary_deficit": 3.1,
    },
    "Japan": {
        "initial_debt": 206.5,
        "interest_rate": 0.10,
        "growth_rate": 4.6,
        "primary_deficit": 0.9,
    },
}

print("\n=== 2025 Country Baselines ===")
print(
    f"{'Country':<15} {'Debt Y0':>9} {'Debt Y30':>9} "
    f"{'Y1 rate/growth':>15} {'Y1 deficit':>12} {'Fiscal gap':>11}"
    f" {'Break-even GDP growth':>22}"
)

for name, assumptions in scenarios.items():
    results = simulate_debt(**assumptions, years=30)
    plt.plot(range(len(results)), results, label=name)

    balance = stabilizing_primary_balance(
        assumptions["initial_debt"],
        assumptions["interest_rate"],
        assumptions["growth_rate"],
    )
    primary_deficit = assumptions["primary_deficit"]
    interest_growth_effect = results[1] - results[0] - primary_deficit
    fiscal_gap = balance + primary_deficit
    initial_debt = assumptions["initial_debt"]
    interest_factor = 1 + assumptions["interest_rate"] / 100
    break_even_growth = 100 * (
        initial_debt * interest_factor / (initial_debt - primary_deficit) - 1
    )

    print(
        f"{name:<15} {results[0]:>8.2f}% {results[-1]:>8.2f}% "
        f"{interest_growth_effect:>12.2f} pp {primary_deficit:>9.2f} pp "
        f"{fiscal_gap:>8.2f} pp"
        f" {break_even_growth:>21.2f}%"
    )

plt.title("Sovereign Debt-to-GDP Under Illustrative Scenarios")
plt.xlabel("Years since start")
plt.ylabel("Debt-to-GDP (%)")
plt.legend()
plt.grid(alpha=0.3)

us_baseline = scenarios["United States"]
baseline_rate = us_baseline["interest_rate"]
test_rates = [baseline_rate, baseline_rate + 1, baseline_rate + 2]

plt.figure(figsize=(9, 5))
plt.title("U.S. Debt-to-GDP Under Higher Effective Interest Rates")
print("\n=== U.S. Borrowing-Cost Stress Test ===")

stress_results = {}
for rate in test_rates:
    assumptions = us_baseline.copy()
    assumptions["interest_rate"] = rate

    results = simulate_debt(**assumptions, years=30)
    stress_results[rate] = results
    plt.plot(range(len(results)), results, label=f"{rate:.2f}% effective rate")

    target_balance = stabilizing_primary_balance(
        assumptions["initial_debt"],
        rate,
        assumptions["growth_rate"],
    )
    fiscal_gap = target_balance + assumptions["primary_deficit"]

    print(
        f"At {rate:.2f}% effective rate, Year 30 debt-to-GDP is {results[-1]:.2f}% "
        f"and the fiscal gap is {fiscal_gap:.2f} percentage points."
    )


plt.title("U.S. Debt-to-GDP Under Higher Effective Interest Rates")
plt.xlabel("Years since start")
plt.ylabel("Debt-to-GDP (%)")

gradual_assumptions = us_baseline.copy()
gradual_assumptions["interest_rate"] = baseline_rate + 2

gradual_results = simulate_debt(
    **gradual_assumptions,
    years=30,
    starting_rate=baseline_rate,
    refinancing_share=0.20,
)

plt.plot(
    range(len(gradual_results)),
    gradual_results,
    linestyle="--",
    label="5.08% target, 20% repriced annually",
)
immediate_results = stress_results[gradual_assumptions["interest_rate"]]

print("\n=== 5.08% Rate Shock | Debt-to-GDP ===")
print(f"{'Year':>4} {'Immediate':>11} {'Gradual':>11} {'Difference':>12}")

for year in (5, 10, 30):
    difference = immediate_results[year] - gradual_results[year]
    print(
        f"{year:>4} {immediate_results[year]:>10.2f}% "
        f"{gradual_results[year]:>10.2f}% {difference:>9.2f} pp"
    )
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

debt_2024 = {
    "United States": 122.3,
    "France": 113.2,
    "Japan": 214.5,
}

print("\n=== Historical Check | 2024 to 2025 ===")
print(f"{'Country':<15} {'Modeled':>10} {'Published':>10} {'Residual':>11}")

for name, assumptions in scenarios.items():
    historical_inputs = assumptions.copy()
    historical_inputs["initial_debt"] = debt_2024[name]

    modeled_debt = simulate_debt(**historical_inputs, years=1)[-1]
    published_debt = assumptions["initial_debt"]
    residual = published_debt - modeled_debt

    print(
        f"{name:<15} {modeled_debt:>9.2f}% "
        f"{published_debt:>9.2f}% {residual:>+8.2f} pp"
    )

plt.show()
