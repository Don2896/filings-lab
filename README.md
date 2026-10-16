# filings-lab

A data platform that ingests SEC filings and market data, extracts structured signals with an LLM, and serves an AI research agent and dashboard.

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
