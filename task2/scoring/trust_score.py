"""
trust_score.py
==============
Trust Score Formula:
    Trust Score = f(author_credibility, domain_authority,
                    recency, medical_disclaimer, content_richness)

Final score is normalized to 0.0 – 1.0
"""

from datetime import datetime

# ── Domain authority table (manually curated) ────────────────────────────────
DOMAIN_AUTHORITY = {
    # High authority (0.85 – 1.0)
    "pubmed.ncbi.nlm.nih.gov": 1.0,
    "who.int": 0.97,
    "cdc.gov": 0.96,
    "nih.gov": 0.95,
    "nejm.org": 0.95,
    "thelancet.com": 0.94,
    "bmj.com": 0.93,
    "jamanetwork.com": 0.92,
    "nature.com": 0.91,
    "mayoclinic.org": 0.90,
    "clevelandclinic.org": 0.88,
    "hopkinsmedicine.org": 0.88,

    # Medium-high authority (0.65 – 0.84)
    "healthline.com": 0.80,
    "medicalnewstoday.com": 0.78,
    "webmd.com": 0.75,
    "medscape.com": 0.82,
    "youtube.com": 0.65,

    # Medium authority (0.40 – 0.64)
    "towardsdatascience.com": 0.60,
    "medium.com": 0.50,
    "realpython.com": 0.58,
    "geeksforgeeks.org": 0.52,

    # Default for unknown domains
    "__default__": 0.30,
}

# ── Known credible author organizations ──────────────────────────────────────
CREDIBLE_ORGANIZATIONS = [
    "who", "cdc", "nih", "mayo clinic", "cleveland clinic",
    "johns hopkins", "harvard", "stanford", "oxford", "cambridge",
    "lancet", "nejm", "bmj", "jama", "nature", "pubmed",
    "healthline", "medscape", "medically reviewed"
]

# ── Weights for each factor (must sum to 1.0) ────────────────────────────────
WEIGHTS = {
    "domain_authority":          0.30,
    "author_credibility":        0.25,
    "recency":                   0.20,
    "medical_disclaimer":        0.15,
    "content_richness":          0.10,
}

# ─────────────────────────────────────────────────────────────────────────────

def calculate_trust_score(source_type, author, published_date,
                           domain, content_chunks,
                           has_medical_disclaimer=False,
                           has_transcript=False):
    """
    Calculate trust score between 0.0 and 1.0.

    Parameters
    ----------
    source_type           : str   – "blog", "youtube", "pubmed"
    author                : str or list – author name(s)
    published_date        : str   – "YYYY-MM-DD" or "YYYY" or "Unknown"
    domain                : str   – e.g. "healthline.com"
    content_chunks        : list  – list of text strings
    has_medical_disclaimer: bool
    has_transcript        : bool  – for YouTube only

    Returns
    -------
    dict with "score" (float 0-1) and "breakdown" (dict of factor scores)
    """

    scores = {}

    scores["domain_authority"]   = _score_domain(domain)
    scores["author_credibility"] = _score_author(author, source_type)
    scores["recency"]            = _score_recency(published_date)
    scores["medical_disclaimer"] = _score_disclaimer(has_medical_disclaimer, source_type)
    scores["content_richness"]   = _score_content(content_chunks, source_type, has_transcript)

    # Weighted sum
    raw_score = sum(WEIGHTS[k] * scores[k] for k in WEIGHTS)

    # Apply abuse-prevention penalties
    penalty, penalty_reasons = _abuse_penalties(author, domain, published_date,
                                                 has_medical_disclaimer, source_type)
    final_score = max(0.0, raw_score - penalty)

    return {
        "score": round(final_score, 4),
        "breakdown": {k: round(v, 4) for k, v in scores.items()},
        "penalty_applied": round(penalty, 4),
        "penalty_reasons": penalty_reasons
    }

# ── Factor scoring functions ──────────────────────────────────────────────────

def _score_domain(domain):
    """Look up domain authority score."""
    domain = domain.lower().replace("www.", "")
    return DOMAIN_AUTHORITY.get(domain, DOMAIN_AUTHORITY["__default__"])


def _score_author(author, source_type):
    """
    Score author credibility.
    - Multiple authors → average individual scores
    - Unknown author → 0.1 (penalized but not zero)
    - Recognized org → high score
    """
    if isinstance(author, list):
        if not author or author == ["Unknown"]:
            return 0.1
        individual_scores = [_single_author_score(a) for a in author]
        return sum(individual_scores) / len(individual_scores)   # average

    return _single_author_score(author)


def _single_author_score(name):
    if not name or name.strip().lower() in ("unknown", "", "none"):
        return 0.1

    name_lower = name.lower()

    # Check against known credible organizations
    if any(org in name_lower for org in CREDIBLE_ORGANIZATIONS):
        return 0.95

    # Has a full name (First Last) → likely real person
    parts = name.strip().split()
    if len(parts) >= 2:
        return 0.70

    # Single word / initials only → lower confidence
    return 0.40


def _score_recency(published_date):
    """
    Score based on how recent the content is.
    - Within 1 year  → 1.0
    - Within 2 years → 0.8
    - Within 5 years → 0.6
    - Older          → 0.3
    - Unknown        → 0.2
    """
    if not published_date or published_date == "Unknown":
        return 0.2

    try:
        # Handle both "YYYY-MM-DD" and "YYYY"
        year_str = str(published_date)[:4]
        year = int(year_str)
        current_year = datetime.now().year
        age = current_year - year

        if age <= 1:   return 1.0
        if age <= 2:   return 0.8
        if age <= 5:   return 0.6
        if age <= 10:  return 0.4
        return 0.2
    except (ValueError, TypeError):
        return 0.2


def _score_disclaimer(has_medical_disclaimer, source_type):
    """
    Medical disclaimer presence score.
    PubMed is inherently peer-reviewed → always full score.
    """
    if source_type == "pubmed":
        return 1.0
    return 1.0 if has_medical_disclaimer else 0.0


def _score_content(content_chunks, source_type, has_transcript=False):
    """
    Score based on content richness.
    - YouTube with transcript → bonus
    - Long, chunked content   → higher score
    """
    if not content_chunks or content_chunks == ["Content could not be extracted."]:
        return 0.0

    total_words = sum(len(c.split()) for c in content_chunks)

    if source_type == "youtube":
        if has_transcript:
            if total_words > 1000: return 1.0
            if total_words > 300:  return 0.8
            return 0.6
        else:
            return 0.3   # description only, no transcript

    # Blog / PubMed
    if total_words > 1000: return 1.0
    if total_words > 500:  return 0.85
    if total_words > 200:  return 0.65
    if total_words > 50:   return 0.40
    return 0.20


# ── Abuse prevention logic ────────────────────────────────────────────────────

def _abuse_penalties(author, domain, published_date,
                      has_medical_disclaimer, source_type):
    """
    Returns (total_penalty_float, list_of_reason_strings).

    Penalties prevent manipulation by fake authors, SEO spam,
    misleading medical content, and outdated information.
    """
    penalty = 0.0
    reasons = []

    # 1. Fake / suspicious author patterns
    if isinstance(author, str):
        author_lower = author.lower()
        suspicious_patterns = ["admin", "user", "test", "anonymous",
                                "editor", "staff", "webmaster", "no author"]
        if any(p in author_lower for p in suspicious_patterns):
            penalty += 0.10
            reasons.append("Suspicious/generic author name detected (-0.10)")

    # 2. SEO spam / low-authority domain
    domain_score = _score_domain(domain)
    if domain_score <= 0.30:
        penalty += 0.10
        reasons.append("Low domain authority — possible SEO spam blog (-0.10)")

    # 3. Missing medical disclaimer for medical content
    if source_type in ("blog", "youtube") and not has_medical_disclaimer:
        penalty += 0.08
        reasons.append("No medical disclaimer found on medical content (-0.08)")

    # 4. Outdated content penalty
    try:
        year = int(str(published_date)[:4])
        age  = datetime.now().year - year
        if age > 10:
            penalty += 0.15
            reasons.append(f"Content is {age} years old — strong recency penalty (-0.15)")
        elif age > 5:
            penalty += 0.07
            reasons.append(f"Content is {age} years old — moderate recency penalty (-0.07)")
    except (ValueError, TypeError):
        pass

    return round(penalty, 4), reasons
