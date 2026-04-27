# 🏗 Task 2: Modular Architecture

Task 2 implements a **Layered Architecture** to ensure that each component can be developed and tested in isolation.

---

## 🗺 System Layers

### 1. Scraper Layer (`scraper/`)
Atomic modules that focus exclusively on raw data retrieval.
- `blog_scraper.py`
- `youtube_scraper.py`
- `pubmed_scraper.py`
*Each module returns a standard "Raw Scraped" dictionary.*

### 2. Utils Layer (`utils/`)
Shared processing services used by all scrapers and the main orchestrator.
- **`chunking.py`**: Handles paragraph grouping and word-count normalization.
- **`tagging.py`**: Encapsulates KeyBERT keyword extraction.

### 3. Scoring Layer (`scoring/`)
The mathematical core of the system.
- **`trust_score.py`**: Implements the weighted scoring formula and the penalty engine.

### 4. Orchestration Layer (`main.py`)
Responsible for "piping" data between layers.
- Handles initialization.
- Maps URLs to scrapers.
- Passes scraped content to the `build_record` pipeline.
- Aggregates final JSON results.

---

## 📈 Component Interactions
1. `main.py` calls `scraper.scrape_...()`
2. Raw data flows to `utils.chunk_paragraphs()`
3. Chunked text flows to `utils.generate_tags()`
4. Metadata and content flow to `scoring.calculate_trust_score()`
5. Integrated record is saved to `output/`
