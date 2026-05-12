# Sources

Upstream sources that feed this knowledge base. Used for two purposes:
1. **Sync schedule** — regularly check these URLs for new or updated content
2. **Deep mode** — experts can check the live source when users need the latest information

## How to use

**Periodic sync:** Compare `last_checked` dates against source pages. Download new/updated documents to `raw/`, update INDEX.md, compile to knowledge articles.

**Expert deep mode:** When a user asks an expert to go deeper or verify against the latest rules, the expert should fetch the `live_url` directly and cross-reference with the compiled knowledge article. Flag any discrepancies as potential updates.

---

## OECD Transfer Pricing Country Profiles

- **live_url:** https://www.oecd.org/en/topics/sub-issues/transfer-pricing/transfer-pricing-country-profiles.html
- **pdf_pattern:** `https://www.oecd.org/content/dam/oecd/en/topics/policy-sub-issues/transfer-pricing/transfer-pricing-country-profile-{slug}.pdf`
- **last_checked:** 2026-04-09
- **countries_downloaded:** 83
- **notes:** Most slugs use hyphens (e.g., `united-states`). Exceptions: `new_zealand` uses underscore. Some countries on the page may not have PDFs available yet.
- **update_frequency:** OECD updates profiles periodically. Several marked "UPDATED (January 2026)" as of last check: Bosnia and Herzegovina, Brazil, Costa Rica, Croatia, Greece, Iceland, Korea, Norway.

---

## Big 4 / Advisory Firm Transfer Pricing Guides

- **directory:** `raw/advisories/`
- **last_checked:** 2026-04-29
- **notes:** Country-level TP summaries from Big 4 and other advisory firms. Includes worldwide guides (single PDF) and per-country publications.

Status: `New` (unprocessed) → `Compiled` (wiki article created) → `Verified` (human reviewed)

| File | Firm | Source URL | Year | Downloaded | Status |
|------|------|-----------|------|------------|--------|
| ey-worldwide-2025.pdf | EY | https://www.ey.com/content/dam/ey-unified-site/ey-com/en-gl/technical/tax-guides/documents/en-gl-worldwide-transfer-pricing-reference-guide-2025.pdf | 2025 | 2026-04-29 | Compiled |
| kpmg-global-tp-review-2023.pdf | KPMG | https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2023/kpmg-global-transfer-pricing-review.pdf | 2023 | 2026-04-29 | Compiled |
| deloitte-global-tp-doc-summary-2021.pdf | Deloitte | https://www.deloitte.com/au/en/services/tax/analysis/global-tax-reset-transfer-pricing-documentation-summary.html | 2021 | 2026-04-29 | Compiled |
