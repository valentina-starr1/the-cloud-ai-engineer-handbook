# vLLM Kubernetes Deployment — PagedAttention on K8s

## 1. Architectural Overview

vLLM implements efficient attention for large language models using a memory-efficient algorithm called PagedAttention. Instead of keeping all key/value tensors fully resident in GPU memory, vLLM pages attention state in and out — staging parts of the attention key/value cache between GPU memory and host memory (or NVMe) as needed during generation.

When deployed on Kubernetes, the common architecture is:

- Each vLLM Pod runs a single model worker process and exposes an OpenAI-compatible HTTP API for inference.
- Pods are scheduled onto GPU-capable nodes using the Kubernetes device plugin (nvidia.com/gpu). For multi-GPU pods, each container can request multiple GPUs and vLLM will use CUDA to bind tensors across devices.
- PagedAttention reduces peak GPU memory pressure by moving cold attention pages out of GPU memory; this enables serving larger context windows or bigger models on a fixed GPU count.
- Persistent storage (fast NVMe-backed hostPath or local SSD) is recommended for storing model shards and any paged cache to avoid network-bound paging.

Diagram (logical)

```
[Client] --> [Ingress / LB] --> [vLLM Pod A (node:gpu-1)]
                            \-> [vLLM Pod B (node:gpu-2)]

vLLM Pod:
  - Pod with containers: vllm-server
  - mounts: model weights on /models, optional local paging dir /var/lib/vllm/pagecache
  - resources: nvidia.com/gpu: 4, cpu: 8, memory: 64Gi
```

## 2. System Prerequisites

- Kubernetes cluster (EKS/GKE) with GPU-enabled node pools.
  - Ensure NVIDIA device plugin is installed: https://github.com/NVIDIA/k8s-device-plugin
- GPU drivers and container runtime
  - Nodes must have NVIDIA drivers compatible with your CUDA version.
  - Install the NVIDIA Container Toolkit on nodes to allow GPU access inside containers.
- CUDA and cuDNN compatibility
  - Choose a vLLM container image built for the CUDA version on your nodes (e.g., CUDA 11.x or 12.x). Mismatches between driver and container CUDA may prevent GPU access.
- Storage and paging
  - Fast local storage (NVMe) is recommended for model weights and PagedAttention page caches. Use instance local SSDs or provisioned NVMe for best performance.
- GPU memory sizing guidance
  - vLLM with PagedAttention can lower the peak GPU memory footprint, but you still need enough aggregate GPU memory to hold the active working set.
  - As a ballpark, for a 13B model in FP16 you may need ~24–48 GiB aggregated GPU memory to get good throughput. For 70B or larger models, aim for multiple A100-class GPUs (80GB) or scale horizontally.

## 3. Deployment Guide (EKS / GKE)

This guide describes deploying a production-ready vLLM server on Kubernetes with multi-GPU support.

Prereqs

- kubectl configured for your cluster
- A GPU node pool with nodes labeled `nvidia.com/gpu=true` (or similar)
- NVIDIA device plugin installed
- A container registry with a vLLM image (we reference a public image in the example)

High-level steps

1. Prepare model artifacts
   - Upload model weights to a fast storage location reachable by the node (e.g., a node-local directory, or pre-pulled into the image). For large models prefer local disk mounted into the Pod.
2. Configure the Kubernetes Deployment
   - Use resources.limits `nvidia.com/gpu` to request multiple GPUs per Pod.
   - Use nodeSelector, tolerations, and podAffinity to keep vLLM Pods on GPU nodes.
   - Mount a high-performance hostPath or PersistentVolume for model weights and page cache.
3. Expose the service
   - Use a Service + Ingress or LoadBalancer to expose the OpenAI-compatible API.
4. Scale and autoscale
   - Use Horizontal Pod Autoscaler carefully; with multi-GPU pods, HPA should be driven by custom metrics (request latency / GPU utilization) and may be combined with Cluster Autoscaler for node scaling.

A production-ready example manifest is included in `code-examples/vllm-k8s/deployment.yaml`.

Notes on memory and paging

- Tune the vLLM server's paging parameters (page size, cache size) so that hot attention pages remain in GPU memory while cold pages are safely paged out to host/NVMe.
- Monitor GPU memory, host memory, and disk I/O to find the optimal balance for your workload.

