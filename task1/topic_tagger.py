from keybert import KeyBERT

kw_model = KeyBERT()

def generate_tags(text, top_n=5):
    if not text or len(text.strip()) < 20:
        return []
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=top_n)
    return [kw[0] for kw in keywords]