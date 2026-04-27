# 🎯 Task 1: Multi-Source Web Scraper & Trust Scorer

This sub-project implements a flexible web scraping and content analysis system designed to extract structured data from diverse sources including medical journals (PubMed), video platforms (YouTube), and general blog posts.

> [!IMPORTANT]
> **[📖 User Guide](./USER_GUIDE.md)** | **[🛠 Technical Guide](./TECHNICAL_GUIDE.md)**

## ✨ Features

- **Multi-Source Scraping**: Specialized modules for Blogs (recursive fallback), YouTube (transcripts + metadata), and PubMed.
- **AI-Powered Tagging**: Uses `KeyBERT` to automatically extract the most relevant keywords.
- **Trust Scoring Algorithm**: A weighted scoring system (0-100) based on source credibility, authorship, and recency.
- **Robustness**: Header rotation and anti-bot protection using `httpx` and `fake-useragent`.
- **Automated Language Detection**: Uses `langdetect` to identify the content's primary language.

## 🏗 Project Structure

```text
task1/
├── main.py               # Main entry point (orchestrator)
├── scrappers/            # Scraper package
│   ├── blog_scraper.py   # Generic & specialized blog logic
│   ├── youtube_scraper.py# YouTube transcript extraction
│   └── pubmed_scrapper.py# PubMed specific journal scraping
├── topic_tagger.py       # AI Topic generation using KeyBERT
├── trust_score.py        # Logic for Trust Score calculation
└── scraped_data/         # Output directory for JSON results
```

## 🛠 Technical Details

### 1. Scraper Implementations
- **Blog Scraper**: Uses `requests` and `BeautifulSoup4`. Implements fallback logic to extract content even when standard tags are missing.
- **YouTube Scraper**: Utilizes `youtube-transcript-api` for full transcripts and `requests` for metadata (Title, Author, Date).
- **PubMed Scrapper**: Optimized for the NCBI structure, extracting authors, journal info, and abstracts.

### 2. Trust Scoring Rules (0 - 100)
The trust score is calculated based on the following additive rules:
- **Source Type**: PubMed (+40), YouTube (+20), Blog (+15).
- **Author Identity**: Known author present (+15).
- **Recency**: Date present (+10), published in 2022 or later (+10 bonus).
- **Content Richness**: >500 words (+15), >200 words (+8).
- **YouTube Quality**: Transcript available (+10).
- **Advanced Logic**: For a deep dive into the evolution of this algorithm, see the [Trust Scoring Algorithm](../documentation/trust_scoring.md).

## 🚀 Installation & Usage

### Prerequisites
- Python 3.12+
- Pip

### Setup
```bash
pip install youtube-transcript-api requests beautifulsoup4 langdetect keybert httpx fake-useragent
```

### Execution
```bash
python main.py
```
The results will be saved as JSON files in the `scraped_data/` directory.

## 📊 Output Schema

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

## ⚠️ Important Notes

- **Anti-Bot Protection**: Sites like Healthline and PubMed have aggressive protections. This scraper uses `fake-useragent` but may still require proxies for high-volume scraping.
- **YouTube Transcripts**: If transcripts are disabled by the creator, the scraper will fall back to the video description.
- **KeyBERT Models**: On first run, ~500MB of transformer models will be downloaded.

