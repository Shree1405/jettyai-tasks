# 🎯 Task 1: Overview

Task 1 is a multi-source web scraping and content analysis system. It is designed to extract, clean, and evaluate medical-related content from diverse web platforms.

## 🌟 Key Objectives
- **Data Acquisition**: Retrieve content from Blogs, YouTube, and PubMed.
- **Content Enrichment**: Automatically generate topic tags using AI.
- **Credibility Assessment**: Calculate a trust score based on source-specific heuristics.
- **Standardization**: Output data in a uniform JSON schema for downstream consumption.

## 🚀 Quick Start
To run the Task 1 pipeline:
1. Navigate to the `task1/` directory.
2. Install dependencies: `pip install -r requirements.txt` (or manually install `requests`, `bs4`, `youtube-transcript-api`, `keybert`).
3. Execute the orchestrator: `python main.py`.

## 📁 Output
All scraped data is stored in the `task1/scraped_data/` directory as individual and combined JSON files.
