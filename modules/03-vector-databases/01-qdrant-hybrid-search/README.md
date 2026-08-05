# Qdrant sparse-dense hybrid search and payload filtering

Overview
This module contains a pipeline that builds dense embeddings (sentence-transformers) and sparse TF-IDF vectors, indexes them into Qdrant, and performs hybrid search by combining dense similarity with sparse scores and then reranking via Reciprocal Rank Fusion (RRF).

Design
- Dense embeddings: sentence-transformers / SBERT
- Sparse features: TF-IDF using scikit-learn
- Search: Top-K on dense space then re-rank using sparse similarity + payload filters
- RRF: combine multiple ranked lists robustly

Usage
- pip install -r requirements (sentence-transformers, qdrant-client, scikit-learn, numpy)
- python hybrid_search_pipeline.py --insert example_data.json
