# 🏥 Task 2: Medical Content Scraper & Trust Scoring System

This sub-project represents a modularized and improved version of the medical content scraping pipeline. It features a decoupled architecture for better scalability, maintenance, and advanced scoring logic.

> [!IMPORTANT]
> **[📖 User Guide](./USER_GUIDE.md)** | **[🛠 Technical Guide](./TECHNICAL_GUIDE.md)**

## 🏗 Modular Architecture

The project is split into four logical layers to ensure clean separation of concerns:

- **`scraper/`**: Specialized modules for fetching raw data.
- **`scoring/`**: Core logic for evaluating content trustworthiness.
- **`utils/`**: Shared services for semantic tagging and content chunking.
- **`main.py`**: Orchestration layer that builds the final records.

```text
task2/
├── main.py                    ← Pipeline Orchestrator
├── scraper/
│   ├── blog_scraper.py        ← Generic/Specialized Blog Logic
│   ├── youtube_scraper.py     ← YouTube Metadata & Transcripts
│   └── pubmed_scraper.py      ← PubMed (NCBI) Article Extraction
├── scoring/
│   └── trust_score.py         ← Weighted Scoring & Abuse Penalties
├── utils/
│   ├── tagging.py             ← KeyBERT Semantic Tagging
│   └── chunking.py            ← Paragraph-to-Chunk Logic
└── output/                    ← Final JSON Records
```

> [!TIP]
> For a detailed explanation of this architecture and component interactions, see [System Architecture](../documentation/architecture.md) and [API Reference](../documentation/api_reference.md).

## 🛠 Advanced Trust Scoring

The Trust Score (0.0 – 1.0) is a weighted sum of five key factors, adjusted by automated abuse penalties.

### 1. Weighted Factors (Sum = 1.0)
| Factor | Weight | Scoring Logic |
| :--- | :--- | :--- |
| **Domain Authority** | 30% | Curated lookup (e.g., PubMed=1.0, WHO=0.97). |
| **Author Credibility**| 25% | Recognized organizations (0.95), Full Name (0.70). |
| **Recency** | 20% | ≤1yr (1.0), ≤2yrs (0.8), ≤5yrs (0.6), >10yrs (0.2). |
| **Medical Disclaimer**| 15% | Present (1.0), Absent (0.0). PubMed always 1.0. |
| **Content Richness** | 10% | Word count thresholds (>1000 words = 1.0). |

### 2. Domain Authority (Partial List)
| Domain | Score | Domain | Score |
| :--- | :--- | :--- | :--- |
| pubmed.ncbi.nlm.nih.gov | 1.00 | who.int | 0.97 |
| cdc.gov | 0.96 | nih.gov | 0.95 |
| healthline.com | 0.80 | youtube.com | 0.65 |
| medium.com | 0.50 | unknown.com | 0.30 |

### 3. Abuse Prevention Penalties
| Scenario | Penalty | Reason |
| :--- | :--- | :--- |
| **Suspicious Author** | -0.10 | Use of "admin", "staff", "webmaster". |
| **Low Authority** | -0.10 | Domain score ≤ 0.30 (Potential SEO spam). |
| **Missing Disclaimer**| -0.08 | Required for medical content on Blogs/YouTube. |
| **Outdated Content** | -0.15 | Content older than 10 years. |

## 🚀 Getting Started

### Installation
```bash
pip install requests beautifulsoup4 youtube-transcript-api langdetect keybert
```

### Execution
```bash
python main.py
```

## 📊 Technical Features

- **Semantic Chunking**: Content is split into chunks of ~150 words using `utils/chunking.py`, preserving paragraph integrity where possible.
- **Dynamic Tagging**: Uses `KeyBERT` in `utils/tagging.py` to extract topics without a fixed taxonomy.
- **Error Resilience**: Failed scrapes return a partial record with "Unknown" values rather than crashing the pipeline.
- **Language Detection**: Automatically skips tagging for extremely short or non-detectable content.

## ⚠️ Limitations & Edge Cases
- **JavaScript Rendering**: Currently relies on `requests`. Sites using heavy client-side rendering (React/Next.js) may return partial content.
- **YouTube Metadata**: Publish dates are extracted from Open Graph tags, which may be less reliable than the official Data API.
- **Geographic Data**: The `region` field is currently "Unknown" and requires integration with a GeoIP service.

