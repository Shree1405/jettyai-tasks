"""
main.py
=======
Entry point for the multi-source medical content scraping pipeline.
Scrapes blogs, YouTube videos, and a PubMed article,
then calculates trust scores and saves structured JSON output.

Run:
    python main.py
"""

import json
import os
import time
import sys

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from scraper.blog_scraper    import scrape_blog
from scraper.youtube_scraper import scrape_youtube
from scraper.pubmed_scraper  import scrape_pubmed
from scoring.trust_score     import calculate_trust_score
from utils.tagging           import generate_tags
from utils.chunking          import chunk_paragraphs

try:
    from langdetect import detect as detect_language
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

# ── URLs ──────────────────────────────────────────────────────────────────────

BLOG_URLS = [
    "https://www.who.int/news-room/spotlight/ten-threats-to-global-health-in-2019",
    "https://www.healthline.com/health/diabetes/type-1-diabetes-vs-type-2-diabetes",
    "https://www.medicalnewstoday.com/articles/ai-in-healthcare"
]

YOUTUBE_URLS = [
    "https://www.youtube.com/watch?v=DMLDF9MQGPM",   # Osmosis - Diabetes
    "https://www.youtube.com/watch?v=3JZ_D3ELwOQ"    # AI in healthcare
]

PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/37283936/"

# ── Pipeline ──────────────────────────────────────────────────────────────────

def detect_lang(text):
    if not LANGDETECT_AVAILABLE or not text or len(text.strip()) < 20:
        return "en"
    try:
        return detect_language(text)
    except Exception:
        return "unknown"


def build_record(url, source_type, scraped):
    """Convert raw scraped data into the final JSON schema."""

    # Rechunk paragraphs to consistent size
    chunks = chunk_paragraphs(scraped.get("content_chunks", []), max_words=150)

    # Full text for tagging and language detection
    full_text = " ".join(chunks)

    # Language detection
    language = detect_lang(full_text)

    # Topic tags
    tags = generate_tags(full_text)

    # Author — normalize to string for trust scoring
    author_raw = scraped.get("author", "Unknown")
    if isinstance(author_raw, list):
        author_str = ", ".join(author_raw) if author_raw else "Unknown"
    else:
        author_str = author_raw or "Unknown"

    # Trust score
    trust_result = calculate_trust_score(
        source_type         = source_type,
        author              = scraped.get("author", "Unknown"),   # pass original (list ok)
        published_date      = scraped.get("published_date", "Unknown"),
        domain              = scraped.get("domain", "unknown.com"),
        content_chunks      = chunks,
        has_medical_disclaimer = scraped.get("has_medical_disclaimer", False),
        has_transcript      = scraped.get("has_transcript", False)
    )

    return {
        "source_url":    url,
        "source_type":   source_type,
        "author":        author_str,
        "published_date": scraped.get("published_date", "Unknown"),
        "language":      language,
        "region":        "Unknown",   # requires IP geolocation API
        "topic_tags":    tags,
        "trust_score":   trust_result["score"],
        "trust_breakdown": trust_result["breakdown"],
        "penalty_applied": trust_result["penalty_applied"],
        "penalty_reasons": trust_result["penalty_reasons"],
        "content_chunks": chunks
    }


def save_json(data, filename):
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved → {path}")


def print_summary(record):
    print(f"    Author      : {record['author']}")
    print(f"    Date        : {record['published_date']}")
    print(f"    Language    : {record['language']}")
    print(f"    Tags        : {record['topic_tags']}")
    print(f"    Trust Score : {record['trust_score']} / 1.0")
    print(f"    Chunks      : {len(record['content_chunks'])}")
    if record["penalty_reasons"]:
        for r in record["penalty_reasons"]:
            print(f"    ⚠ {r}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  Medical Content Scraping & Trust Scoring Pipeline")
    print("="*60)

    all_records = []

    # ── Blogs ──
    print("\n[1/3] Scraping Blogs...")
    blog_records = []
    for i, url in enumerate(BLOG_URLS, 1):
        print(f"\n  Blog {i}: {url}")
        scraped = scrape_blog(url)
        record  = build_record(url, "blog", scraped)
        blog_records.append(record)
        all_records.append(record)
        print_summary(record)
        time.sleep(1)   # polite delay

    save_json(blog_records, "blogs.json")

    # ── YouTube ──
    print("\n[2/3] Scraping YouTube Videos...")
    youtube_records = []
    for i, url in enumerate(YOUTUBE_URLS, 1):
        print(f"\n  YouTube {i}: {url}")
        scraped = scrape_youtube(url)
        record  = build_record(url, "youtube", scraped)
        youtube_records.append(record)
        all_records.append(record)
        print_summary(record)
        time.sleep(1)

    save_json(youtube_records, "youtube.json")

    # ── PubMed ──
    print("\n[3/3] Scraping PubMed Article...")
    print(f"\n  PubMed: {PUBMED_URL}")
    scraped = scrape_pubmed(PUBMED_URL)
    record  = build_record(PUBMED_URL, "pubmed", scraped)
    pubmed_records = [record]
    all_records.append(record)
    print_summary(record)

    save_json(pubmed_records, "pubmed.json")

    # ── Combined ──
    save_json(all_records, "scraped_data.json")

    print("\n" + "="*60)
    print("  DONE! All files saved to output/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
