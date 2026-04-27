import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape_pubmed(url):
    """Scrape a PubMed article and return structured data."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[PubMed] Failed to fetch {url}: {e}")
        return _empty_pubmed(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title   = _extract_title(soup)
    authors = _extract_authors(soup)
    journal = _extract_journal(soup)
    year    = _extract_year(soup)
    chunks  = _extract_abstract(soup)

    return {
        "title": title,
        "author": authors,          # list of authors
        "published_date": year,
        "journal": journal,
        "domain": "pubmed.ncbi.nlm.nih.gov",
        "has_medical_disclaimer": True,   # PubMed is always peer-reviewed
        "content_chunks": chunks
    }

# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_title(soup):
    tag = soup.find("h1", class_="heading-title")
    if tag:
        return tag.get_text(strip=True)
    og = soup.find("meta", property="og:title")
    if og:
        return og["content"].strip()
    return "Unknown"

def _extract_authors(soup):
    """Returns a list of author name strings."""
    authors = []
    # Primary: full-name links
    for a in soup.find_all("a", class_="full-name"):
        name = a.get_text(strip=True)
        if name:
            authors.append(name)
    # Fallback: author spans
    if not authors:
        for span in soup.find_all("span", class_="authors-list-item"):
            name = span.get_text(strip=True)
            if name:
                authors.append(name)
    return authors if authors else ["Unknown"]

def _extract_journal(soup):
    btn = soup.find("button", id="full-view-journal-trigger")
    if btn:
        return btn.get_text(strip=True)
    tag = soup.find("meta", attrs={"name": "citation_journal_title"})
    if tag:
        return tag["content"].strip()
    return "Unknown"

def _extract_year(soup):
    # Citation span usually contains "2023 Jan;..."
    cit = soup.find("span", class_="cit")
    if cit:
        text = cit.get_text(strip=True)
        import re
        match = re.search(r"\b(19|20)\d{2}\b", text)
        if match:
            return match.group(0)
    tag = soup.find("meta", attrs={"name": "citation_publication_date"})
    if tag:
        return tag["content"][:4]
    return "Unknown"

def _extract_abstract(soup):
    div = soup.find("div", class_="abstract-content")
    if div:
        chunks = [p.get_text(strip=True) for p in div.find_all("p") if p.get_text(strip=True)]
        return chunks if chunks else [div.get_text(strip=True)]

    # Fallback: og:description
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        return [og["content"].strip()]

    return ["Abstract not available."]

def _empty_pubmed(url):
    return {
        "title": "Unknown", "author": ["Unknown"],
        "published_date": "Unknown", "journal": "Unknown",
        "domain": "pubmed.ncbi.nlm.nih.gov",
        "has_medical_disclaimer": True,
        "content_chunks": []
    }
