# A/B Test Analysis: Checkout Page Redesign

Analyzed a simulated A/B test of 10,000 users to decide whether a redesigned checkout page should replace the current one.

**Result:** conversion rose from 11.72% to 13.38% (+1.67 pp, p = 0.012, 95% CI [+0.37, +2.97] pp); revenue per user rose from $7.43 to $8.44. Recommendation: roll out.

## Skills demonstrated
- **Data collection:** pulled JSON from an API with `requests`, saved raw data with Python file I/O
- **Data cleaning (Pandas):** fixed inconsistent labels, missing values, duplicates, impossible values
- **Preprocessing (NumPy):** median imputation, percentile capping (winsorizing), log transform, z-scores, binning
- **Visualization (Matplotlib/Seaborn):** conversion by group/device/user type, daily trend, distributions, confidence interval plot
- **Statistics:** two-proportion z-test, chi-square test, confidence interval, Welch's t-test, p-values

## Files
| File | What it is |
|---|---|
| `ab_test_analysis.ipynb` | the full analysis (start here) |
| `WRITEUP_TECHNICAL.md` | full methodology, formulas, limitations, interview Q&A |
| `WRITEUP_NONTECHNICAL.md` | plain-English summary for non-technical readers |
| `generate_dataset.py` | creates the simulated, messy dataset |
| `serve_data.py` | tiny local API that serves the data |
| `raw_ab_test.csv` | raw dataset |
| `figures/` | saved charts |

## How to run
```bash
pip install -r requirements.txt
python serve_data.py          # terminal 1: starts the API
jupyter notebook              # terminal 2: open ab_test_analysis.ipynb, Run All
```
If the API isn't running, the notebook automatically loads `raw_ab_test.csv`.
