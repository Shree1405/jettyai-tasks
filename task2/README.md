# Medical Content Scraper & Trust Scoring System

## Project Structure

```
project/
├── main.py                    ← Entry point, run this
├── scraper/
│   ├── blog_scraper.py        ← Scrapes blog posts
│   ├── youtube_scraper.py     ← Scrapes YouTube videos + transcripts
│   └── pubmed_scraper.py      ← Scrapes PubMed articles
├── scoring/
│   └── trust_score.py         ← Trust scoring algorithm (0.0 – 1.0)
├── utils/
│   ├── tagging.py             ← Auto topic tag generation
│   └── chunking.py            ← Content chunking logic
└── output/
    ├── blogs.json
    ├── youtube.json
    ├── pubmed.json
    └── scraped_data.json      ← All 6 sources combined
```

---

## Tools & Libraries

| Library | Version | Purpose |
|---|---|---|
| `requests` | latest | HTTP requests to fetch web pages |
| `beautifulsoup4` | latest | HTML parsing and content extraction |
| `youtube-transcript-api` | latest | Fetch YouTube video transcripts |
| `langdetect` | latest | Automatic language detection |
| `keybert` | latest | Semantic topic tag generation |

---

## Installation

```bash
pip install requests beautifulsoup4 youtube-transcript-api langdetect keybert
```

---

## How to Run

```bash
cd project
python main.py
```

Output files will appear in the `output/` folder.

---

## Scraping Approach

### Blogs
- Uses `requests` to fetch HTML and `BeautifulSoup` to parse it
- Tries multiple CSS class patterns for author and date extraction
- Filters `<p>` tags longer than 60 characters to remove nav/footer noise
- Detects medical disclaimers by scanning for keywords

### YouTube
- Fetches Open Graph metadata for title, channel, description
- Uses `youtube-transcript-api` to get full auto-generated or human transcript
- Falls back to video description if transcript is unavailable
- Groups transcript lines into 8-line chunks

### PubMed
- Targets PubMed's consistent HTML structure
- Extracts title, all authors (as a list), journal, year, and abstract paragraphs
- Always marks `has_medical_disclaimer = True` since it is peer-reviewed

---

## Trust Score Algorithm

### Formula
```
Trust Score = weighted_sum(
    domain_authority    × 0.30,
    author_credibility  × 0.25,
    recency             × 0.20,
    medical_disclaimer  × 0.15,
    content_richness    × 0.10
) − abuse_penalties
```

### Factor Details

| Factor | How It Is Scored |
|---|---|
| Domain Authority | Curated lookup table (WHO=0.97, PubMed=1.0, unknown=0.30) |
| Author Credibility | Known org → 0.95, Full name → 0.70, Unknown → 0.10 |
| Recency | ≤1 year → 1.0, ≤2 years → 0.8, ≤5 years → 0.6, older → lower |
| Medical Disclaimer | Present → 1.0, Absent → 0.0 (PubMed always 1.0) |
| Content Richness | Based on word count and transcript availability |

### Abuse Prevention

| Threat | Penalty |
|---|---|
| Suspicious author name (admin, editor, staff) | −0.10 |
| Low domain authority (≤0.30) | −0.10 |
| No medical disclaimer on medical content | −0.08 |
| Content older than 10 years | −0.15 |
| Content older than 5 years | −0.07 |

---

## Edge Case Handling

| Edge Case | Handling |
|---|---|
| Missing author | Score = 0.1, flagged in breakdown |
| Missing date | Recency score = 0.2 |
| No transcript (YouTube) | Fallback to description, content score = 0.3 |
| Multiple authors (PubMed) | Average of individual credibility scores |
| Non-English content | Detected via `langdetect`, stored in `language` field |
| Very long articles | Re-chunked to max 150 words per chunk |
| Failed HTTP request | Returns empty record with all fields set to "Unknown" |

---

## Limitations

1. YouTube publish date requires the YouTube Data API v3 for reliable extraction (basic scraping may return "Unknown")
2. `region` field is always "Unknown" — real region detection needs an IP geolocation API
3. Some blog sites use JavaScript rendering (React/Next.js) — `requests` cannot scrape them; Selenium would be needed
4. Domain authority table is manually curated and may need updates
5. KeyBERT model download (~500MB) is required on first run
