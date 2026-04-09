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
