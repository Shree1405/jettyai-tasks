# 🕵️‍♂️ Task 2: Advanced Scrapers

While the sources (Blogs, YouTube, PubMed) are the same as Task 1, the Task 2 implementations are more robust and return deeper metadata.

---

## 🛠 Features common to all Scrapers
- **Schema Mapping**: All scrapers return a dictionary with keys: `author`, `published_date`, `domain`, `content_chunks`, `has_medical_disclaimer`.
- **Error Transparency**: If a field cannot be found, it returns `None` or `"Unknown"`, allowing the Scoring Engine to handle it gracefully rather than crashing.

## 🎥 YouTube Scraper
- **Enhanced Transcripts**: Performs pre-processing on transcripts to remove timestamp metadata and speaker identifiers, creating a "clean" text block for chunking.
- **Thumbnail/Region Support**: Architecture is ready for additional video metadata (thumbnails, region codes) which were not supported in Task 1.

## 🔬 PubMed Scraper
- **Cleaned Abstracts**: Specifically handles "Labelled Abstracts" (e.g., BACKGROUND:, METHODS:) to ensure they are treated as separate logical paragraphs during chunking.
- **Domain Identity**: Explicitly returns `pubmed.ncbi.nlm.nih.gov` as the domain to trigger the highest baseline authority score.

## 🛡 Network Management
- **Centralized Logic**: Future versions can move header rotation and proxy management into a shared `utils/network.py`, a change that is much easier in this modular structure than in Task 1.
