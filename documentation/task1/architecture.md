# 🏗 Task 1: System Architecture

Task 1 follows a **Monolithic Orchestration** pattern. The system is designed for simplicity and direct execution.

---

## 🗺 Component Map

### 1. The Orchestrator (`main.py`)
The "brain" of the system. It:
- Defines the target URLs.
- Iterates through sources.
- Calls the appropriate scraper modules.
- Coordinates the tagging and scoring post-processing.
- Handles file I/O.

### 2. The Scraper Package (`scrappers/`)
Contains specialized modules for different web environments:
- **`blog_scraper.py`**: Handles HTML parsing for general articles.
- **`youtube_scraper.py`**: Manages transcript fetching and video metadata.
- **`pubmed_scrapper.py`**: Specialized for the NCBI journal structure.

### 3. Enrichment Modules
- **`topic_tagger.py`**: Integrates with the `KeyBERT` library to perform semantic keyword extraction.
- **`trust_score.py`**: Implements a rule-based additive scoring algorithm.

---

## 🔄 Data Flow
1. **Input**: A list of URLs categorized by type.
2. **Scrape**: Raw HTML/JSON/Transcript data is fetched.
3. **Clean**: Content is extracted and noise (ads/nav) is removed.
4. **Enrich**: Tags are generated and Trust Scores are calculated.
5. **Persist**: A structured JSON object is written to disk.
