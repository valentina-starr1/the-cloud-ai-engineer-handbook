# OpenLLMetry Tracing for RAG Pipelines

This module explains how to instrument RAG pipelines using OpenLLMetry/OpenTelemetry and export traces to Jaeger or other backends.

Highlights:
- Instrument embedding, vector-store retrieval, and LLM calls as separate spans.
- Attach attributes: model.name, request.id, retriever.name, num_documents.
- Export using OTLP or Jaeger exporters. Use sampling rules in production to avoid high cardinality.

See tracer_setup.py for example tracer initialization and traced_rag_app.py for a sample RAG app with custom span attributes.
