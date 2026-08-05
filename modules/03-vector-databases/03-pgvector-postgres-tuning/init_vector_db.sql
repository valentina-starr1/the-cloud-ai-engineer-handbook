-- Enable extension and create table for pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Create embeddings table
CREATE TABLE IF NOT EXISTS documents (
  id BIGSERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  embedding vector(1536),
  metadata JSONB
);

-- Create HNSW index for low-latency retrieval
-- Example parameters: M controls memory/graph connectivity, ef_search tunes recall at runtime
CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Alternative: HNSW (supported if using pgvector >= x)
-- CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx ON documents USING hnsw (embedding) WITH (m = 16, ef_construction = 200);

-- Example: insert test row
INSERT INTO documents (text, embedding, metadata) VALUES (
  'Example document about AI infrastructure',
  array_fill(0.0::double precision, ARRAY[1536])::vector,
  '{"tags":["inference","infrastructure"]}'
) ON CONFLICT DO NOTHING;
