# 🕵️‍♂️ Task 1: Scraper Implementations

Detailed technical breakdown of how Task 1 extracts data from various sources.

---

## 📝 Blog Scraper (`scrappers/blog_scraper.py`)
Designed for flexibility across different CMS (WordPress, Medium, etc.).

- **Parsing Engine**: `BeautifulSoup4` with `lxml` or `html.parser`.
- **Logic**:
    - Scans for common content containers (`article`, `main`, `.post-content`).
    - Extracts `h1` for titles and `meta[name='author']` for creators.
    - Implements a recursive fallback: if no primary container is found, it analyzes paragraph density to find the main text.

## 🎥 YouTube Scraper (`scrappers/youtube_scraper.py`)
Focuses on capturing the "spoken word" content of medical videos.

- **Transcript Fetching**: Uses the `youtube-transcript-api`. If the API fails (e.g., transcripts disabled), it gracefully returns an empty list.
- **Metadata**: Parses the video page using `requests` and regex to extract:
    - Channel Name
    - Upload Date
    - Video Description (used as a content fallback)

## 🔬 PubMed Scraper (`scrappers/pubmed_scrapper.py`)
Optimized for high-fidelity medical data.

- **Strategy**: Specific CSS selectors for the PubMed UI.
- **Data Points**:
    - Article Title
    - Complete Author List
    - Journal Citation String
    - Structured Abstract (Background, Methods, Results, Conclusion)
- **Authority**: PubMed articles are treated as gold-standard sources in the subsequent scoring phase.
