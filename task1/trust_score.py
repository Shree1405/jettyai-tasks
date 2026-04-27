def calculate_trust_score(source_type, author, published_date, content_chunks, has_transcript=False):
    score = 0

    # Rule 1: Source type base score
    if source_type == "pubmed":
        score += 40      # Peer-reviewed = highest trust
    elif source_type == "youtube":
        score += 20
    elif source_type == "blog":
        score += 15

    # Rule 2: Author known/present
    if author and author != "Unknown":
        score += 15

    # Rule 3: Date is present and recent
    if published_date and published_date != "Unknown":
        score += 10
        try:
            year = int(str(published_date)[:4])
            if year >= 2022:
                score += 10   # Bonus for recency
        except:
            pass

    # Rule 4: Content richness
    total_words = sum(len(chunk.split()) for chunk in content_chunks)
    if total_words > 500:
        score += 15
    elif total_words > 200:
        score += 8

    # Rule 5: YouTube transcript available
    if source_type == "youtube" and has_transcript:
        score += 10

    return min(score, 100)   # Cap at 100