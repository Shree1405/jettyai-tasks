# 🛠 Task 2: Technical Developer Guide

This document details the modular architecture and advanced algorithms implemented in Task 2.

---

## 🏛 Modular Architecture
Task 2 is organized into four distinct layers:

1. **Scraper Layer (`scraper/`)**: Atomic modules for fetching raw data from specific sources.
2. **Utils Layer (`utils/`)**: Shared processing services for tagging and chunking.
3. **Scoring Layer (`scoring/`)**: Complex logic for trust evaluation and abuse prevention.
4. **Orchestration Layer (`main.py`)**: Assembles the components into a unified pipeline.

## ⚖️ Advanced Trust Scoring Algorithm
The scoring logic in `scoring/trust_score.py` uses a weighted multi-factor formula.

### Weighted Factors (100% Total)
- **Domain Authority (30%)**: Verified via a curated lookup table of 25+ medical domains.
- **Author Credibility (25%)**: Recognition of medical organizations and credentials.
- **Recency (20%)**: Dynamic age-based scoring with a 10-year lookback.
- **Medical Disclaimer (15%)**: Automated detection of safety warnings.
- **Content Richness (10%)**: Word count and transcript depth.

### Abuse Prevention Penalties
The algorithm applies specific deductions for suspicious signals:
- **Fake Authors**: -0.10 for "admin", "webmaster", etc.
- **SEO Spam**: -0.10 for domains with low baseline authority.
- **Outdated Content**: Up to -0.15 for content older than 10 years.

## ⚙️ Processing Pipeline

### Semantic Chunking (`utils/chunking.py`)
Groups raw paragraphs into ~150-word chunks while preserving paragraph integrity. This is critical for maintaining context in downstream LLM/RAG applications.

### Dynamic Tagging (`utils/tagging.py`)
Utilizes KeyBERT to extract the top 5 semantic tags from the full text. It includes error handling to skip tagging for very short or non-detectable content.

## 🔧 Extending the Modular System
To add a new data source:
1. Create a new module in `scraper/`.
2. Implement a `scrape_...` function that returns a dictionary matching the schema expected by `main.py:build_record`.
3. Add the new domain to the `DOMAIN_AUTHORITY` table in `scoring/trust_score.py` if necessary.
4. Update `main.py` to include the new scraper in the loop.
