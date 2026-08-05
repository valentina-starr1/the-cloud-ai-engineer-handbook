# Karpenter GPU Autoscaling on AWS

This guide describes how to configure Karpenter to provision GPU-backed nodes on AWS. The objective is scale-to-zero when no GPU workloads are present and scale up quickly for bursty inference/training.

Key points:

- Use provisioner with instanceSelector to prefer GPU instance types (e.g., p4d, g5) and spot vs on-demand pools.
- Configure consolidation and TTL to allow scale-to-zero.
- Set taints/tolerations to isolate GPU workloads.

See provisioner.yaml for an example Karpenter Provisioner manifest and test_scale_workload.yaml for a deployment that requests GPUs to force scaling.
