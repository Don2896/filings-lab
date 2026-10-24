# filings-lab

A data platform that ingests SEC filings and market data, extracts structured signals with an LLM, and serves an AI research agent and dashboard.

What it is: a data platform that pulls in companies’ official SEC filings (10-Ks) and market data, uses an LLM to extract structured information from the text, and puts an AI research agent and dashboard on top.

The pipeline:

Ingest: download filings from EDGAR. (This is where you are now.)
Extract: Claude turns sections like Risk Factors into structured data.
Store: save the results in a database.
Tools and agent: Claude can fetch filings and query the data itself to answer questions like “What new risks did Apple add this year?”
MCP server and dashboard: expose the data to other AI tools and show it visually.

What it’s meant to achieve:

For a user: analysts at funds read thousands of filings looking for changes in risk, guidance or tone. Filings Lab automates that reading and highlights what changed between years.
For you: one portfolio project that shows data engineering, production LLM use and agents on real financial data. It’s relevant to AI engineering roles and the systematic funds you’re targeting, and it’s the place where every Track A topic gets applied for real.

**Status:** in progress

## Planned architecture

1. **Ingest**: pull SEC filings and market data
2. **Extract**: turn filings into structured signals with an LLM
3. **Tools**: query functions over the extracted data
4. **Agent**: AI research agent that uses the tools
5. **MCP server**: expose the tools over the Model Context Protocol
6. **Dashboard**: visualise signals and research output

```
ingest → extract → tools → agent → MCP server → dashboard
```

## Setup

_TBD_

## Roadmap

_TBD_
