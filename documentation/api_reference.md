# 📚 API Reference (Task 2)

This document provides a reference for the core functions in the Task 2 modular pipeline.

---

## 🏗 Scraper Module (`scraper/`)

### `scrape_blog(url: str) -> dict`
Fetches and parses a blog post.
- **Returns**: A dictionary containing `title`, `author`, `published_date`, `domain`, `has_medical_disclaimer`, and `content_chunks`.

### `scrape_youtube(url: str) -> dict`
Fetches YouTube metadata and transcript.
- **Returns**: A dictionary containing metadata and a list of transcript lines in `content_chunks`.

### `scrape_pubmed(url: str) -> dict`
Fetches a PubMed article abstract and metadata.
- **Returns**: A dictionary with structured NCBI data.

---

## ⚖️ Scoring Module (`scoring/`)

### `calculate_trust_score(...) -> dict`
The primary function for trust evaluation.
- **Parameters**:
    - `source_type`: "blog", "youtube", or "pubmed"
    - `author`: Name string or list of authors.
    - `published_date`: Date string.
    - `domain`: Website domain string.
    - `content_chunks`: List of text strings.
    - `has_medical_disclaimer`: Boolean.
    - `has_transcript`: Boolean (YouTube only).
- **Returns**:
    ```json
    {
      "score": 0.85,
      "breakdown": { ... },
      "penalty_applied": 0.10,
      "penalty_reasons": [ ... ]
    }
    ```

---

## 🛠 Utils Module (`utils/`)

### `generate_tags(text: str) -> list`
Extracts semantic tags using KeyBERT.
- **Returns**: List of top 5 keywords.

### `chunk_paragraphs(paragraphs: list, max_words: int = 150) -> list`
Groups small text blocks into larger chunks.
- **Parameters**:
    - `paragraphs`: List of raw strings.
    - `max_words`: Target word count per chunk.
- **Returns**: List of normalized text chunks.
