import requests
import re
from bs4 import BeautifulSoup

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    TRANSCRIPT_AVAILABLE = True
except ImportError:
    TRANSCRIPT_AVAILABLE = False

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def scrape_youtube(url):
    """Scrape a YouTube video and return structured data."""
    video_id = _extract_video_id(url)
    if not video_id:
        print(f"[YouTube] Could not extract video ID from {url}")
        return _empty_youtube(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"[YouTube] Failed to fetch page {url}: {e}")
        return _empty_youtube(url)

    title       = _extract_title(soup)
    channel     = _extract_channel(soup)
    description = _extract_description(soup)
    date        = _extract_date(soup)
    chunks, has_transcript = _extract_transcript(video_id, description)

    return {
        "title": title,
        "author": channel,
        "published_date": date,
        "domain": "youtube.com",
        "has_medical_disclaimer": _has_medical_disclaimer(description),
        "has_transcript": has_transcript,
        "content_chunks": chunks
    }

# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_video_id(url):
    patterns = [
        r"v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"embed/([^?]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def _extract_title(soup):
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    return "Unknown"

def _extract_channel(soup):
    # Try link itemprop
    link = soup.find("link", itemprop="name")
    if link and link.get("content"):
        return link["content"].strip()
    # Try meta
    tag = soup.find("meta", itemprop="channelId")
    if tag:
        owner = soup.find("span", itemprop="author")
        if owner:
            return owner.get_text(strip=True)
    return "Unknown"

def _extract_description(soup):
    og = soup.find("meta", property="og:description")
    if og and og.get("content"):
        return og["content"].strip()
    return ""

def _extract_date(soup):
    tag = soup.find("meta", itemprop="datePublished")
    if tag and tag.get("content"):
        return tag["content"][:10]
    tag = soup.find("meta", {"name": "upload_date"})
    if tag and tag.get("content"):
        return tag["content"][:10]
    return "Unknown"

def _extract_transcript(video_id, description_fallback):
    """Returns (chunks, has_transcript)."""
    if not TRANSCRIPT_AVAILABLE:
        return _chunk_text(description_fallback, chunk_size=5), False

    try:
        # Version 1.2.4+ requires instantiating the API class
        api     = YouTubeTranscriptApi()
        fetched = api.fetch(video_id)
        entries = fetched.to_raw_data()
        texts   = [e["text"] for e in entries]
        # Group every 8 lines into one chunk
        chunks = [" ".join(texts[i:i+8]) for i in range(0, len(texts), 8)]
        return chunks, True
    except Exception as e:
        print(f"[YouTube] Transcript unavailable for {video_id}: {e}")
        # Fallback: use description
        return [description_fallback] if description_fallback else ["Transcript unavailable."], False

def _chunk_text(text, chunk_size=5):
    sentences = text.split(". ")
    return [". ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]

def _has_medical_disclaimer(text):
    keywords = ["not medical advice", "consult a doctor", "consult your physician",
                "for informational purposes", "medical disclaimer", "seek professional"]
    return any(kw in text.lower() for kw in keywords)

def _empty_youtube(url):
    return {
        "title": "Unknown", "author": "Unknown",
        "published_date": "Unknown", "domain": "youtube.com",
        "has_medical_disclaimer": False, "has_transcript": False,
        "content_chunks": []
    }
