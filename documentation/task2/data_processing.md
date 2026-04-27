# ⚙️ Task 2: Data Processing (Chunking & Tagging)

Task 2 implements advanced text processing to prepare scraped data for AI applications (RAG/LLM).

---

## 🧩 Semantic Chunking (`utils/chunking.py`)

Unlike simple character-based splitting, Task 2 uses **Paragraph-Preserving Chunking**.

### Logic
1. **Target**: ~150 words per chunk.
2. **Method**:
    - Iterate through paragraphs extracted by the scraper.
    - Group paragraphs together into a single chunk until the word limit is reached.
    - Start a new chunk if adding the next paragraph would exceed the limit.
3. **Benefit**: Ensures that logical units of thought (paragraphs) are not split in half, providing better context for AI embeddings.

## 🏷 Dynamic Tagging (`utils/tagging.py`)

Task 2 utilizes **KeyBERT** for unsupervised topic extraction.

### Process
1. **Model**: Uses a pre-trained BERT transformer model.
2. **Candidate Extraction**: Identifies noun phrases within the text.
3. **Similarity**: Ranks phrases by their cosine similarity to the document's overall embedding.
4. **Output**: The top 5 highest-ranking phrases are returned as topic tags.
5. **Robustness**: Automatically skips tagging if the text is too short or if a language error occurs.
