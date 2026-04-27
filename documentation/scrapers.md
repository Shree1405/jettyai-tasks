# 🕵️‍♂️ Scraper Logic & Implementation

This document details the technical implementation of the scrapers used in JettyAI Tasks, focusing on the robust extraction techniques for Blogs, YouTube, and PubMed.

---

## 📝 Blog Scraper

The Blog Scraper is designed to be highly adaptive, as blog structures vary significantly across the web.

### Extraction Strategy
1. **Metadata**:
   - Priority: Open Graph tags (`og:title`, `og:author`).
   - Fallback: Standard meta tags, H1 tags, and specific CSS class lookups (e.g., `.author`, `.byline`).
2. **Content Container Detection**:
   - The scraper attempts to find the "main" content by searching for `<article>`, `<main>`, or classes containing "content".
   - It decomposes noise elements like `<script>`, `<style>`, `<nav>`, and `<ads>` before extraction.
3. **Medical Disclaimer Detection**:
   - Performs a case-insensitive keyword search for phrases like "medically reviewed", "not medical advice", or "consult a doctor".

### Resilience Features
- **Header Rotation**: Uses a realistic `User-Agent` to avoid immediate bot detection.
- **Noise Filtering**: Automatically skips short text blocks (<60 characters) to avoid including navigation links or image captions in the main content.

---

## 🎥 YouTube Scraper

Extraction from YouTube focuses on two primary data points: video metadata and the spoken transcript.

### Metadata Extraction
- Extracted via `requests` from the HTML source.
- Uses Open Graph tags for Title and Description.
- Extracts the published date from the `itemprop="datePublished"` or `schema.org` tags.

### Transcript Logic
- **Primary**: Uses `youtube-transcript-api` to fetch the auto-generated or manually uploaded transcript.
- **Secondary (Fallback)**: If transcripts are disabled or unavailable, it falls back to the video description.
- **Formatting**: Transcripts are cleaned and formatted into consistent text blocks for chunking.

---

## 🔬 PubMed Scraper

The PubMed scraper is specialized for the NCBI (National Center for Biotechnology Information) structure.

### Features
- **Author Extraction**: Specifically handles multiple authors and affiliations.
- **Journal Metadata**: Extracts the journal name, volume, and publication year.
- **Abstract Parsing**: Targets the structured abstract sections commonly found in medical papers.
- **Authority**: Content from PubMed is automatically granted a "Domain Authority" of 1.0.

---

## 🛡 Anti-Bot & Throttling
- **Polite Scraping**: A 1-second delay is implemented between requests in `main.py`.
- **Timeout Management**: All requests have a 15-second timeout to prevent the pipeline from hanging on unresponsive servers.
- **Status Checking**: Implements `response.raise_for_status()` to ensure partial or error pages aren't processed as valid data.
