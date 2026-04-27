# Multi-Source Web Scraper & Trust Scorer

This project is a flexible web scraping and content analysis system designed to extract structured data from diverse sources including medical journals (PubMed), video platforms (YouTube), and general blog posts. It automatically detects language, generates AI-powered topic tags, and calculates a content "Trust Score."

## Features

- **Multi-Source Scraping**: Specialized modules for Blogs (recursive fallback), YouTube (transcripts + metadata), and PubMed (specialized headers).
- **AI-Powered Tagging**: Uses `KeyBERT` to automatically extract the most relevant keywords from the content.
- **Trust Scoring Algorithm**: A weighted scoring system (0-100) based on source credibility, authorship, recency, and content richness.
- **Robustness**: 
    - Automatic User-Agent rotation using `fake-useragent`.
    - Handles anti-bot protections using `httpx`.
    - Prioritizes Open Graph and Metadata tags for high-accuracy extraction.
- **Structured Storage**: Outputs data in clean, ready-to-use JSON format.

## 🛠️ Project Structure

```text
task1/
├── main.py               # Main entry point (orchestrator)
├── scrappers/            # Scraper package
│   ├── __init__.py
│   ├── blog_scraper.py   # Generic & specialized blog scraping logic
│   ├── youtube_scraper.py# YouTube transcript & info extraction
│   └── pubmed_scrapper.py# PubMed specific journal scraping
├── topic_tagger.py       # AI Topic generation using KeyBERT
├── trust_score.py        # Logic for calculating the Trust Score
└── scraped_data/         # Output directory for JSON results
```

## Prerequisites

- **Python 3.12+** (Tested on 3.14)
- Pip

##  Installation

1. Clone the repository and navigate to the project folder.
2. Install the required dependencies:

```bash
pip install youtube-transcript-api requests beautifulsoup4 langdetect keybert httpx fake-useragent
```

## Usage

Run the main script to start the scraping process:

```bash
python main.py
```

The script will process the URLs defined in `main.py` and save the results to the `scraped_data/` folder.

## Output Schema

Each entry in the output JSON files follows this schema:

```json
{
  "source_url": "URL of the content",
  "source_type": "blog | youtube | pubmed",
  "author": "Name of author or channel",
  "published_date": "YYYY-MM-DD",
  "language": "ISO language code",
  "topic_tags": ["tag1", "tag2"],
  "trust_score": 85,
  "content_chunks": ["chunk1...", "chunk2..."]
}
```

##  Important Notes

- **PubMed & Healthline**: These sites have aggressive anti-bot protections. If you encounter `403 Forbidden` errors, consider using a residential proxy or a headless browser solution like Playwright.
- **YouTube Transcripts**: Transcripts must be enabled by the uploader to be extracted. If disabled, the scraper falls back to the video description.
- **HF HUB Warning**: When running for the first time, `KeyBERT` will download its transformer models. You may see a warning about `HF_TOKEN`; this can be ignored unless you require higher rate limits.
