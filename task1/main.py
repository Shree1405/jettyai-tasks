import json
import os
from langdetect import detect
from scrappers.blog_scraper import scrape_blog
from scrappers.youtube_scraper import scrape_youtube
from scrappers.pubmed_scrapper import scrape_pubmed
from topic_tagger import generate_tags
from trust_score import calculate_trust_score

def build_record(url, source_type, scraped):
    full_text = " ".join(scraped["content_chunks"])

    try:
        language = detect(full_text)
    except:
        language = "unknown"

    tags = generate_tags(full_text)

    has_transcript = source_type == "youtube" and len(scraped["content_chunks"]) > 1
    trust = calculate_trust_score(
        source_type,
        scraped.get("author", "Unknown"),
        scraped.get("published_date", "Unknown"),
        scraped["content_chunks"],
        has_transcript
    )

    return {
        "source_url": url,
        "source_type": source_type,
        "author": scraped.get("author", "Unknown"),
        "published_date": scraped.get("published_date", "Unknown"),
        "language": language,
        "region": "Unknown",       # Needs IP geolocation API for real region
        "topic_tags": tags,
        "trust_score": trust,
        "content_chunks": scraped["content_chunks"]
    }

def save_json(data_list, filename):
    os.makedirs("scraped_data", exist_ok=True)
    with open(f"scraped_data/{filename}", "w") as f:
        json.dump(data_list, f, indent=2)

# --- Run Everything ---
blog_urls = [
    "https://www.who.int/news-room/spotlight/ten-threats-to-global-health-in-2019",
    "https://www.healthline.com/health/diabetes/type-1-vs-type-2-diabetes",
    "https://www.medicalnewstoday.com/articles/artificial-intelligence-in-healthcare"
]

youtube_urls = [
    "https://youtu.be/xyQY8a-ng6g?si=KcnqrrZMZcqCrpLI",
    "https://youtu.be/yQ6VOOd73MA?si=sE7-TXN24hncbCT8"
]

pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/37283936/"

blogs_data = [build_record(u, "blog", scrape_blog(u)) for u in blog_urls]
youtube_data = [build_record(u, "youtube", scrape_youtube(u)) for u in youtube_urls]
pubmed_data = [build_record(pubmed_url, "pubmed", scrape_pubmed(pubmed_url))]

save_json(blogs_data, "blogs.json")
save_json(youtube_data, "youtube.json")
save_json(pubmed_data, "pubmed.json")

print("Done! Check scraped_data/ folder.")