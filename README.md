# Sovereign Debt Sustainability Simulator
## Background

I began this project in the week the U.S. gross national debt passed $40 trillion, in August 2026. In 1999, with the budget in surplus, President Clinton proposed paying off the debt held by the public by 2015. The federal budget ran surpluses from fiscal 1998 through 2001. Today, those years are hard to picture.

A Python model of how a country's debt-to-GDP ratio evolves over time, based on the interest rate on its debt, nominal GDP growth, and the primary budget balance. The project has been built in three versions, from fixed illustrative scenarios (V1) to calibrated 2025 country baselines and stress tests (V2) to an interactive simulator where users set their own parameters (V3).
 
## Repository structure
 
```
├── 001 VersionOne/
│   ├── Debt-To-GDP-Sim1.py        Illustrative scenarios
│   └── Figures/
├── 002 VersionTwo/
│   ├── Debt-To-GDP-Sim2.py        2025 country baselines and stress tests
│   └── Figures/
├── 003 VersionThree/
│   ├── Sim3.py                    Run this: interactive simulator
│   ├── debt_model.py              The math (no input or charts)
│   ├── debt_charts.py             All plotting
│   ├── user_inputs.py             Prompts and input validation
│   └── Figures/
├── requirements.txt
├── LICENSE
└── README.md
```
 
## Getting started
 
Requires Python 3 with `matplotlib` and `numpy`.
 
```bash
pip install -r requirements.txt
python "003 VersionThree/Sim3.py"
```
 
The program asks for each input in turn; press Enter to accept default values [in brackets]. Close each chart window to continue to the next prompt.
 
## The model
 
All rates are in percent and all balances are in percent of GDP.
 
| Symbol | Meaning |
|---|---|
| $d_t$ | Debt-to-GDP ratio in year $t$ |
| $r$ | Effective (average) interest rate on government debt |
| $g$ | Nominal GDP growth |
| $pd$ | Primary deficit (deficit excluding interest payments; negative = surplus) |
 
**Debt dynamics**
 
$$d_{t+1} = d_t \cdot \frac{1 + r}{1 + g} + pd$$
 
**Debt-stabilizing primary balance:** the primary surplus that holds the debt ratio constant.
 
$$s^* = d \cdot \left(\frac{1 + r}{1 + g} - 1\right)$$
 
**Fiscal gap:** how much the primary balance must improve to stabilize debt. A positive value means tightening is needed.
 
$$\text{fiscal gap} = s^* + pd$$
 
**Break-even growth:** the nominal growth rate at which debt-to-GDP stays constant, given the current rate and deficit. Not defined when the deficit is as large as the debt.
 
$$g^* = \frac{d \cdot (1 + r)}{d - pd} - 1$$
 
**Decomposition:** each year's change in the debt ratio splits into three parts:
 
| Component | Formula | Effect |
|---|---|---|
| Interest | $d_t \cdot r / (1 + g)$ | Pushes debt up |
| Growth | $-d_t \cdot g / (1 + g)$ | Shrinks the ratio |
| Primary deficit | $pd$ | New borrowing beyond interest |
 
## Version history
 
### Version 1: Illustrative scenarios
Simulates debt over 30 years for three stylized cases (a US-like case, a Japan-like case and a debt crisis) and reports the stabilizing primary balance and fiscal gap for each.
 
![Version 1 scenarios](001%20VersionOne/Figures/Figure_1_V1.png)
 
### Version 2: 2025 baselines and stress tests
Uses 2025 inputs for the United States, France and Japan. Adds break-even growth, an interest-rate stress test (+1 and +2 percentage points), gradual repricing of debt as it is refinanced (20% per year), and a one-year historical check of the model against published 2024 to 2025 debt ratios.
 
![Version 2 country baselines](002%20VersionTwo/Figures/Figure_1_V2.png)
 
![Version 2 rate stress test](002%20VersionTwo/Figures/Figure_2_V2.png)
 
### Version 3: Interactive simulator
Users enter their own starting debt, interest rate, GDP growth, primary deficit and simulation length. Outputs:
 
- **Debt path:** a year-by-year table plus a chart against the starting level
- **Sustainability:** fiscal gap and break-even growth
- **Decomposition:** stacked bars showing how much of each year's change comes from interest, growth and the deficit
- **Scenario comparison:** each new run starts from the previous inputs, so you can change one assumption and compare paths on one chart
- **Uncertainty analysis (Monte Carlo):** 1,000 simulations with random yearly shocks to growth and interest rates, shown as a fan chart, with the probability of debt crossing a user-set threshold
## Version 3 examples
 
The illustrative scenarios below all run for 30 years. Inputs are listed as debt / r / g / primary deficit.
 
| Scenario | Inputs | Year 30 | Fiscal gap | What it shows |
|---|---|---|---|---|
| Baseline | 100 / 3 / 4 / 3 | 153.3% | +2.04 pp | Growth exceeds the interest rate, but the deficit still pushes debt up |
| Rate shock | 100 / 5 / 4 / 3 | 237.0% | +3.96 pp | The baseline with rates 2 pp higher |
| Snowball | 100 / 5 / 3 / 3 | 298.7% | +4.94 pp | Interest above growth makes debt compound |
| Consolidation | 100 / 5 / 3 / −2 | 97.7% | −0.06 pp | A 2% primary surplus roughly holds debt steady even when r > g |
| Growth-led paydown | 120 / 2 / 7 / −1 | 12.2% | −6.61 pp | High growth, low rates and a small surplus shrink debt quickly |
| Debt crisis | 100 / 10 / 0 / 6 | 2,731.9% | +16.00 pp | High rates, no growth and a large deficit: the debt ratio explodes |
 
**Figure 1: Baseline debt path.** The top panel shows the debt path against its starting level. The bottom panel splits each year's change into interest (red), growth (green) and the primary deficit (orange). Growth more than offsets interest, so the deficit alone is what drives debt up.
 
![Figure 1: Baseline debt path](003%20VersionThree/Figures/Figure_1_V3.png)
 
**Figure 2: Baseline, rate shock, snowball and consolidation.** Raising the interest rate by 2 pp (rate shock) or letting it exceed growth (snowball) sharply raises the path, while a primary surplus (consolidation) holds debt roughly flat despite the same high rate.
 
![Figure 2: Scenario comparison](003%20VersionThree/Figures/Figure_2_V3.png)
 
**Figure 3: All six scenarios.** Figure 2 with the growth-led paydown and debt crisis added. The debt crisis path rises so far that it compresses the scale for the other scenarios, which shows how quickly debt compounds when interest rates are high, growth stalls and deficits stay large.
 
![Figure 3: All six scenarios](003%20VersionThree/Figures/Figure_3_V3.png)
 
**Figure 4: United States**
 
![United States](003%20VersionThree/Figures/Figure_4_V3_US.png)
 
**Figure 5: France**
 
![France](003%20VersionThree/Figures/Figure_5_V3_FRA.png)
 
**Figure 6: Japan**
 
![Japan](003%20VersionThree/Figures/Figure_6_V3_JPN.png)
 
**Figure 7: Country comparison**
 
![Country comparison](003%20VersionThree/Figures/Figure_7_V3_RWComp.png)
 
### Country results (60 years, 2025 baselines from Version 2)
 
| Country | Debt | r | g | Primary deficit | Year 30 | Fiscal gap | Break-even g | P(debt > 150%)* |
|---|---|---|---|---|---|---|---|---|
| United States | 123.9 | 3.08 | 4.5 | 3.2 | 161.5% | +1.52 pp | 5.81% | 79.8% |
| France | 116.0 | 1.80 | 1.9 | 3.1 | 204.3% | +2.99 pp | 4.60% | 100% |
| Japan | 206.5 | 0.10 | 4.6 | 0.9 | 70.5% | −7.98 pp | 0.54% | 0% |
 
\*From the uncertainty analysis, using the default volatility (growth 2 pp, interest rate 1 pp) and a fixed random seed.
 
<!-- TODO: add sources for the 2025 inputs (e.g. IMF, OECD, national statistics). -->
Input sources: TODO
 
Japan's falling path depends on near-zero interest rates and 4.6% nominal growth persisting for 30 years; small changes to either assumption change the result substantially.

## License
 
See [LICENSE](LICENSE).

## Data and assumptions

The debt and budget figures come from the IMF’s April 2026 *Fiscal Monitor*. Nominal GDP growth comes from each country’s national accounts. [IMF Fiscal Monitor, Tables A1, A2, and A7](https://www.imf.org/-/media/files/publications/fiscal-monitor/2026/april/english/msa.pdf) · [U.S. BEA](https://bea.gov/index.php/news/2026/gdp-second-estimate-4th-quarter-and-year-2025) · [France INSEE](https://www.insee.fr/en/statistiques/8988863) · [Japan Cabinet Office](https://www.esri.cao.go.jp/en/sna/data/sokuhou/files/2026/qe262/pdf/gaiyou2621_e.pdf)

The starting interest rate is estimated by dividing 2025 net interest expense by 2024 gross debt. It represents the net interest burden on existing debt. Market yields measure the rate investors demand on bonds today.

The refinancing share is illustrative. The model abstracts from individual bond maturities, exchange-rate valuation, and other adjustments to the debt stock.
