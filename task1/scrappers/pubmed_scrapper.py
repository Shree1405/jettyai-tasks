import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

ua = UserAgent()

def scrape_pubmed(url):
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
    }

    try:
        with httpx.Client(follow_redirects=True, headers=headers, timeout=15.0) as client:
            # PubMed often blocks, try making it look very real
            response = client.get(url)
            response.raise_for_status()
            html = response.text
    except Exception as e:
        print(f"Error fetching PubMed {url}: {e}")
        return {"title": "Error", "author": "Unknown", "published_date": "Unknown", "content_chunks": []}

    soup = BeautifulSoup(html, "html.parser")

    # Title
    title = soup.find("h1", class_="heading-title")
    title = title.get_text(strip=True) if title else "Unknown"

    # Authors - multiple patterns
    authors = [a.get_text(strip=True) for a in soup.find_all("a", class_="full-name")]
    if not authors:
        authors = [meta.get("content") for meta in soup.find_all("meta", attrs={"name": "citation_author"})]

    # Journal
    journal = soup.find("button", id="full-view-journal-trigger") or soup.find("meta", attrs={"name": "citation_journal_title"})
    if journal:
        journal = journal.get_text(strip=True) if hasattr(journal, "get_text") else journal.get("content")
    else:
        journal = "Unknown"

    # Abstract
    abstract_div = soup.find("div", class_="abstract-content") or soup.find("div", id="abstract")
    if abstract_div:
        paragraphs = [p.get_text(strip=True) for p in abstract_div.find_all("p") if p.get_text(strip=True)]
    else:
        # Try meta tags
        abstract_meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        paragraphs = [abstract_meta.get("content")] if abstract_meta else []

    # Year
    year = soup.find("span", class_="cit") or soup.find("meta", attrs={"name": "citation_publication_date"})
    if year:
        year_text = year.get_text(strip=True) if hasattr(year, "get_text") else year.get("content")
        match = re.search(r"\d{4}", year_text)
        year = match.group(0) if match else "Unknown"
    else:
        year = "Unknown"

    return {
        "title": title,
        "author": ", ".join(authors) if authors else "Unknown",
        "published_date": year,
        "journal": journal,
        "content_chunks": paragraphs
    }