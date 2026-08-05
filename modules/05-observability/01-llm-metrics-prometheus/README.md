LLM metrics tracking with Prometheus and OpenTelemetry

This module explains how to track key LLM metrics:
- TTFT: Time To First Token — measured from request arrival until first token is produced
- ITL: Inference Token Latency — per-token latency
- GPU VRAM saturation: sampled via nvidia-smi when available

Files
- prometheus-rules.yaml: sample Prometheus alert rules for CUDA OOM and latency spikes
- telemetry_middleware.py: FastAPI middleware that instruments requests and exports Prometheus metrics via OpenTelemetry

Usage
- Deploy a Prometheus server scraping /metrics from your FastAPI app.
- Use the provided Prometheus rules to alert on high latency or GPU memory saturation.
