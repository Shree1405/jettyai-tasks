import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

def scrape_blog(url):
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    try:
        with httpx.Client(follow_redirects=True, headers=headers, timeout=15.0) as client:
            response = client.get(url)
            response.raise_for_status()
            html = response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {"title": "Error", "author": "Unknown", "published_date": "Unknown", "content_chunks": []}

    soup = BeautifulSoup(html, "html.parser")

    # Metadata extraction via Meta Tags
    title = (soup.find("meta", property="og:title") or soup.find("title")).get("content", soup.title.string if soup.title else "Unknown")
    
    author = "Unknown"
    author_tag = soup.find("meta", attrs={"property": "article:author"}) or soup.find("meta", attrs={"name": "author"}) or soup.find("meta", attrs={"property": "og:site_name"})
    if author_tag:
        author = author_tag.get("content", "Unknown")
    
    date = "Unknown"
    date_tag = soup.find("meta", attrs={"property": "article:published_time"}) or soup.find("meta", attrs={"name": "pubdate"}) or soup.find("meta", attrs={"property": "og:updated_time"})
    if date_tag:
        date = date_tag.get("content", "Unknown")[:10]

    # Content extraction
    # Try common article containers first
    article = soup.find("article") or soup.find("main") or soup.find("div", class_="content") or soup.find("div", id="content")
    
    if article:
        content_source = article
    else:
        content_source = soup

    # Extract paragraphs and filter out short/irrelevant ones
    paragraphs = []
    for p in content_source.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 60:  # Higher threshold for quality
            paragraphs.append(text)

    # Fallback if no paragraphs found in article
    if not paragraphs:
        # Just grab anything with decent text length in divs
        for div in soup.find_all("div"):
            text = div.get_text(strip=True)
            if len(text) > 200 and len(div.find_all("p")) == 0: # Direct text in div
                paragraphs.append(text[:500]) # Cap it to avoid huge noise
                break

    return {
        "title": title,
        "author": author,
        "published_date": date,
        "content_chunks": paragraphs
    }