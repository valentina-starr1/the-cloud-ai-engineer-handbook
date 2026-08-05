#!/usr/bin/env python3
"""
SQLAlchemy repository for similarity search using pgvector.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import numpy as np

class VectorRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_document(self, text: str, vector: np.ndarray, metadata: dict = None):
        with self.engine.begin() as conn:
            conn.execute(
                text("INSERT INTO documents (text, embedding, metadata) VALUES (:text, :embedding, :metadata)"),
                {"text": text, "embedding": vector.tolist(), "metadata": metadata or {}}
            )

    def search_hnsw(self, query_vector, top_k=10):
        # This example uses ivfflat index (vector_cosine_ops) - adjust SQL for your index type
        sql = text("""
            SELECT id, text, metadata, embedding <#> :q AS distance
            FROM documents
            ORDER BY embedding <#> :q
            LIMIT :k
        """)
        with self.engine.connect() as conn:
            rows = conn.execute(sql, {"q": query_vector.tolist(), "k": top_k}).fetchall()
        return rows

if __name__ == "__main__":
    import argparse
    import sqlalchemy
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsn", required=True)
    args = parser.parse_args()
    engine = sqlalchemy.create_engine(args.dsn)
    repo = VectorRepository(engine)
    # Example query: zero vector
    results = repo.search_hnsw(np.zeros(1536), top_k=5)
    print(results)
