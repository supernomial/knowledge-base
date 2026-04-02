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
