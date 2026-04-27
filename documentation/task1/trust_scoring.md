# ⚖️ Task 1: Trust Scoring Algorithm

The Trust Score in Task 1 is an **additive heuristic** ranging from 0 to 100. It provides a baseline measure of how reliable a piece of content is likely to be.

---

## 🔢 Scoring Components

### 1. Source Weight (Max 40)
The platform hosting the content is the strongest signal.
- **PubMed**: +40 points (Peer-reviewed)
- **YouTube**: +20 points (Educational/Visual)
- **Blog**: +15 points (General information)

### 2. Authorship (Max 15)
- **Known Creator**: +15 points if an author name or channel title is successfully extracted.
- **Anonymous**: 0 points.

### 3. Recency (Max 20)
- **Dated Content**: +10 points if a publication date is found.
- **Freshness Bonus**: +10 points if the content was published in 2022 or later.

### 4. Content Depth (Max 15)
- **Long-form**: +15 points if > 500 words.
- **Medium-form**: +8 points if > 200 words.

### 5. Media Quality (Max 10)
- **Verified Audio**: +10 points (YouTube only) if a transcript is available.

---

## 📊 Summary Table
| Factor | Max Points |
| :--- | :--- |
| Source Reliability | 40 |
| Verified Author | 15 |
| Date & Freshness | 20 |
| Word Count / Depth | 15 |
| Transcript Presence| 10 |
| **TOTAL** | **100** |
