# Checkout Page A/B Test: Summary for a General Audience

## Summary

An online store redesigned its checkout page. A two-week experiment was analyzed to find out whether the new page gets more visitors to complete a purchase.

**Result:** Yes. With the new page, about 13 to 14 out of every 100 visitors made a purchase, compared with about 12 out of every 100 on the old page. The difference is large enough that it is unlikely to be due to chance. The recommendation is to adopt the new page.

---

## The Question

Does the new checkout page lead more visitors to buy, and is the improvement real or due to random variation?

---

## How the Test Worked

1. **Two versions.** The current checkout page (the "control") and the redesigned page (the "treatment").
2. **Random assignment.** About 5,000 visitors saw the current page and about 5,000 saw the new page. Visitors were assigned at random, so the two groups are comparable and the page is the main difference between them.
3. **One outcome measured.** For each visitor, whether they made a purchase.

This type of experiment is called an A/B test.

---

## Preparing the Data

The raw data contained errors that had to be fixed before analysis:

- The same category written in different ways (for example "CONTROL", "control" and " control "), which a computer treats as separate values
- 200 duplicate records that would have counted some visitors twice
- Impossible values, such as negative time spent on a page
- Missing entries
- A few extreme values, such as sessions lasting hours (likely automated traffic) and a handful of unusually large orders, which can distort averages

---

## Results

| | Current page | New page |
|---|---|---|
| Visitors | 5,061 | 4,939 |
| Visitors who purchased | 593 | 661 |
| Purchase rate | 11.7% | 13.4% |

The new page produced about 1.7 additional purchases per 100 visitors, a relative improvement of about 14%.

Revenue also increased. Average revenue per visitor was $8.44 with the new page compared with $7.43 with the current one. The average order size was about the same ($63), so the added revenue came from more people purchasing rather than people spending more.

---

## Is the Difference Real?

The new page performed better, but small differences can appear by chance. Flipping a coin 100 times rarely produces exactly 50 heads. A statistical test is used to separate real improvements from random variation.

The question the test answers is:

> If the two pages actually performed the same, how likely is it that a gap this large would still appear?

The answer was about 1.2% (1 in 85). This probability is called the p-value. A common standard is to call a result "statistically significant" when the p-value is below 5%. At 1.2%, this result meets that standard, so the improvement is unlikely to be due to chance.

A likely range for the true improvement was also calculated: between 0.4 and 3.0 additional purchases per 100 visitors. The range is fairly wide, so the exact size of the benefit is uncertain, but the entire range is above zero, which supports the conclusion.

---

## Recommendation

Adopt the new checkout page. It increases the share of visitors who purchase and increases revenue per visitor.

---

## Limitations

- The data is simulated for this project, so real-world results would differ.
- The test ran for two weeks. A new design can get a temporary boost from novelty, and a longer test would show whether the improvement lasts.
- The range of possible improvement is wide, so the benefit could be modest or substantial.
- The revenue result was only just significant (p-value of 4.0% against the 5% standard), so it is supporting evidence rather than strong proof.
- The new page performed better on desktop, mobile and tablet, but the groups were too small to be certain about any single device.

## Next Steps

- Run the test longer to narrow the range of possible improvement
- Test a mobile-specific checkout design, since mobile showed the smallest gain
- Repeat the analysis with real company data

---

## Glossary

| Term | Meaning |
|---|---|
| A/B test | An experiment that shows two versions to different random groups to see which performs better |
| Control / treatment | The current version / the new version being tested |
| Conversion rate | The share of visitors who complete the desired action (here, a purchase) |
| p-value | The probability of seeing a gap this large if there were truly no difference. A small value suggests the difference is real |
| Statistically significant | A difference that is unlikely to be due to chance (commonly, a p-value below 5%) |
| Confidence interval | A range that likely contains the true size of the effect |
| Outlier | An unusually extreme value that can distort averages |
