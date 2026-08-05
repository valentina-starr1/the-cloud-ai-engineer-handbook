# LlamaIndex Hierarchical Retrieval Patterns

This module explores hierarchical node parsing, parent-child chunking, and sentence window retrieval strategies using LlamaIndex (or similar retrieval indices).

Key concepts:

- Node-level parsing: break documents into semantically meaningful nodes (sections, paragraphs).
- Parent-child chunking: maintain hierarchical references to allow coarse-to-fine retrieval.
- Sentence window retrieval: preserve sentence boundaries when creating overlapping chunks for better context.

See rag_pipeline_config.json for tuning parameters and hierarchical_rag.py for an example pipeline constructing an AutoMergingRetriever and sentence-window retriever.
