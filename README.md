# Supernomial Knowledge Base

Transfer pricing knowledge base for the Supernomial Cowork plugin. Contains jurisdiction profiles, regulatory data, and domain expertise that plugin review agents consume at runtime.

## Structure

```
manifest.json              Master index of available expert knowledge
jurisdictions/             Country-specific TP regulatory profiles
  us/                      United States
    country-profile.md     OECD TP Country Profile (structured markdown)
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
- Future: OECD Transfer Pricing Guidelines, case law, administrative practice

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

### Tools evaluated (2026-04-02)

| Tool | Verdict | Notes |
|---|---|---|
| PageIndex | Use selectively | Good for messy PDFs, overkill for structured docs. MIT license, 23K stars |
| RAGFlow | Too heavy | Enterprise RAG platform, 5+ Docker containers, 16GB RAM. Overkill |
| EdgeParse | Strong for extraction | Rust-native PDF extraction, 0.064 sec/doc, macOS native. Very new (Apache 2.0) |
| Chandra | Niche — scanned docs | OCR model, needs GPU. Use hosted API for occasional scanned docs |
| TinyFish | Wrong category | Web automation, not document processing |
| FOLIO/Open Legal Standard | Not relevant | Legal taxonomy with zero TP concepts |
| knowledge-rag (MCP) | Future option | Best local RAG MCP server if we ever need vector search (hybrid search + reranking) |
