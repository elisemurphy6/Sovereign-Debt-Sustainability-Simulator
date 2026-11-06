# Sovereign Debt Sustainability Simulator

Japan starts with the highest debt-to-GDP ratio in this simulation. It’s also the only country whose ratio falls when 2025 conditions are held constant.

This Python project compares debt paths for the United States, France, and Japan. It shows how interest costs, nominal GDP growth, and the primary budget balance shape those paths, then tests how quickly a rate shock can work its way into U.S. debt.

## Run locally

```bash
python -m pip install -r requirements.txt
python simulate_debt.py
```

Run both commands from the repository root. The script prints the results and opens two Matplotlib charts.

## What the simulation shows

| Country | Starting debt / GDP | Year 30 debt / GDP | 2025 nominal GDP growth | Growth needed to stabilize debt |
|---|---:|---:|---:|---:|
| United States | 123.90% | 161.47% | 4.50% | 5.81% |
| France | 116.00% | 204.32% | 1.90% | 4.60% |
| Japan | 206.50% | 70.53% | 4.60% | 0.54% |

In Japan’s first simulated year, the gap between interest costs and GDP growth pulls debt-to-GDP down by **8.88 percentage points**. The primary deficit adds back **0.90 points**, leaving a net decline of **7.98 points**. In the U.S. and France, the primary deficit is large enough to push the ratio up despite nominal growth exceeding the implied interest rate.

The 30-year paths are scenarios. Each asks what would happen if the country’s 2025 growth rate, interest rate, and primary deficit persisted.

## How quickly does a rate shock hit?

The U.S. stress test raises the effective interest rate from **3.08% to 5.08%** while holding growth and the primary deficit fixed. In one scenario, the full increase takes effect in Year 1. In the other, the effective rate closes **20% of the remaining gap** each year, representing gradual refinancing.

| Year | Immediate increase | Gradual refinancing | Difference |
|---|---:|---:|---:|
| 5 | 143.56% | 136.91% | 6.65 pp |
| 10 | 163.76% | 154.50% | 9.27 pp |
| 30 | 250.42% | 238.58% | 11.85 pp |

By Year 30, the effective rates are nearly identical, but the debt ratios are still **11.85 percentage points apart**. The immediate shock adds interest to the debt balance sooner, and that extra debt carries forward.

## Model

```text
debt_next = debt_current × (1 + interest_rate) / (1 + nominal_growth)
            + primary_deficit
```

Debt and the primary deficit are expressed as percentages of GDP. The deficit uses the new year’s GDP, and a negative deficit represents a surplus. The equation uses decimal rates. The Python script converts percentage inputs such as `4.5` to decimals internally.

The simulator also calculates two ways to hold debt-to-GDP at its starting level. **Break-even growth** tells you how fast nominal GDP would need to grow with fiscal policy and interest costs fixed. The **fiscal gap** tells you how much the primary balance would need to improve with growth and interest costs fixed. A negative fiscal gap means the current balance is already stronger than the balance required to stabilize debt.

## Historical check

The script takes each country’s published 2024 debt ratio, applies the 2025 inputs for one year, and compares the result with the published 2025 ratio. It reports the difference as **published minus modeled**. Because this check uses data from the year it reconstructs, it shows how closely the simplified equation matches the historical result.

## Data and assumptions

The debt and budget figures come from the IMF’s April 2026 *Fiscal Monitor*. Nominal GDP growth comes from each country’s national accounts. [IMF Fiscal Monitor, Tables A1, A2, and A7](https://www.imf.org/-/media/files/publications/fiscal-monitor/2026/april/english/msa.pdf) · [U.S. BEA](https://bea.gov/index.php/news/2026/gdp-second-estimate-4th-quarter-and-year-2025) · [France INSEE](https://www.insee.fr/en/statistiques/8988863) · [Japan Cabinet Office](https://www.esri.cao.go.jp/en/sna/data/sokuhou/files/2026/qe262/pdf/gaiyou2621_e.pdf)

The starting interest rate is estimated by dividing 2025 net interest expense by 2024 gross debt. It represents the net interest burden on existing debt. Market yields measure the rate investors demand on bonds today.

The refinancing share is illustrative. The model abstracts from individual bond maturities, exchange-rate valuation, and other adjustments to the debt stock.
