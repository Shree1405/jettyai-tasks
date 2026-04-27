# 🛠 Task 1: Technical Developer Guide

This document provides a deep dive into the code architecture and logic of the Task 1 Multi-Source Scraper.

---

## 🏗 Code Architecture
Task 1 follows an **integrated monolithic design** where the main orchestrator (`main.py`) directly interacts with specialized scraper modules.

### File Structure
- `main.py`: The central orchestrator that manages the flow.
- `scrappers/`: Package containing source-specific logic.
- `topic_tagger.py`: Interface for KeyBERT semantic analysis.
- `trust_score.py`: Rule-based credibility calculation.

## 🕵️‍♂️ Scraper Implementation

### Blog Scraper (`scrappers/blog_scraper.py`)
- Uses `requests` for fetching and `BeautifulSoup4` for parsing.
- Implements a generic fallback mechanism to find article content when standard tags are missing.
- Filters out noise (headers, footers, nav) by analyzing DOM structure.

### YouTube Scraper (`scrappers/youtube_scraper.py`)
- Integrates `youtube-transcript-api` to extract raw video transcripts.
- Uses `requests` and regex to pull metadata (Author, Published Date) from the video page HTML.

### PubMed Scraper (`scrappers/pubmed_scrapper.py`)
- Specialized parser for the NCBI structure.
- Focuses on extracting structured author lists and the article abstract.

## ⚖️ Trust Scoring Logic
Task 1 uses a **rule-based additive system** (0-100).

| Feature | Score Weight |
| :--- | :--- |
| **Source Type** | PubMed (+40), YouTube (+20), Blog (+15) |
| **Known Author** | +15 if author name is found |
| **Recency** | +10 if date found, +10 bonus for ≥ 2022 |
| **Richness** | +15 if >500 words, +8 if >200 words |
| **YouTube** | +10 if transcript is available |

## 🏷 AI Topic Tagging
The `topic_tagger.py` module wraps the `KeyBERT` library. It performs a cosine similarity search between the document embedding and potential sub-phrase embeddings to identify the top 5 most descriptive tags.

## 🔧 Extending Task 1
To add a new source:
1. Create a new scraper file in `scrappers/`.
2. Implement a function that returns a dictionary with standard keys (`author`, `content_chunks`, etc.).
3. Update `main.py` to include the new source in the `build_record` pipeline.
