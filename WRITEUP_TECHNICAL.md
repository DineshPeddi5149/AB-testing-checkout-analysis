# A/B Test Analysis: Checkout Page Redesign

Technical write-up. Full analysis in `ab_test_analysis.ipynb`.

**Tools:** Python, Pandas, NumPy, SciPy, Matplotlib, Seaborn

---

## 1. Objective

Determine whether a redesigned checkout page (treatment) converts a higher share of users than the current page (control), and whether the difference is statistically significant.

| Item | Specification |
|---|---|
| Unit of randomization | User |
| Allocation | Random, approximately 50/50 |
| Duration | 14 days (2026-09-01 to 2026-09-14) |
| Primary metric | Conversion rate (`converted`, binary) |
| Secondary metrics | Revenue per user, average order value |
| Null hypothesis (H0) | p_treatment = p_control |
| Alternative (H1) | p_treatment is not equal to p_control (two-sided) |
| Significance level | alpha = 0.05 |

**Data source:** The dataset is simulated (`generate_dataset.py`, seed 42) with data quality issues injected deliberately. It contains 10,200 raw rows and 8 columns: `user_id, group, date, device, user_type, time_on_page, converted, revenue`.

---

## 2. Methodology

### 2.1 Data collection

- `serve_data.py` runs a local HTTP server (Python standard library) that returns the dataset as JSON at `GET /api/ab_test`.
- The notebook retrieves it with `requests.get()`, validates the response with `raise_for_status()`, and parses it with `.json()`.
- The raw response is written to `data/raw_ab_test.json` using `json.dump`.
- If the API is unavailable, the notebook falls back to `raw_ab_test.csv`.

### 2.2 Data cleaning (Pandas)

The raw data was profiled first with `isna().sum()`, `duplicated().sum()`, `unique()` and `describe()`.

| Issue | Evidence | Treatment |
|---|---|---|
| Inconsistent `group` labels | `CONTROL`, ` treatment ` (case, whitespace) | `str.strip().str.lower()` |
| Inconsistent `device` labels and nulls | `Mobile` vs `mobile`; missing values | Normalize case; fill nulls with `"unknown"` |
| Duplicate records | 200 exact duplicates | `drop_duplicates()`, leaving 10,000 rows |
| Incorrect dtype | `date` stored as string | `pd.to_datetime` |
| Invalid values | 20 negative `time_on_page` | Set to NaN |
| Missing `time_on_page` | 319 nulls after the step above | Imputed in preprocessing |
| Outliers | Bot-like sessions; a few very large orders | Capped in preprocessing |

Validation checks (`assert`): `user_id` is unique, `group` is in {control, treatment}, `converted` is in {0, 1}.

### 2.3 Preprocessing (NumPy)

- **Imputation:** missing `time_on_page` filled with the median (`np.nanmedian`, `np.where`).
- **Outlier handling:** winsorized at the 99th percentile (`np.percentile`, `np.clip`).
  - `time_on_page` cap: 470 seconds (100 values capped).
  - `revenue` cap: $233, with the percentile computed among purchasers only so that the zero values do not distort it (13 orders capped).
- **Feature engineering:** `log_time = log1p(time_on_page)`, `time_zscore`, and `time_bucket` created with `np.select`.
- **Output:** `data/clean_ab_test.csv`.

Winsorizing was chosen over deletion so that all randomized users remain in the analysis.

### 2.4 Exploratory analysis

Five figures are saved to `figures/`:
1. Conversion rate and revenue per user by group
2. Conversion by device and by user type
3. Daily conversion rate by group
4. Distribution of time on page and order value
5. 95% confidence interval for the lift

---

## 3. Results

### 3.1 Group balance

| Group | Users | Conversions | Conversion rate |
|---|---|---|---|
| Control | 5,061 | 593 | 11.72% |
| Treatment | 4,939 | 661 | 13.38% |

A chi-square goodness-of-fit test against a 50/50 split gives p = 0.222, so there is no evidence of an allocation imbalance.

### 3.2 Primary metric: two-proportion z-test

Pooled conversion rate:

p_pooled = (593 + 661) / 10,000 = 0.1254

Standard error under H0:

SE = sqrt( p_pooled x (1 - p_pooled) x (1/n_control + 1/n_treatment) )
SE = sqrt( 0.1254 x 0.8746 x (1/5061 + 1/4939) ) = 0.00662

Test statistic and p-value:

z = (0.13383 - 0.11717) / 0.00662 = 2.515
p = 2 x (1 - Phi(|z|)) = 0.0119

Since p < 0.05, H0 is rejected.

| Metric | Value |
|---|---|
| Absolute lift | +1.67 percentage points |
| Relative lift | +14.2% |
| 95% CI for the difference (unpooled SE) | [+0.37, +2.97] percentage points |

The confidence interval uses the unpooled standard error (approximately 0.00663), because the two proportions are not assumed equal under the alternative: difference +/- 1.96 x SE.

**Cross-check:** a chi-square test of independence on the 2x2 table (no continuity correction) returns p = 0.0119, identical to the z-test. For a 2x2 table, chi-square equals z squared.

### 3.3 Secondary metric: revenue

| Metric | Control | Treatment | Difference |
|---|---|---|---|
| Revenue per user (winsorized, zeros included) | $7.43 | $8.44 | +$1.01 |
| Average order value (purchasers only) | $63.40 | $63.08 | -$0.32 |

Welch's t-test on revenue per user: t = 2.054, p = 0.040. Average order value is essentially unchanged, so the revenue increase is attributable to a higher number of purchasers, not larger orders.

### 3.4 Segment analysis by device (exploratory)

| Device | Control | Treatment | Lift (pp) | p-value |
|---|---|---|---|---|
| Desktop | 12.0% | 14.1% | +2.0 | 0.072 |
| Mobile | 11.6% | 12.6% | +0.9 | 0.315 |
| Tablet | 11.4% | 14.7% | +3.3 | 0.162 |

Treatment is directionally higher in every segment, but no individual segment is significant. Segment sample sizes are smaller and no multiple-comparison correction was applied, so these results are exploratory.

---

## 4. Conclusion

The redesigned checkout page increased conversion from 11.72% to 13.38% (z = 2.52, p = 0.012). The 95% confidence interval for the lift is [+0.37, +2.97] percentage points, which excludes zero but is wide. Revenue per user also increased (p = 0.040).

**Recommendation:** roll out the redesigned checkout page.

---

## 5. Limitations

1. **Simulated data.** Real traffic includes seasonality, repeat visitors and tracking error that are not represented here.
2. **Test duration.** 14 days may not rule out a novelty effect.
3. **Revenue significance is marginal.** p = 0.040 is close to the 0.05 threshold.
4. **No prospective power analysis.** In practice, the required sample size for a target minimum detectable effect would be calculated before launching the test.
5. **Analyst judgment calls.** The imputation and winsorizing choices affect the revenue analysis. They do not affect the conversion test, which uses only the binary outcome.
6. **Segment results are exploratory** and not adjusted for multiple comparisons.
7. **Normal approximation.** The z-test is appropriate at these sample sizes. Smaller samples would call for an exact test.

## 6. Possible Extensions

- Pre-test power and sample size calculation
- Logistic regression to adjust for device, user type and engagement
- Bootstrap confidence interval as a robustness check
- Replication on a public real-world A/B dataset

---

## 7. Reproducibility

```bash
pip install -r requirements.txt
python generate_dataset.py      # optional: regenerate raw data
python serve_data.py            # terminal 1: start the API
jupyter notebook                # terminal 2: open ab_test_analysis.ipynb and run all cells
```
