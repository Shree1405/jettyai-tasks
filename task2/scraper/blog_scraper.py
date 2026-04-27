import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape_blog(url):
    """Scrape a blog post and return structured data."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[Blog] Failed to fetch {url}: {e}")
        return _empty_blog(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title    = _extract_title(soup)
    author   = _extract_author(soup)
    date     = _extract_date(soup)
    chunks   = _extract_content(soup)
    domain   = _get_domain(url)
    has_disclaimer = _has_medical_disclaimer(soup)

    return {
        "title": title,
        "author": author,
        "published_date": date,
        "domain": domain,
        "has_medical_disclaimer": has_disclaimer,
        "content_chunks": chunks
    }

# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_title(soup):
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return soup.title.get_text(strip=True) if soup.title else "Unknown"

def _extract_author(soup):
    # Try common meta tags first
    for attr, val in [("name","author"), ("property","article:author"),
                      ("name","byl"), ("name","dc.creator")]:
        tag = soup.find("meta", {attr: val})
        if tag and tag.get("content"):
            return tag["content"].strip()

    # Try common HTML patterns
    for css in ["author", "byline", "article-author", "post-author",
                "entry-author", "writer", "contributor"]:
        tag = soup.find(class_=lambda c: c and css in c.lower())
        if tag:
            text = tag.get_text(strip=True)
            if text and len(text) < 100:
                return text

    # Try schema.org
    schema = soup.find("span", itemprop="author")
    if schema:
        return schema.get_text(strip=True)

    return "Unknown"

def _extract_date(soup):
    # Meta tags
    for attr, val in [("property","article:published_time"),
                      ("name","date"), ("name","pubdate"),
                      ("property","og:updated_time"),
                      ("name","DC.date.issued")]:
        tag = soup.find("meta", {attr: val})
        if tag and tag.get("content"):
            return tag["content"][:10]

    # <time> tag
    time_tag = soup.find("time")
    if time_tag:
        dt = time_tag.get("datetime") or time_tag.get_text(strip=True)
        return dt[:10] if dt else "Unknown"

    # Common CSS classes
    for css in ["date", "published", "post-date", "entry-date", "article-date"]:
        tag = soup.find(class_=lambda c: c and css in c.lower())
        if tag:
            return tag.get_text(strip=True)[:30]

    return "Unknown"

def _extract_content(soup):
    # Remove noise elements
    for tag in soup(["script","style","nav","header","footer",
                     "aside","form","iframe","noscript","ads"]):
        tag.decompose()

    # Try article / main content containers
    container = (soup.find("article") or
                 soup.find("main") or
                 soup.find(class_="sf-content-block") or
                 soup.find(class_=lambda c: c and "content" in str(c).lower()) or
                 soup.find("div", id=lambda i: i and "content" in str(i).lower()))

    paragraphs = []
    source = container if container else soup

    for p in source.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 60:          # skip short/nav text
            paragraphs.append(text)

    return paragraphs if paragraphs else ["Content could not be extracted."]

def _get_domain(url):
    from urllib.parse import urlparse
    return urlparse(url).netloc.replace("www.", "")

def _has_medical_disclaimer(soup):
    text = soup.get_text().lower()
    keywords = ["medically reviewed", "reviewed by", "medical disclaimer",
                "consult a doctor", "consult your physician",
                "not medical advice", "for informational purposes"]
    return any(kw in text for kw in keywords)

def _empty_blog(url):
    return {
        "title": "Unknown", "author": "Unknown",
        "published_date": "Unknown", "domain": _get_domain(url),
        "has_medical_disclaimer": False, "content_chunks": []
    }
