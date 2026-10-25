# Filings Lab

A data platform that ingests SEC 10-K filings, uses an LLM to extract structured
risk factors, and (in progress) serves an AI research agent on top.

**Status:** in progress. Ingestion and LLM extraction work; tools and agent are next.

## What it does today
1. **Ingest:** looks up a company on SEC EDGAR, finds its latest 10-Ks and downloads them (cached, with SEC-compliant headers and block-page detection).
2. **Extract section:** cleans the HTML and isolates Item 1A (Risk Factors), skipping the table of contents and cross-references.
3. **Extract risks with Claude:** returns a JSON list of risks, each with a category, title and one-sentence summary. Output is parsed and validated (exact keys, allowed categories) before saving, and results are cached so each filing is only sent to Claude once.

Example output (`data/processed/AAPL/2025-10-31.json`):
```json
{
  "category": "geopolitical",
  "title": "Tariffs and international trade restrictions",
  "summary": "New U.S. tariffs, retaliatory measures and potential Section 232 semiconductor tariffs can raise costs, limit product availability and force costly supply chain restructuring."
}
```

## Architecture
```
EDGAR → ingest/edgar.py → extract/risk_factors.py → data/processed/*.json
                                                  → tools → agent → MCP server (planned)
```

## Setup
```bash
git clone https://github.com/Don2896/filings-lab.git
cd filings-lab
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your SEC_USER_AGENT and ANTHROPIC_API_KEY
```

## Usage
```bash
PYTHONPATH=src python -m filings_lab.extract.risk_factors
```

## Roadmap
- [x] EDGAR ingestion with caching
- [x] Item 1A extraction
- [x] LLM risk extraction with validation
- [ ] Year-over-year comparison of risks
- [ ] Tool use: let Claude call the ingestion functions
- [ ] Research agent
- [ ] MCP server
- [ ] Tests, Docker, demo