# Supernomial Knowledge Base

Transfer pricing knowledge base for the Supernomial Cowork plugin. Contains jurisdiction profiles, regulatory data, and domain expertise that plugin review agents consume at runtime.

## Structure

```
manifest.md                  Master index of available experts and knowledge files
experts/                     Agent prompts (thin — point to knowledge files)
  countries/                 Country expert agents
  topics/                    Topic expert agents (local files, CbCR, etc.)
  transactions/              Transaction expert agents
  industries/                Industry expert agents
knowledge/                   Synthesized knowledge consumed by expert agents
  countries/
    united-states/
      country-profile.md     Synthesized country profile (all sources merged)
extracted/                   Verbatim extractions from source documents
  advisories/
    ey-worldwide-2025/       EY Worldwide TP Reference Guide 2025
    kpmg-worldwide-2025/     KPMG Global TP Review 2025
    deloitte-global-tp-doc-summary-2021.md
raw/                         Source PDFs (not committed to repo)
  advisories/
```

## How It Works

The Supernomial Cowork plugin fetches knowledge from this repo at runtime. When a user asks for an expert review of their transfer pricing work, the plugin:

1. Reads `manifest.json` to discover available experts
2. Presents available experts to the user
3. Fetches the relevant knowledge files
4. Reviews the user's deliverable against the regulatory data

## Sources

Knowledge files are derived from authoritative public sources:

- **OECD Transfer Pricing Country Profiles** — standardized regulatory questionnaires published by the OECD, filled by each jurisdiction
- **EY Worldwide Transfer Pricing Reference Guide** — comprehensive per-country TP compliance guide (annual)
- **KPMG Global Transfer Pricing Review** — per-country TP documentation summary (annual)
- **Deloitte Global Tax Reset — Transfer Pricing Documentation Summary** — CbCR and documentation overview (2021)
- Future: OECD Transfer Pricing Guidelines, case law, administrative practice

## Two-Layer Architecture: Extracted vs. Knowledge

The knowledge base has two layers that serve different purposes:

### Layer 1: `extracted/` — Verbatim source extractions

Each source document (EY, KPMG, Deloitte, etc.) is extracted into its own file with exact wording from the source. These files:
- Use the source document's own headers, question text, and labels verbatim
- Never paraphrase or summarize
- Include YAML frontmatter with `extraction_method: visual` when extracted by reading PDF pages as images
- Never include personal contact information
- Are the **source of truth** — one file per source per jurisdiction

### Layer 2: `knowledge/` — Synthesized country profiles

Country profiles in `knowledge/countries/<country>/country-profile.md` are **synthesized** from all available extracted sources. These files:
- Merge information from all sources into a single comprehensive profile
- Use a layered-detail structure: "Quick Reference" bullets for fast lookup, "Detailed Rules" for full regulatory text
- Include a "Key Facts at a Glance" table at the top
- Cite every fact with its source in parentheses, e.g., `(EY 2025)`, `(KPMG 2025)`, `(OECD)`
- Are the **primary knowledge** consumed by expert agents at runtime
- List all sources and compilation date in YAML frontmatter under `synthesis:`

### Why two layers?

- **Maintainability:** When a source updates (e.g., EY 2026), re-extract verbatim, then re-synthesize. No duplication to keep in sync.
- **Accuracy:** Extracted files preserve exact source wording for citation. Synthesis merges and resolves across sources at build time.
- **Speed:** Expert agents read only the synthesized profile (~500 lines). They don't need to fetch and cross-reference 3-4 source files.
- **Traceability:** Every fact in the synthesis cites its source. If the agent needs exact source wording, the extracted file is available.

## Workflow: Adding or Updating a Country

### Step 1: Extract from source documents

For each advisory source (EY, KPMG, Deloitte, etc.):

1. Find the country's pages in the source PDF (`raw/advisories/`)
2. Render pages as images (visual extraction via pymupdf)
3. Read the images and transcribe content verbatim into structured markdown
4. Use the source document's exact headers, question text, and labels — do not paraphrase
5. Save to `extracted/advisories/<source-name>/<country>.md` with YAML frontmatter including `extraction_method: visual`
6. Never include personal contact information (names, emails)

### Step 2: Synthesize the country profile

1. Run **3 parallel synthesis agents**, each with a different organizational approach:
   - **Agent A — Topic-organized:** Follows regulatory topic structure (methods, comparability, documentation, etc.)
   - **Agent B — Practitioner-use-case:** Organized by what practitioners look up (obligations, deadlines, penalties, audit risks)
   - **Agent C — Layered-detail:** Quick-reference bullets + detailed rules per section, with a Key Facts table at top
2. Compare the three outputs for completeness, structure, and lookup efficiency
3. Select the best approach (typically layered-detail — it optimizes for both fast and deep lookups)
4. Apply minor cleanups (remove duplicate sections, consolidate orphan single-line sections)
5. Write to `knowledge/countries/<country>/country-profile.md` with YAML frontmatter documenting all sources under `synthesis:`

### Step 3: Update manifest

Add the country's knowledge files to the `Knowledge files` table in `manifest.md`.

## Contributing

Knowledge files follow a structured markdown format with YAML frontmatter. See existing files for the template. Each file must declare its source, coverage, and extraction date in the frontmatter.

## Architecture Decisions

### File format: Markdown (not JSON)

Knowledge files use structured markdown with YAML frontmatter. The primary consumer is Claude (an LLM), not code. Markdown is:
- More token-efficient than JSON (no syntactic overhead from braces, quotes, commas)
- Better for explanatory text (regulatory paragraphs are natural language, not escaped strings)
- More robust to produce (malformed markdown doesn't break; malformed JSON does)
- Human-readable on GitHub and in diffs
- Equally navigable by Claude (LLMs don't do field lookups — they read text and reason)

JSON is used only for structured metadata: `manifest.json` (routing/discovery) and tree indexes (navigation).

### Scaling to large documents: tree indexes + split files

For small documents (country profiles, ~15 pages): fetch and read the full file. Fits in context.

For large documents (OECD Guidelines 600+ pages, case law corpora): use a tree index + split files.

```
oecd-tpg/
  index.json                Tree structure with section-to-file mapping
  chapter-02-methods.md     ~30 pages each — agent fetches only what it needs
  chapter-03-comparability.md
  ...
```

The tree index tells the agent where to look (~2K tokens). The agent fetches only the relevant chapter file(s) instead of the whole document. This gives ~80% token savings when consulting multiple sources.

### Tree indexing: heading parser (not LLM)

We evaluated PageIndex (LLM-based tree indexing, github.com/VectifyAI/PageIndex). Findings:

- PageIndex uses LLM calls to build tree indexes: ~$0.03 for a 15-page doc, ~$5-15 for 600 pages
- This doesn't scale to thousands of court documents
- Most TP sources are well-structured (clear headings, numbered paragraphs, published TOCs)
- A simple heading parser builds the same tree JSON for $0, instantly

**Decision:** Use a zero-cost heading parser for structured documents (90% of TP sources). Reserve PageIndex only for messy/unstructured PDFs where headings can't be parsed deterministically. The tree JSON format is identical either way — agents don't care how it was built.

| Document type | Indexing method | Cost |
|---|---|---|
| OECD Guidelines, country profiles | Heading parser | $0 |
| Tax legislation, court decisions | Section/paragraph parser | $0 |
| Messy scanned PDFs, old rulings | PageIndex (LLM-based) | ~$0.03-15/doc |
| Born-digital PDFs | EdgeParse (Rust, deterministic) | $0, 0.064 sec/doc |

### Runtime retrieval in Cowork

Cowork agents can fetch public URLs but cannot run Python. This means:
- PageIndex's Python retrieval API (`get_page_content`) doesn't work at runtime
- Selective retrieval is achieved by **pre-splitting documents into section files** during the build phase
- The agent reads the tree index from GitHub, identifies relevant sections, then fetches only those section files
- No MCP server or local infrastructure required on the user's machine

### Build pipeline (future)

Agents running on the maintainer's machine will:
1. Download source documents (OECD website, tax authority portals, court databases)
2. Extract text (EdgeParse for born-digital PDFs, Chandra OCR for scanned docs)
3. Build tree index (heading parser for structured docs, PageIndex for messy ones)
4. Split into section files based on the tree
5. Generate structured markdown with YAML frontmatter
6. Push to this repo with updated manifest.json

### Tools evaluated (2026-04-02, updated 2026-04-30)

| Tool | Verdict | Notes |
|---|---|---|
| PageIndex | Use selectively | Good for messy PDFs, overkill for structured docs. MIT license, 23K stars |
| RAGFlow | Too heavy | Enterprise RAG platform, 5+ Docker containers, 16GB RAM. Overkill |
| EdgeParse | Strong for extraction | Rust-native PDF extraction, 0.064 sec/doc, macOS native. Very new (Apache 2.0) |
| Nutrient (PSPDFKit) | Good for simple PDFs | Free <1K docs/mo, 0.011s/page, strong reading order (0.93). Installed as Claude Code skill. Fails on complex landscape tables (Deloitte TP summary) |
| OpenDataLoader | Promising, not tested | #1 accuracy (0.907), 0.93 table score, Apache 2.0. Requires Java runtime |
| MinerU | Future option | SOTA accuracy, cross-page table merging. Heavy install, needs GPU for best results |
| MarkItDown (Microsoft) | Weak for tables | Good for simple text extraction. Tables lose structure on complex layouts |
| pdfplumber | Weak for complex tables | Good for simple bordered tables. Fragments on multi-level headers |
| Chandra | Niche — scanned docs | OCR model, needs GPU. Use hosted API for occasional scanned docs |
| TinyFish | Wrong category | Web automation, not document processing |
| FOLIO/Open Legal Standard | Not relevant | Legal taxonomy with zero TP concepts |
| knowledge-rag (MCP) | Future option | Best local RAG MCP server if we ever need vector search (hybrid search + reranking) |

**Note on complex landscape tables:** No tool tested (Nutrient, EdgeParse, MarkItDown, pdfplumber) correctly extracts the Deloitte Global TP Documentation Summary — a landscape PDF with multi-level merged headers and icon-based values. Custom pymupdf position-based parsing with visual verification remains the best approach for these edge cases.
