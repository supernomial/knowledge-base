---
title: Financial Benchmark Sources
accessed: 2026-05-14
---

# Financial Benchmark Sources

Citation block for the Financial Capacity Analysis section of FT studies. The plugin's `prep-ft-study` skill drops these citations into the appendix and the body-table footnotes.

## Primary source — Damodaran NYU Stern

**Aswath Damodaran, NYU Stern School of Business** — annual industry-aggregate dataset for public companies. Free, structured, updated each January. Widely cited in corporate finance, valuation, and transfer-pricing practice.

- Home page: https://pages.stern.nyu.edu/~adamodar/
- Data page: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html
- Companies in each industry: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/indname.html
- Variable definitions: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/dataarchived.html

## Datasets used

| Dataset | URL (US version; geo suffixes per file) | Ratios extracted |
|---|---|---|
| Operating and Net Margins by Industry | https://pages.stern.nyu.edu/~adamodar/pc/datasets/margin.xls | Op Margin, EBITDA Margin, Net Margin |
| Debt Ratio Trade-Off Variables by Industry | https://pages.stern.nyu.edu/~adamodar/pc/datasets/dbtfund.xls | Book D/Cap, Market D/Cap, Market D/E, EBIT/Interest, Debt/EBITDA |
| Return on Equity Decomposition by Industry | https://pages.stern.nyu.edu/~adamodar/pc/datasets/roe.xls | ROE |
| Interest Coverage Ratios and Synthetic Ratings | https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ratings.htm | EBIT/Interest → rating mapping |

## Geographic coverage

Four geo files maintained in this folder, derived from Damodaran's geo-specific datasets:

| File | Damodaran source suffix | Universe |
|---|---|---|
| `damodaran/us-2026.md` | (no suffix) | US public companies |
| `damodaran/europe-2026.md` | Europe | European public companies |
| `damodaran/global-2026.md` | Global | All public companies globally |
| `damodaran/emerging-2026.md` | emerg | Emerging-market public companies |

The tested party's geographic context drives the choice: a German subsidiary uses the Europe file; a US borrower uses the US file; a global / multi-jurisdictional borrower uses the Global file.

## Rule-of-thumb thresholds

For ratios where Damodaran does not publish industry medians (Asset Coverage), the skill applies long-standing lending-convention thresholds documented in `rule-of-thumb.md`. These thresholds reflect broad practitioner consensus and S&P / Moody's general criteria, but are not industry-specific.

## Refresh cadence

Damodaran releases his datasets in **January each year**. The benchmark files in this folder should be refreshed annually using `refresh.py`. The skill reads the most recent year file present.

## Acknowledged limitations

1. **Public-company bias.** Damodaran's data covers listed companies. Private subsidiaries (typical FT-study tested parties) may not perfectly match the public-company peer distribution. The skill's appendix discloses this in every report.
2. **Aggregate vs distribution.** Damodaran publishes industry aggregates (sum of debt / sum of EBITDA, etc.) rather than per-company distributions. The figures function as industry medians for benchmarking purposes but are not full IQRs.
3. **Annual snapshot.** Values are a single point-in-time per year; trend analysis is the user's responsibility if material to the case.

## Citation block for the report

The Appendix subsection in the FT-study report should include a citation paragraph along these lines:

> Industry-median benchmarks are sourced from Aswath Damodaran (NYU Stern), publicly available at https://pages.stern.nyu.edu/~adamodar/. The data reflects the aggregate financial profile of publicly-listed companies in each industry as of [release year]. Rule-of-thumb thresholds for ratios where no industry median is published reflect long-standing lending-convention thresholds drawn from S&P and Moody's general criteria.
