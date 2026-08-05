# Prometheus & OpenTelemetry LLM Tracking

This module documents metrics and alert rules for tracking LLM performance and GPU saturation.

Key metrics to collect:

- ttft_seconds: Time to first token for LLM responses.
- internal_ttf_latency_seconds (itl): Internal token-level latency for streaming models.
- gpu_vram_usage_bytes: Per-GPU VRAM usage.
- gpu_vram_total_bytes: Total VRAM on the device to compute saturation percentage.

Instrumentation guidance:

- Export OpenTelemetry metrics from model servers (FastAPI, Ray serve, Triton) and scrape with Prometheus.
- Use labels: job, model_name, deployment, gpu_id, instance_type.
- Compute saturation: (gpu_vram_usage_bytes / gpu_vram_total_bytes) * 100.

Prometheus alerts include CUDA OOM detection and sustained latency spikes. See prometheus-rules.yaml for examples.
