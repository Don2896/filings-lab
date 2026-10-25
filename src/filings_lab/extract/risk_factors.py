from dotenv import load_dotenv
from pathlib import Path
from filings_lab.ingest.edgar import get_cik, get_10k_filings, download_filing, extract_risk_factors

import anthropic
import json



load_dotenv()
client = anthropic.Anthropic()

SYSTEM = """You extract risks from SEC 10-K filings.
Return ONLY a JSON list. Each item has exactly these keys:
"category" (one of: supply_chain, competition, regulatory, macroeconomic, technology, legal, other, cybersecurity, geopolitical, operational, financial),
"title" (max 8 words), "summary" (one sentence).
No other text."""

sample = """We depend on a small number of suppliers in Asia for key components.
Governments may introduce new data privacy laws that restrict our services.
Intense competition could reduce our prices and margins."""


VALID_KEYS = {"category", "title", "summary"}
ALLOWED_CATEGORIES = {
    "supply_chain", "competition", "regulatory",
    "macroeconomic", "technology", "legal", "other","cybersecurity", 
    "geopolitical", "operational", "financial"
}

def validate_risks(risks: list) -> list:
    """Check each risk has exactly the right keys and an allowed category."""
    for item in risks:
        # 1. Is it a dict with exactly the right keys?
        if not isinstance(item, dict) or set(item.keys()) != VALID_KEYS:
            raise ValueError(f"Bad keys: {item}")
        # 2. Is the category one we allow?
        if item["category"] not in ALLOWED_CATEGORIES:
            raise ValueError(f"Bad category: {item['category']}")
    # 3. Everything passed, so hand the list back
    return risks


def extract_risks(text:str) -> list:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=8000,
        system=SYSTEM,
        messages= [{"role":"user", "content":text}]
    )
    if response.stop_reason == "max_tokens":
        raise RuntimeError("Response cut off: increase max_tokens")

    raw = response.content[0].text
    risks = json.loads(raw)
    return validate_risks(risks)



def save_risks(risks: list, out_path: Path) -> Path:
    """Save a list of risks to a JSON file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(risks, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    for ticker in ["AAPL", "MSFT"]:
        cik = get_cik(ticker)
        for filing in get_10k_filings(cik):          # returns 2 filings
            out_path = Path(f"data/processed/{ticker}/{filing['filing_date']}.json")

            if out_path.exists():
                print(f"already extracted: {out_path}")
                continue                              # skip to the next filing

            html_path = download_filing(cik, filing, ticker)
            text = extract_risk_factors(html_path)
            risks = extract_risks(text)
            save_risks(risks, out_path)
            print(f"{len(risks)} risks saved to {out_path}")