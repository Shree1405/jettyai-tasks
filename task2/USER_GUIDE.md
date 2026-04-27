# 📖 Task 2: User Guide

Welcome to the User Guide for the Task 2 Medical Content Scraper. Task 2 is the advanced, modular version of the pipeline, featuring enhanced scoring and data processing.

---

## 🏗 System Overview
Task 2 is built for scalability. It separates the scraping logic from the processing and scoring layers, allowing for a more professional and maintainable data pipeline.

## 🚀 Getting Started

### 1. Installation
Install the required dependencies:
```bash
pip install requests beautifulsoup4 youtube-transcript-api langdetect keybert
```

### 2. Configuration
URLs are managed in `main.py` under the `BLOG_URLS`, `YOUTUBE_URLS`, and `PUBMED_URL` constants. You can also adjust the `time.sleep(1)` delay if you need to scrape more or less aggressively.

### 3. Execution
Run the orchestrator:
```bash
python main.py
```

## 📊 Analyzing the Output
Task 2 generates detailed JSON records in the `output/` directory.

### Enhanced Trust Score (0.0 - 1.0)
Unlike Task 1, this version provides a **normalized score** and a **detailed breakdown**:
- `trust_score`: The final calculated credibility.
- `trust_breakdown`: Scores for each factor (Domain, Author, Recency, etc.).
- `penalty_reasons`: If the score was lowered, this list explains why (e.g., "Outdated content").

### Content Chunking
The output text is split into `content_chunks` of approximately 150 words. This makes the data ready for use in AI applications like Chatbots or Knowledge Bases.

## ⚠️ Important Notes
- **Language Detection**: The system automatically detects the language of the content.
- **Medical Disclaimers**: Task 2 actively searches for safety warnings, which contributes significantly to the trust score.
- **NCBI Reliability**: PubMed articles are always given the highest trust weighting.
