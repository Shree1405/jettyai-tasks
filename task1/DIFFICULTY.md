# 📈 Task 1: Difficulty & Complexity Analysis

This document outlines the implementation challenges and operational complexity of Task 1.

---

## 🏗 Implementation Difficulty: **Medium**

Task 1 is a monolithic implementation that focuses on breadth of sources rather than architectural depth.

### 🧩 Complexity Breakdown

| Component | Difficulty | Challenges |
| :--- | :--- | :--- |
| **Blog Scraper** | 🟢 Easy | Standard DOM traversal using BeautifulSoup. |
| **YouTube Scraper** | 🟡 Medium | Managing transcript API limits and regex-based metadata extraction. |
| **PubMed Scraper** | 🟠 Hard | Handling highly structured medical data and inconsistent author formats. |
| **Trust Scoring** | 🟢 Easy | Simple additive logic (if X then +Y). |
| **Tagging** | 🟡 Medium | Integration with KeyBERT and managing model downloads. |

---

## 🛠 Operational Challenges

1. **Anti-Bot Resistance**: Task 1 uses basic header rotation. It is susceptible to IP blocking on high-authority medical sites if run too frequently.
2. **Monolithic Maintenance**: Since logic is tightly coupled in `main.py`, adding a new source requires modifications to the core orchestration loop, increasing the risk of regression.
3. **Data Quality**: The simple scoring model can be easily "gamed" by blogs with high word counts but low actual credibility.

---

## 🎯 Target Skill Level
**Beginner to Intermediate Python Developer**
- Requires understanding of web scraping (BS4), API consumption, and basic data structures.
