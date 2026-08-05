PGVector: choosing HNSW vs IVFFlat inside Postgres

Overview
PGVector wraps vector storage inside PostgreSQL. For low-latency nearest neighbor search use HNSW (graph-based). For large-scale approximate search with controllable recall/throughput, consider IVFFlat + OPQ with prebuilt centroids.

This folder provides an initialization SQL file and a small Python repository layer using SQLAlchemy to query HNSW indexes.
