# CUDA Multi-Stage Container Runtime

This folder contains a multi-stage Dockerfile optimized for building PyTorch with CUDA 12.x and a short guide for setting up the NVIDIA Container Toolkit so the resulting container can access GPUs on host systems.

Contents
- Dockerfile.gpu — multi-stage Dockerfile pinned to CUDA 12.x and PyTorch CUDA wheels
- verify_gpu.py — small runtime check for PyTorch and CUDA driver access

Recommendations
- Use NVIDIA drivers matching CUDA 12.x on the host and install the nvidia-container-toolkit so containers can access GPUs.
- Use the `--gpus` flag with Docker or run on a runtime that supports GPU passthrough (e.g. containerd with nvidia-container-runtime).

Quick test
1. Build the image:

   docker build -t cuda-pytorch:12 -f Dockerfile.gpu .

2. Run with GPU access:

   docker run --gpus all --rm -it cuda-pytorch:12 python verify_gpu.py

Notes on image size and layers
- The multi-stage approach builds only what is required and reduces final image size by excluding build dependencies.
- Pin versions to reproducible PyTorch releases and update the PyTorch index URL to match the chosen CUDA minor version.
