# 🚀 JettyAI Tasks: Web Scraping & Trust Scoring Suite

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Activity](https://img.shields.io/badge/status-active-brightgreen)

A professional suite of scrapers designed to extract, analyze, and score medical and health-related content from disparate sources including Blogs, YouTube, and PubMed. This project demonstrates advanced data extraction techniques, semantic analysis, and automated trust evaluation.

---

## 📖 Overview

JettyAI Tasks is a collection of tools aimed at automating the collection of high-quality medical data. It doesn't just scrape text; it performs semantic analysis to generate topic tags and applies a weighted scoring algorithm to determine the **Trust Score** of the source.

### Project Goals
- **Automated Extraction**: Scrape deep content from JavaScript-heavy blogs and transcript-rich platforms.
- **AI Classification**: Utilize `KeyBERT` and NLP to automatically categorize content.
- **Quality Assurance**: Implement trust scoring based on domain authority, recency, and author credibility.
- **Scalable Architecture**: Transition from unified scripts to modular, decoupled components.

---

## 🏗 Repository Structure

This repository is organized into two primary work packages, reflecting an evolution from a prototype to a production-ready modular system.

| Component | Focus | Key Features |
| :--- | :--- | :--- |
| **[Task 1: Integrated Scraper](./task1)** | **Prototyping** | Unified `scrappers/` package, direct orchestration, simplified scoring. |
| **[Task 2: Modular Architecture](./task2)** | **Production Grade** | Decoupled layers (`scraper/`, `scoring/`, `utils/`), advanced abuse penalties, detailed breakdown. |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.12+ installed.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Shree1405/jettyai-tasks.git
cd jettyai-tasks

# Install unified dependencies
pip install requests beautifulsoup4 youtube-transcript-api langdetect keybert httpx fake-useragent
```

---

## 📁 Deep Dive: Tasks

### [Task 1: Multi-Source Web Scraper](./task1)
The initial implementation focusing on rapid data collection.
- **Scraper Logic**: Unified `scrappers/` package targeting Blog, YouTube, and PubMed.
- **Scoring**: A rule-based system (0-100) focused on source type, author presence, and basic recency.
- **Output**: Direct JSON generation into `scraped_data/`.

### [Task 2: Medical Content Scoring System](./task2)
A refined, modular version with improved logic and scalability.
- **Architecture**: Separates scraping from processing and scoring.
- **Advanced Algorithm**: Trust Score (0.0 - 1.0) with weighted factors:
  - **Domain Authority (30%)**: Curated lookup of 25+ medical/health domains.
  - **Author Credibility (25%)**: Recognition of medical organizations and credentials.
  - **Recency (20%)**: Dynamic age-based scoring with 10-year lookback.
  - **Medical Disclaimer (15%)**: Automatic detection of safety warnings.
  - **Content Richness (10%)**: Word count and transcript depth evaluation.
- **Abuse Prevention**: Built-in penalties for suspicious authors, SEO spam, and outdated content.

---

---

## 📚 Detailed Documentation

For a deeper dive into the technical implementation, please refer to the following documents:

- [🏗 **System Architecture**](./documentation/architecture.md): Overview of the modular design and data flow.
- [🕵️‍♂️ **Scraper Logic**](./documentation/scrapers.md): Details on how we extract data from Blogs, YouTube, and PubMed.
- [⚖️ **Trust Scoring Algorithm**](./documentation/trust_scoring.md): Comprehensive breakdown of the scoring formula and weights.
- [⚙️ **Data Processing**](./documentation/data_processing.md): Explanation of semantic tagging and content chunking.
- [📚 **API Reference**](./documentation/api_reference.md): Detailed function signatures and usage.

---

## 📊 Technical Features

- **Semantic Tagging**: Uses `KeyBERT` for keyword extraction without requiring pre-defined labels.
- **Content Chunking**: Automatically splits articles into 150-word chunks for downstream LLM/RAG integration.
- **Anti-Bot Resilience**: Implements header rotation (`fake-useragent`) and request throttling.
- **Language Detection**: Automatic identification of content language using `langdetect`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for suggestions.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

