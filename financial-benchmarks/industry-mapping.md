---
title: Sector → Damodaran Industry Mapping
accessed: 2026-05-14
purpose: Map smartZebra sector codes (and common NAICS / SIC categories) to Damodaran industry names so the Financial Capacity skill can look up the right benchmark row.
---

# Sector → Damodaran Industry Mapping

Damodaran groups public companies into ~94 industries (US count; Europe / Global counts vary slightly). The skill needs to map the tested party's industry — captured in the intake workbook as either a smartZebra sector code or a free-text description — onto a Damodaran industry name.

For ambiguous mappings (e.g. a specialty-chemicals firm that could plausibly fit "Chemical (Specialty)" or "Diversified Chemicals"), the skill asks the user to pick. The selected mapping is saved in `data.json` for the entity so subsequent runs reuse it.

## Common smartZebra sector codes → Damodaran industries

The codes below come from smartZebra's Workflow B Sector picker. Where smartZebra carries multiple example companies for a code (e.g. "BASF, Symrise" for Process Industries), the example companies are used to disambiguate to the closest Damodaran row.

| smartZebra code (example) | Likely Damodaran industry | Notes |
|---|---|---|
| 1000 — Energy | Oil/Gas (Integrated), Oil/Gas (Production and Exploration), Oilfield Services/Equipment | Pick by activity. |
| 1300 — Materials (broad) | Chemical (Specialty), Chemical (Basic), Chemical (Diversified), Metals & Mining, Paper/Forest Products, Building Materials | Most TP cases are subcategories. |
| 2200 — Process Industries | Chemical (Specialty) — primary; Chemical (Basic) for commodity petrochems; Chemical (Diversified) for groups with broad portfolios | Helios-class specialty chemicals → Chemical (Specialty). |
| 2300 — Producer Manufacturing | Machinery, Auto Parts, Aerospace/Defense, Electrical Equipment | Pick by end-market. |
| 2400 — Electronic Technology | Semiconductor, Semiconductor Equip, Computer Services, Software (System & Application) | Pick by sub-sector. |
| 3000 — Health Technology | Drugs (Biotechnology), Drugs (Pharmaceutical), Healthcare Products, Healthcare Support Services | Drugs = pharma; Products = devices. |
| 3500 — Communications | Telecom (Wireless), Telecom Services, Cable TV, Broadcasting | — |
| 3700 — Health Services | Healthcare Information and Technology, Hospitals/Healthcare Facilities, Healthcare Support Services | — |
| 4500 — Consumer Non-Durables | Beverage (Alcoholic), Beverage (Soft), Food Processing, Tobacco, Household Products | Food/Beverage/HPC. |
| 4600 — Consumer Durables | Auto & Truck, Auto Parts, Furn/Home Furnishings, Recreation | — |
| 5300 — Retail Trade | Retail (Distributors), Retail (Online), Retail (Special Lines), Retail (Grocery and Food) | Pick by channel. |
| 5500 — Transportation | Air Transport, Trucking, Shipbuilding & Marine, Transportation (Railroads) | — |
| 6000 — Finance | Bank (Money Center), Banks (Regional), Insurance, Investments & Asset Management, Financial Svcs. (Non-bank & Insurance) | Generally use Damodaran's financial-services tables, not the industrial benchmarks. |
| 6900 — Utilities | Power, Utility (General), Utility (Water) | — |
| 7000 — Industrial Services | Construction Supplies, Engineering/Construction, Real Estate | — |
| 8000 — Commercial Services | Business & Consumer Services, Advertising, Office Equipment & Services | — |

## Damodaran industry list (US 2026 release, 94 industries)

The authoritative list of Damodaran industry names is published in each geo's benchmark file (e.g. `damodaran/europe-2026.md`). When in doubt, the skill should display the available industries to the user and let them pick.

Common TP-relevant industries (subset, for quick reference):

- Advertising
- Aerospace/Defense
- Apparel
- Auto & Truck / Auto Parts
- Bank (Money Center) / Banks (Regional)
- Beverage (Alcoholic) / Beverage (Soft)
- Building Materials
- Business & Consumer Services
- Chemical (Basic) / Chemical (Diversified) / Chemical (Specialty)
- Computer Services
- Construction Supplies
- Diversified
- Drugs (Biotechnology) / Drugs (Pharmaceutical)
- Electronics (Consumer & Office) / Electronics (General)
- Engineering/Construction
- Entertainment
- Food Processing / Food Wholesalers
- Furn/Home Furnishings
- Healthcare Products / Healthcare Support Services
- Homebuilding
- Hospitals/Healthcare Facilities
- Household Products
- Information Services
- Insurance (General) / Insurance (Life) / Insurance (Prop/Cas.)
- Investments & Asset Management
- Machinery
- Metals & Mining
- Oil/Gas (Integrated) / Oil/Gas (Production and Exploration)
- Oilfield Services/Equipment
- Packaging & Container
- Paper/Forest Products
- Power
- R.E.I.T.
- Real Estate (General/Diversified) / Real Estate (Operations & Services)
- Recreation
- Restaurant/Dining
- Retail (Building Supply) / Retail (Distributors) / Retail (General) / Retail (Grocery and Food) / Retail (Online) / Retail (Special Lines)
- Rubber& Tires
- Semiconductor / Semiconductor Equip
- Shipbuilding & Marine
- Shoe
- Software (Entertainment) / Software (Internet) / Software (System & Application)
- Steel
- Telecom (Wireless) / Telecom Services
- Tobacco
- Transportation / Transportation (Railroads)
- Trucking
- Utility (General) / Utility (Water)

## When the user's sector is unclear

If the workbook's sector field doesn't map cleanly, the skill should:

1. Show the user the 3–5 candidate Damodaran industries that match the workbook description.
2. Ask the user to pick the closest one.
3. Save the choice to `data.json` for this entity.
4. Re-use the saved choice on subsequent runs without asking again.
