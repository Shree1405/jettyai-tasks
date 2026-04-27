# 🏥 Task 2: Overview (Improved Scraper)

Task 2 is a second-generation medical content scraping pipeline. It is built with **modularization**, **scalability**, and **advanced data engineering** in mind.

## 🌟 Key Improvements over Task 1
- **Decoupled Logic**: Scrapers, scoring algorithms, and utilities are separated into distinct packages.
- **Advanced Scoring**: Moves from simple addition to a weighted multi-factor formula (0.0 - 1.0) with automated abuse detection.
- **Semantic Chunking**: Implements context-aware text splitting for better LLM/RAG integration.
- **Resilience**: Enhanced error handling ensures the pipeline survives partial failures.

## 🚀 Execution
Run the system from the `task2/` directory:
```bash
python main.py
```

## 📁 Storage
Final records are saved to `task2/output/` in a highly structured JSON format including detailed scoring breakdowns.
