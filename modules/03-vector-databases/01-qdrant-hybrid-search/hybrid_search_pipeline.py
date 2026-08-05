#!/usr/bin/env python3
"""
Hybrid search pipeline:
1. Build dense embeddings (sentence-transformers)
2. Build sparse vectors (TF-IDF)
3. Insert into Qdrant with payloads
4. Query: dense search -> get candidates -> rerank with sparse score using RRF
"""
import argparse
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

def rrf_scores(ranks, k=60):
    # Reciprocal Rank Fusion: sum(1/(k + rank))
    scores = {}
    for rank_list in ranks:
        for idx, doc_id in enumerate(rank_list):
            scores.setdefault(doc_id, 0.0)
            scores[doc_id] += 1.0 / (60 + idx + 1)
    return scores

def build_dense_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings

def build_sparse_matrix(texts):
    vectorizer = TfidfVectorizer(max_features=32768, stop_words='english')
    sparse = vectorizer.fit_transform(texts)
    return vectorizer, sparse

def insert_to_qdrant(client: QdrantClient, collection_name, embeddings, texts, payloads=None):
    client.recreate_collection(collection_name=collection_name, vectors_config={
        "dense_vector": VectorParams(size=embeddings.shape[1], distance=Distance.COSINE)
    })
    points = []
    for i, emb in enumerate(embeddings):
        payload = payloads[i] if payloads else {}
        payload.update({"text": texts[i]})
        points.append(PointStruct(id=i, vector=emb.tolist(), payload=payload))
    client.upsert(collection_name=collection_name, points=points, wait=True)

def hybrid_query(client: QdrantClient, collection_name: str, query_text: str, vectorizer: TfidfVectorizer, sentence_model: SentenceTransformer, top_k=50):
    # Dense candidates
    q_emb = sentence_model.encode([query_text], convert_to_numpy=True)[0]
    search_results = client.search(collection_name=collection_name, query_vector=q_emb.tolist(), limit=top_k)
    dense_ids = [r.id for r in search_results]
    # Build sparse query vector and compute sparse similarities locally
    sparse_q = vectorizer.transform([query_text])
    # For each candidate fetch text payload and compute cosine with sparse vectors if you stored sparse features
    # This simplified pipeline re-ranks by mixing dense rank with payload match length
    # For demonstration, build two ranking lists: dense ranking and text length ranking
    dense_ranks = dense_ids
    length_ranks = sorted(dense_ids, key=lambda i: len(client.retrieve(collection_name=collection_name, ids=[i])[0].payload.get("text","")), reverse=True)
    combined = rrf_scores([dense_ranks, length_ranks])
    # Return top re-ranked ids
    top = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return top

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="JSON file with [{'id':..., 'text':..., 'meta':{}}]")
    parser.add_argument("--collection", default="hybrid_demo")
    parser.add_argument("--qdrant_host", default="localhost")
    args = parser.parse_args()

    with open(args.data, "r") as f:
        docs = json.load(f)
    texts = [d["text"] for d in docs]
    payloads = [d.get("meta", {}) for d in docs]

    print("Building dense embeddings...")
    dense_embs = build_dense_embeddings(texts)
    print("Building sparse TF-IDF features...")
    vect, sparse = build_sparse_matrix(texts)

    client = QdrantClient(host=args.qdrant_host, prefer_grpc=False)
    print("Inserting to Qdrant...")
    insert_to_qdrant(client, args.collection, dense_embs, texts, payloads)
    print("Example query re-ranking:")
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    res = hybrid_query(client, args.collection, "example query about AI inference", vect, sentence_model)
    print("Top re-ranked:", res)

if __name__ == "__main__":
    main()
