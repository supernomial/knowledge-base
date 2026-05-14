"""Refresh the Damodaran-sourced financial benchmark markdown files.

Run annually, after Damodaran publishes the January update.

Downloads the 12 source .xls files (3 datasets × 4 geographies), joins them on
"Industry Name" per geo, and rewrites each geo's markdown file under
`financial-benchmarks/damodaran/<geo>-<year>.md`.

The rating-coverage table and the rule-of-thumb / mapping / sources files are
maintained by hand — this script does not touch them.

Usage:
    python3 scripts/refresh_financial_benchmarks.py [--year 2027] [--out financial-benchmarks]
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas is required. Install via `pip install pandas xlrd`.")


GEOS = (
    # geo_id, label, filename suffix
    ("us", "United States", ""),
    ("europe", "Europe", "Europe"),
    ("global", "Global", "Global"),
    ("emerging", "Emerging Markets", "emerg"),
)

DATASETS = (
    # dataset_id, filename prefix, sheet to read
    ("margin", "margin", "Industry Averages"),
    ("dbtfund", "dbtfund", "Industry Averages"),
    ("roe", "roe", "Industry Averages"),
)

BASE_URL = "https://pages.stern.nyu.edu/~adamodar/pc/datasets"


def fetch(prefix: str, suffix: str, tmpdir: Path) -> Path:
    url = f"{BASE_URL}/{prefix}{suffix}.xls"
    target = tmpdir / f"{prefix}{suffix or 'US'}.xls"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        target.write_bytes(response.read())
    return target


def read_industry_table(path: Path) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name="Industry Averages", engine="xlrd", header=None)
    header_row = None
    for idx in range(min(15, len(raw))):
        first = raw.iloc[idx, 0]
        if isinstance(first, str) and first.strip().startswith("Industry"):
            header_row = idx
            break
    if header_row is None:
        raise RuntimeError(f"Industry Name header not found in {path}")
    df = pd.read_excel(path, sheet_name="Industry Averages", engine="xlrd", header=header_row)
    df = df.dropna(subset=[df.columns[0]])
    df = df[~df.iloc[:, 0].astype(str).str.contains("Total Market", case=False, na=False)]
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={df.columns[0]: "Industry Name"})
    return df.reset_index(drop=True)


def find_col(df: pd.DataFrame, *patterns: str) -> str | None:
    for col in df.columns:
        for p in patterns:
            if re.search(p, col, re.IGNORECASE):
                return col
    return None


def fmt_pct(v) -> str:
    try:
        if pd.isna(v):
            return "—"
        return f"{float(v) * 100:.2f}%"
    except (TypeError, ValueError):
        return "—"


def fmt_x(v) -> str:
    try:
        if pd.isna(v):
            return "—"
        return f"{float(v):.2f}x"
    except (TypeError, ValueError):
        return "—"


def fmt_int(v) -> str:
    try:
        if pd.isna(v):
            return "—"
        return str(int(float(v)))
    except (TypeError, ValueError):
        return "—"


def build_geo_markdown(
    geo_id: str,
    geo_label: str,
    suffix: str,
    year: str,
    accessed: str,
    margin_df: pd.DataFrame,
    dbt_df: pd.DataFrame,
    roe_df: pd.DataFrame,
) -> str:
    op_col = find_col(margin_df, r"^Pre-tax Unadjusted Operating Margin", r"^Pre-tax.*Operating Margin")
    ebitda_col = find_col(margin_df, r"EBITDA/Sales$")
    net_col = find_col(margin_df, r"^Net Margin$")

    book_dc = find_col(dbt_df, r"^Book Debt to Capital$")
    mkt_dc = find_col(dbt_df, r"^Market Debt to Capital \(Unadjusted")
    mkt_de = find_col(dbt_df, r"^Market D/E \(unadjusted")
    intcov = find_col(dbt_df, r"Interest Coverage")
    debt_ebitda = find_col(dbt_df, r"Debt.*EBITDA")

    roe_col = find_col(roe_df, r"^ROE \(unadjusted\)$")

    merged = margin_df[["Industry Name", "Number of firms"]].copy()
    merged["Op Margin"] = margin_df[op_col] if op_col else None
    merged["EBITDA Margin"] = margin_df[ebitda_col] if ebitda_col else None
    merged["Net Margin"] = margin_df[net_col] if net_col else None

    dbt_keep = [c for c in (book_dc, mkt_dc, mkt_de, intcov, debt_ebitda) if c]
    dbt_names = [
        name
        for name, present in zip(
            ("Book D/Cap", "Market D/Cap", "Market D/E", "EBIT/Interest", "Debt/EBITDA"),
            (book_dc, mkt_dc, mkt_de, intcov, debt_ebitda),
        )
        if present
    ]
    if dbt_keep:
        dbt_sub = dbt_df[["Industry Name"] + dbt_keep].copy()
        dbt_sub.columns = ["Industry Name"] + dbt_names
        merged = merged.merge(dbt_sub, on="Industry Name", how="left")

    if roe_col:
        roe_sub = roe_df[["Industry Name", roe_col]].copy()
        roe_sub.columns = ["Industry Name", "ROE"]
        merged = merged.merge(roe_sub, on="Industry Name", how="left")

    geo_url_suffix = suffix or ""
    lines: list[str] = [
        "---",
        "source: Damodaran NYU Stern",
        f"geo: {geo_label}",
        f"release_year: {year}",
        f"accessed: {accessed}",
        "urls:",
        f"  margins: {BASE_URL}/margin{geo_url_suffix}.xls",
        f"  capital_structure: {BASE_URL}/dbtfund{geo_url_suffix}.xls",
        f"  roe: {BASE_URL}/roe{geo_url_suffix}.xls",
        "ratios:",
        "  - op_margin: Pre-tax operating profit / revenue",
        "  - ebitda_margin: EBITDA / revenue",
        "  - net_margin: Net income / revenue",
        "  - book_d_cap: Book debt / (book debt + book equity)",
        "  - market_d_cap: Market debt / (market debt + market equity)",
        "  - market_d_e: Market debt / market equity",
        "  - ebit_interest: EBIT / interest expense",
        "  - debt_ebitda: Total debt / EBITDA",
        "  - roe: Net income / book equity",
        "---",
        "",
        f"# Damodaran Industry Medians — {geo_label} ({year})",
        "",
        f"Public companies covered: {int(merged['Number of firms'].fillna(0).sum())}. "
        f"Industries: {len(merged)}. "
        f"Source: Damodaran NYU Stern, {year} release; accessed {accessed}.",
        "",
        "| Industry | # Firms | Op Margin | EBITDA Margin | Net Margin | Book D/Cap | Market D/Cap | Market D/E | EBIT/Interest | Debt/EBITDA | ROE |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for _, row in merged.iterrows():
        industry = str(row["Industry Name"]).strip()
        if not industry or industry.lower().startswith("nan"):
            continue
        lines.append(
            "| "
            + " | ".join(
                (
                    industry,
                    fmt_int(row.get("Number of firms")),
                    fmt_pct(row.get("Op Margin")),
                    fmt_pct(row.get("EBITDA Margin")),
                    fmt_pct(row.get("Net Margin")),
                    fmt_pct(row.get("Book D/Cap")),
                    fmt_pct(row.get("Market D/Cap")),
                    fmt_pct(row.get("Market D/E")),
                    fmt_x(row.get("EBIT/Interest")),
                    fmt_x(row.get("Debt/EBITDA")),
                    fmt_pct(row.get("ROE")),
                )
            )
            + " |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh Damodaran financial benchmark files.")
    parser.add_argument("--year", default=str(date.today().year), help="Release year tag (default: current year)")
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent.parent / "financial-benchmarks"),
        help="Output folder (default: ../financial-benchmarks)",
    )
    args = parser.parse_args()

    out_root = Path(args.out)
    damodaran_dir = out_root / "damodaran"
    damodaran_dir.mkdir(parents=True, exist_ok=True)

    accessed = date.today().isoformat()

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for geo_id, geo_label, suffix in GEOS:
            margin = fetch("margin", suffix, tmpdir)
            dbt = fetch("dbtfund", suffix, tmpdir)
            roe = fetch("roe", suffix, tmpdir)

            margin_df = read_industry_table(margin)
            dbt_df = read_industry_table(dbt)
            roe_df = read_industry_table(roe)

            md = build_geo_markdown(geo_id, geo_label, suffix, args.year, accessed, margin_df, dbt_df, roe_df)
            target = damodaran_dir / f"{geo_id}-{args.year}.md"
            target.write_text(md)
            print(f"  ✓ {geo_label:<20s} {len(margin_df):>3} industries → {target.relative_to(out_root.parent)}")

    print()
    print(f"Output ready under {out_root}.")
    print("Remember to: (1) git add the new files, (2) bump manifest.md 'Updated' date, (3) commit + push.")


if __name__ == "__main__":
    main()
