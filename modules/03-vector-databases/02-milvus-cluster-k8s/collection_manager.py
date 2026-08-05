#!/usr/bin/env python3
"""
Create partitioned collections and HNSW index profiles in Milvus using pymilvus.
"""
from pymilvus import (
    connections,
    FieldSchema, CollectionSchema, DataType,
    Collection, utility
)
import argparse

def connect(host="localhost", port="19530"):
    connections.connect(host=host, port=port)
    print("Connected to Milvus at", host, port)

def create_collection(name="demo_collection", vector_dim=1536, shards=2):
    if utility.has_collection(name):
        print("Collection exists, skipping:", name)
        return
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=vector_dim),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096)
    ]
    schema = CollectionSchema(fields, description="Demo partitioned collection")
    col = Collection(name, schema=schema, shards_num=shards)
    print("Created collection:", name)
    return col

def create_partition(collection_name, partition_tag):
    col = Collection(collection_name)
    col.create_partition(partition_tag)
    print("Created partition:", partition_tag)

def create_hnsw_index(collection_name, index_name="hnsw_index", M=48, efConstruction=200):
    col = Collection(collection_name)
    index_params = {
        "index_type": "HNSW",
        "metric_type": "IP",
        "params": {"M": M, "efConstruction": efConstruction}
    }
    col.create_index(field_name="embedding", index_params=index_params)
    print("Created HNSW index on", collection_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="19530")
    parser.add_argument("--collection", default="demo_collection")
    parser.add_argument("--dim", type=int, default=1536)
    args = parser.parse_args()
    connect(args.host, args.port)
    create_collection(args.collection, vector_dim=args.dim, shards=2)
    create_partition(args.collection, "partition_1")
    create_hnsw_index(args.collection)
    print("Done")

if __name__ == "__main__":
    main()
