"""
tagging.py
==========
Automatic topic tagging using KeyBERT.
Falls back to simple keyword extraction if KeyBERT is unavailable.
"""

# Medical domain keywords for fallback tagging
MEDICAL_KEYWORDS = [
    "diabetes", "insulin", "cancer", "tumor", "ai", "artificial intelligence",
    "machine learning", "deep learning", "neural network", "healthcare",
    "diagnosis", "treatment", "therapy", "clinical", "patient", "hospital",
    "disease", "symptom", "medication", "vaccine", "pandemic", "covid",
    "virus", "bacteria", "infection", "surgery", "radiology", "imaging",
    "genomics", "biomarker", "drug", "pharmaceutical", "mental health",
    "depression", "anxiety", "neurological", "cardiology", "oncology",
    "pediatrics", "epidemiology", "public health", "medical", "health",
    "data", "algorithm", "model", "prediction", "accuracy", "precision"
]

try:
    from keybert import KeyBERT
    _kw_model = KeyBERT()
    KEYBERT_AVAILABLE = True
except ImportError:
    _kw_model = None
    KEYBERT_AVAILABLE = False


def generate_tags(text, top_n=6):
    """
    Generate topic tags from text.

    Parameters
    ----------
    text  : str  – combined content text
    top_n : int  – number of tags to return

    Returns
    -------
    list of str  – e.g. ["diabetes", "machine learning", "healthcare"]
    """
    if not text or len(text.strip()) < 30:
        return []

    if KEYBERT_AVAILABLE:
        return _keybert_tags(text, top_n)
    else:
        return _fallback_tags(text, top_n)


def _keybert_tags(text, top_n):
    """Use KeyBERT for semantic keyword extraction."""
    try:
        # Limit text length for performance
        trimmed = text[:5000]
        keywords = _kw_model.extract_keywords(
            trimmed,
            keyphrase_ngram_range=(1, 2),   # single words and bigrams
            stop_words="english",
            use_maxsum=True,                # diversity in results
            nr_candidates=20,
            top_n=top_n
        )
        return [kw[0].title() for kw in keywords]
    except Exception as e:
        print(f"[Tagging] KeyBERT failed: {e}, using fallback.")
        return _fallback_tags(text, top_n)


def _fallback_tags(text, top_n):
    """Simple frequency-based keyword matching against medical vocabulary."""
    text_lower = text.lower()
    word_freq = {}

    for keyword in MEDICAL_KEYWORDS:
        count = text_lower.count(keyword)
        if count > 0:
            word_freq[keyword] = count

    # Sort by frequency, return top_n
    sorted_kws = sorted(word_freq, key=word_freq.get, reverse=True)
    return [kw.title() for kw in sorted_kws[:top_n]]
