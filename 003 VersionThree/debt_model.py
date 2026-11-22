import numpy as np

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

    growth_factor = 1 + growth_rate / 100
    effective_rate = interest_rate if starting_rate is None else starting_rate

    for _ in range(years):
        effective_rate += refinancing_share * (interest_rate - effective_rate)
        interest_factor = 1 + effective_rate / 100
        debt = debt * interest_factor / growth_factor + primary_deficit
        history.append(debt)

    return history

def stabilizing_primary_balance(initial_debt, interest_rate, growth_rate):
    """Primary surplus (% of GDP) needed to hold debt-to-GDP constant."""
    interest_factor = 1 + interest_rate / 100
    growth_factor = 1 + growth_rate / 100
    return initial_debt * (interest_factor / growth_factor - 1)

def break_even_growth(initial_debt, interest_rate, primary_deficit):
    """Returns None when the formula isn't defined (deficit >= debt)."""
    if initial_debt - primary_deficit <= 0:
        return None
    return 100 * (initial_debt * (1 + interest_rate / 100) / (initial_debt - primary_deficit) - 1)

def decompose_changes(history, interest_rate, growth_rate, primary_deficit):
    """Split each year's debt change into interest, growth and deficit parts."""
    r = interest_rate / 100
    g = growth_rate / 100
    interest, growth, deficit = [], [], []
    for prev in history[:-1]:
        interest.append(prev * r / (1 + g))
        growth.append(-prev * g / (1 + g))
        deficit.append(primary_deficit)
    return interest, growth, deficit

def simulate_monte_carlo(initial_debt, interest_rate, growth_rate, primary_deficit, years,
                         growth_sd=2.0, rate_sd=1.0, n_sims=1000, seed=42):
    """Run many debt paths with random yearly shocks to growth and interest rates."""
    rng = np.random.default_rng(seed)  # fixed seed = same results each run
    g = growth_rate + rng.normal(0, growth_sd, size=(n_sims, years))
    r = interest_rate + rng.normal(0, rate_sd, size=(n_sims, years))
    g = np.maximum(g, -99.0)  # keep growth above -100% so the math works

    paths = np.empty((n_sims, years + 1))
    paths[:, 0] = initial_debt
    for t in range(years):
        paths[:, t + 1] = paths[:, t] * (1 + r[:, t] / 100) / (1 + g[:, t] / 100) + primary_deficit
    return paths

