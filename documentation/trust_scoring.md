# ⚖️ Trust Scoring Algorithm

This document explains the logic, formula, and weighting system used to evaluate the trustworthiness of scraped medical content.

---

## 🔬 The Formula

The Trust Score is a weighted summation of five distinct factors, resulting in a score between **0.0 and 1.0**.

$$Trust Score = \sum (Factor_{i} \times Weight_{i}) - Penalties$$

---

## 📊 Factor Weights

| Factor | Weight | Description |
| :--- | :--- | :--- |
| **Domain Authority** | 30% | The reputation of the hosting website. |
| **Author Credibility**| 25% | The credentials and identity of the content creator. |
| **Recency** | 20% | How up-to-date the information is. |
| **Medical Disclaimer**| 15% | Presence of safety warnings for health content. |
| **Content Richness** | 10% | The depth and length of the content/transcript. |

---

## 🛠 Factor Details

### 1. Domain Authority
We maintain a curated list of domains with pre-assigned scores:
- **1.0**: PubMed, WHO, CDC, NIH, NEJM, Lancet.
- **0.90**: Mayo Clinic, Cleveland Clinic.
- **0.80**: Healthline, Medical News Today.
- **0.65**: YouTube (Platform average).
- **0.30**: Unknown/Default blogs.

### 2. Author Credibility
- **Known Organizations (0.95)**: Content attributed to groups like "WHO" or "Mayo Clinic Staff".
- **Verified Names (0.70)**: Presence of a full name (First Last) suggests accountability.
- **Generic/Unknown (0.10)**: Content without an author or with anonymous tags.

### 3. Recency
Medical information decays over time.
- **1.0**: Published ≤ 1 year ago.
- **0.8**: Published ≤ 2 years ago.
- **0.6**: Published ≤ 5 years ago.
- **0.2**: Published > 10 years ago.

### 4. Content Richness
- **Long-form (1.0)**: > 1000 words.
- **Mid-form (0.65 - 0.85)**: 200 - 500 words.
- **Thin Content (0.20)**: < 50 words.

---

## 🛡 Abuse Prevention (Penalties)

To prevent manipulation, the algorithm applies negative weights if suspicious patterns are detected:

| Scenario | Penalty | Reason |
| :--- | :--- | :--- |
| **Suspicious Author** | -0.10 | Keywords like "admin", "webmaster", or "anonymous". |
| **Low Authority** | -0.10 | Domains with a score ≤ 0.30 (Potential SEO spam). |
| **Missing Disclaimer**| -0.08 | Mandatory for non-peer-reviewed health content. |
| **Extreme Age** | -0.15 | Content older than 10 years (Critical for medical info). |

---

## 📄 Implementation Reference
The logic is implemented in `task2/scoring/trust_score.py`. It returns a detailed breakdown allowing users to see exactly why a specific score was awarded.
