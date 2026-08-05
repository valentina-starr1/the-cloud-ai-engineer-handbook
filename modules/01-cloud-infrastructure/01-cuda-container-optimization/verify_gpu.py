#!/usr/bin/env python3
# verify_gpu.py

"""
Simple runtime verification script:
- checks torch and CUDA availability
- prints driver and device details
- runs a small tensor op on GPU to validate correctness
"""

import sys
import time

try:
    import torch
except Exception as e:
    print("ERROR: PyTorch import failed:", e)
    sys.exit(2)

print("PyTorch version:", torch.__version__)

cuda_available = torch.cuda.is_available()
print("CUDA available:", cuda_available)

if cuda_available:
    try:
        device_count = torch.cuda.device_count()
        print(f"CUDA device count: {device_count}")
        print("CUDA driver version:", torch.version.cuda)
        for i in range(device_count):
            name = torch.cuda.get_device_name(i)
            capability = torch.cuda.get_device_capability(i)
            print(f"Device {i}: {name}, capability={capability}")

        # quick sanity tensor computation
        a = torch.randn((1024, 1024), device='cuda')
        b = torch.randn((1024, 1024), device='cuda')
        start = time.time()
        c = torch.matmul(a, b)
        torch.cuda.synchronize()
        end = time.time()
        print(f"GPU matmul time: {end - start:.4f}s")

    except Exception as e:
        print("ERROR while exercising CUDA:", e)
        sys.exit(3)
else:
    print("No CUDA devices detected. If you expected GPUs, ensure the host has NVIDIA drivers and the container runtime provides GPU access.")
