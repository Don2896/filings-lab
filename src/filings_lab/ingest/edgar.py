from pathlib import Path
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)



load_dotenv()                                   # reads your .env file
HEADERS = {"User-Agent": os.getenv("SEC_USER_AGENT")}

def fetch_json(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def save_text(ticker, filing, url) -> Path:
    html_path = Path(f"data/raw/{ticker}/{filing['filing_date']}.html")
    if not html_path.exists():
        html_path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        if "Undeclared Automated Tool" in response.text:
            raise RuntimeError("SEC blocked the request: check your User-Agent")
        html_path.write_text(response.text, encoding="utf-8")
        print(f'downloaded to {html_path}')
    else:
        print(f'already saved to {html_path}')
    return html_path



def get_cik(ticker: str) -> str:
    """Return the 10-digit zero-padded CIK for a ticker, e.g. 'AAPL' -> '0000320193'.
    Source: https://www.sec.gov/files/company_tickers.json
    Raise ValueError if the ticker isn't found."""

    cik = fetch_json("https://www.sec.gov/files/company_tickers.json")
    for item in cik.values():
        if item["ticker"].upper() == ticker.upper():
            return str(item["cik_str"]).zfill(10)
    raise ValueError(f'Ticker {ticker} not found')
    



def get_10k_filings(cik: str, n: int = 2) -> list[dict]:
    """Return the n most recent 10-K filings as dicts with keys:
    accession_number, filing_date, primary_document.
    Source: https://data.sec.gov/submissions/CIK{cik}.json
    Hint: filings['recent'] holds parallel lists (form, accessionNumber,
    filingDate, primaryDocument); zip them and filter where form == '10-K'."""
    ten_k_filings = []
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    filings = fetch_json(url)
    recent = filings['filings']['recent']
    for form, accession_number, filing_date, primary_document in zip(
        recent["form"],
        recent["accessionNumber"],
        recent["filingDate"],
        recent["primaryDocument"]
    ):
        if form == "10-K":
            ten_k_filings.append(
                {
                    "accession_number": accession_number,
                    "filing_date": filing_date,
                    "primary_document": primary_document,
                }
            )
    return ten_k_filings[:n]

def download_filing(cik: str, filing: dict, ticker: str) -> Path:
    """Download the primary document and save to data/raw/{ticker}/{filing_date}.html.
    URL format: https://www.sec.gov/Archives/edgar/data/{cik_without_leading_zeros}/
                {accession_number_without_dashes}/{primary_document}
    Skip the download if the file already exists (saves hitting the SEC repeatedly)."""

    cik_without_leading_zeros = str(int(cik))

    accession_number_without_dashes = filing["accession_number"].replace("-", "")

    url = f"https://www.sec.gov/Archives/edgar/data/{cik_without_leading_zeros}/{accession_number_without_dashes}/{filing['primary_document']}"

    return save_text(ticker, filing, url)



def extract_risk_factors(html_path: Path) -> str:
    """Return the plain text of Item 1A (Risk Factors).
    Strip HTML with BeautifulSoup, then take text between 'Item 1A' and 'Item 1B'
    (fall back to 'Item 2' if 1B is missing)."""
    from bs4 import BeautifulSoup

    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")

    start_index = text.find("Item 1A")
    end_index = text.find("Item 1B", start_index)
    if end_index == -1:
        end_index = text.find("Item 2", start_index)
    if start_index == -1 or end_index == -1:
        raise ValueError(f"Could not find Item 1A in {html_path}")
    return text[start_index:end_index].strip()


