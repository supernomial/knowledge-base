# Financial Benchmarks Manifest

Industry-aggregate financial benchmarks for the Supernomial Cowork plugin's Financial Capacity Analysis (part of `prep-ft-study`).

Base URL: `https://raw.githubusercontent.com/supernomial/knowledge-base/main/financial-benchmarks`

Updated: 2026-05-14

## Damodaran industry medians

Annual aggregates from Damodaran (NYU Stern), four geographic universes.

| ID | Geography | File | Industries | Release |
|---|---|---|---|---|
| us | United States | `damodaran/us-2026.md` | 94 | 2026 |
| europe | Europe | `damodaran/europe-2026.md` | 95 | 2026 |
| global | Global | `damodaran/global-2026.md` | 94 | 2026 |
| emerging | Emerging Markets | `damodaran/emerging-2026.md` | 94 | 2026 |

Ratios reported per industry: Op Margin, EBITDA Margin, Net Margin, Book D/Cap, Market D/Cap, Market D/E, EBIT/Interest, Debt/EBITDA, ROE.

## Damodaran interest-coverage → synthetic rating

Compact lookup table mapping EBIT-to-Interest coverage to a synthetic S&P / Moody's rating.

| File | Use |
|---|---|
| `damodaran/rating-coverage-2026.md` | Reference table for the EBIT/Interest row in the Financial Capacity body table; appendix reference |

## Rule-of-thumb thresholds

For ratios with no public industry median (Asset Coverage).

| File | Use |
|---|---|
| `rule-of-thumb.md` | Pass/Reasoning thresholds where Damodaran does not publish an industry median |

## Sector mapping

| File | Use |
|---|---|
| `industry-mapping.md` | smartZebra sector codes → Damodaran industry names; disambiguation guidance |

## Sources and citation

| File | Use |
|---|---|
| `sources.md` | Citation block for the report appendix; data acquisition URLs and limitations |

## Refresh

`scripts/refresh.py` downloads the source `.xls` files from Damodaran's site, rebuilds the markdown files for every geo, and updates this manifest's "Updated" timestamp. Run annually after Damodaran publishes the new January dataset.

## How the plugin uses these files

The `prep-ft-study` skill fetches the relevant geo file at runtime via raw GitHub HTTPS. The user's tested-party country drives which geo file is read (US borrower → `us-2026.md`; European borrower → `europe-2026.md`; multi-jurisdictional → `global-2026.md`).

For each ratio row in the Financial Capacity body table, the skill:

1. Computes the tested party's 3-year average ratio from the intake workbook.
2. Looks up the industry median in the geo file (mapped via `industry-mapping.md` or user override).
3. Renders the body table row with `Pass` or `Reasoning: <one sentence>` verdict.
4. The appendix subsection reproduces the tested industry's row + 2–3 adjacent industries for reviewer transparency.
