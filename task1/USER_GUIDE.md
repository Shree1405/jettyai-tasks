# 📖 Task 1: User Guide

Welcome to the User Guide for the Task 1 Multi-Source Scraper. This document will help you get the system up and running and understand the data it produces.

---

## 🎯 Purpose
The Task 1 scraper is a robust prototype designed to collect medical and health-related content from:
- **Blogs**: Generic health and medical blog posts.
- **YouTube**: Video transcripts and descriptions.
- **PubMed**: Medical research abstracts.

## 🛠 Prerequisites
- **Python 3.12+**
- **Pip** (Python package manager)

## 🚀 Getting Started

### 1. Installation
Install the necessary libraries using the following command:
```bash
pip install requests beautifulsoup4 youtube-transcript-api langdetect keybert httpx fake-useragent
```

### 2. Configuration
The URLs to be scraped are defined in `main.py`. You can modify the `blog_urls`, `youtube_urls`, and `pubmed_url` variables to target specific content.

### 3. Running the Scraper
Execute the main script from your terminal:
```bash
python main.py
```

## 📊 Understanding the Results
After the script completes, you will find a `scraped_data/` directory containing:
- `blogs.json`: Content and scores for the blog URLs.
- `youtube.json`: Transcripts and metadata for the videos.
- `pubmed.json`: Extracted research data.

### JSON Schema Highlights
- **`trust_score`**: A value from 0 to 100 indicating the source's credibility.
- **`topic_tags`**: Key phrases identified by the AI.
- **`content_chunks`**: The raw text extracted from the source.

## ⚠️ Troubleshooting
- **Missing Transcripts**: If a YouTube video has transcripts disabled, the scraper will use the video description instead.
- **Bot Detection**: Some sites (like Healthline) may block automated requests. The system uses header rotation to minimize this, but you may see "Unknown" fields if a scrape fails.
- **Model Download**: On the first run, the system will download the KeyBERT AI model (~500MB). This may take a few minutes depending on your connection.
