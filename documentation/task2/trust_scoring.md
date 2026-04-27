# ⚖️ Task 2: Advanced Trust Scoring

Task 2 uses a **Weighted Multi-Factor Formula** (0.0 to 1.0) with an integrated **Penalty Engine** for abuse detection.

---

## 🏗 The Scoring Formula

The base score is calculated as follows:
`Score = (Domain Authority * 0.3) + (Author Credibility * 0.25) + (Recency * 0.2) + (Medical Disclaimer * 0.15) + (Content Richness * 0.1)`

### 1. Domain Authority (30%)
Based on a curated lookup table of known medical authorities:
- `pubmed.ncbi.nlm.nih.gov`: 1.0
- `who.int`: 0.97
- `cdc.gov`: 0.96
- `youtube.com`: 0.65
- `Unknown`: 0.30

### 2. Author Credibility (25%)
- **Verified Org**: 0.95
- **Named Author**: 0.70
- **Unknown**: 0.0

### 3. Recency (20%)
- ≤ 1 year old: 1.0
- ≤ 5 years old: 0.6
- > 10 years old: 0.2

### 4. Medical Disclaimer (15%)
- Present: 1.0
- Absent: 0.0

---

## 🚫 The Penalty Engine
After the base score is calculated, automated deductions are applied for "Red Flags":
- **Suspicious Author**: -0.10 for names like "admin", "webmaster", "staff".
- **Low Authority Domain**: -0.10 for domains scoring ≤ 0.30.
- **Outdated Content**: -0.15 for content > 10 years old.
