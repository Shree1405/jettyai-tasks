"""
chunking.py
===========
Splits long text content into manageable chunks for downstream processing.
"""

def chunk_text(text, max_words=150):
    """
    Split a long string into chunks of ~max_words each,
    splitting at sentence boundaries where possible.

    Parameters
    ----------
    text      : str – input text
    max_words : int – approximate max words per chunk

    Returns
    -------
    list of str
    """
    if not text or not text.strip():
        return []

    sentences = _split_sentences(text)
    chunks    = []
    current   = []
    word_count = 0

    for sentence in sentences:
        words = sentence.split()
        if word_count + len(words) > max_words and current:
            chunks.append(" ".join(current).strip())
            current    = []
            word_count = 0
        current.extend(words)
        word_count += len(words)

    if current:
        chunks.append(" ".join(current).strip())

    return [c for c in chunks if len(c) > 20]   # drop trivial chunks


def chunk_paragraphs(paragraphs, max_words=150):
    """
    Re-chunk a list of paragraphs that may individually be too long.

    Parameters
    ----------
    paragraphs : list of str
    max_words  : int

    Returns
    -------
    list of str
    """
    result = []
    for para in paragraphs:
        words = para.split()
        if len(words) <= max_words:
            result.append(para)
        else:
            # Break the long paragraph further
            result.extend(chunk_text(para, max_words))
    return result


def _split_sentences(text):
    """Naive sentence splitter on '. ', '! ', '? '."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
