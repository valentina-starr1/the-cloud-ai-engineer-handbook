"""
Sample RAG application instrumented with OpenLLMetry/OpenTelemetry spans.
This is a minimal illustrative example — adapt to your production stack.
"""
from fastapi import FastAPI, Request
from tracer_setup import init_tracer
from opentelemetry.trace import SpanKind
import time

tracer = init_tracer("sample-rag")
app = FastAPI()

@app.post('/query')
async def query(request: Request):
    payload = await request.json()
    query_text = payload.get('query', '')
    request_id = payload.get('request_id', 'unknown')

    with tracer.start_as_current_span('rag_request', kind=SpanKind.SERVER) as span:
        span.set_attribute('request.id', request_id)
        span.set_attribute('query.length', len(query_text))

        # Embedding span
        with tracer.start_as_current_span('embeddings.generate') as s_emb:
            s_emb.set_attribute('model', 'embedding-model-v1')
            time.sleep(0.02)  # simulate work

        # Vector search span
        with tracer.start_as_current_span('vector_search') as s_vs:
            s_vs.set_attribute('retriever', 'faiss-hnsw')
            s_vs.set_attribute('num_candidates', 10)
            time.sleep(0.01)

        # LLM call span
        with tracer.start_as_current_span('llm.generate') as s_llm:
            s_llm.set_attribute('model', 'gpt-4o')
            time.sleep(0.05)

        return {"request_id": request_id, "answer": "(simulated)"}
