Milvus architecture on Kubernetes: QueryNodes, IndexNodes, DataNodes

Overview
This document describes scaling Milvus components on Kubernetes using Helm and values that align with MinIO and Kafka backends. It explains recommended node sizing and best-effort index shard distribution.

Key points
- Separate QueryNode (CPU-bound), IndexNode (CPU+memory), and DataNode (disk I/O) resources.
- Use MinIO for object storage and Kafka for streaming/incremental indexing.
- Tune replicas and resource requests according to dataset size and QPS.
