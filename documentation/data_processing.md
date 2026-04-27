# ⚙️ Data Processing: Tagging & Chunking

This document describes how raw text is transformed into structured, searchable, and LLM-ready data chunks.

---

## 🏷 Semantic Tagging

Instead of using a fixed list of categories, JettyAI Tasks uses **KeyBERT** for dynamic keyword extraction.

### How it Works
1. **Model**: Uses a BERT-based transformer model to create document embeddings.
2. **Cosine Similarity**: Identifies sub-phrases within the text that are most similar to the document's overall embedding.
3. **Extraction**: Returns the top 5 most relevant keywords/phrases as "Topic Tags".

### Benefits
- **No Taxonomy Required**: Handles new medical topics (e.g., "AI in healthcare") automatically.
- **Context Aware**: Better than simple frequency-based keyword extraction.

---

## 🧩 Content Chunking

To support downstream Retrieval-Augmented Generation (RAG) and LLM contexts, the system implements a logical chunking strategy.

### Chunking Logic
- **Target Size**: ~150 words per chunk.
- **Integrity**: Chunks are created by grouping paragraphs until the word limit is reached. It avoids splitting a single paragraph across chunks unless the paragraph itself is excessively long.
- **Normalization**: Ensures that even if a scraper returns many small paragraphs, they are combined into meaningful blocks for analysis.

### Schema Example
```json
"content_chunks": [
  "Paragraph 1 text... Paragraph 2 text...",
  "Paragraph 3 text... Paragraph 4 text..."
]
```

---

## 🌐 Language Detection

The system uses the `langdetect` library to identify the primary language of the content.

- **Process**: Analyzes the first 200 words of the combined content.
- **Usage**:
  - Sets the `language` field in the final JSON.
  - Can be used to trigger language-specific tagging models (Future enhancement).
  - Skips processing if the text is too short to accurately detect.
