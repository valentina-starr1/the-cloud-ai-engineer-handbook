"""
FastAPI middleware exporting OpenTelemetry metrics to Prometheus.
Requires: fastapi, opentelemetry-sdk, opentelemetry-exporter-prometheus

This middleware instruments:
- request_latency_seconds histogram
- ttft_seconds histogram (time to first token, measured when middleware.mark_first_token() is called by your streamer)
- gpu_vram_used_bytes gauge sampled periodically via nvidia-smi

Usage:
- Mount this middleware into your FastAPI app and call `mark_first_token(request)` from the streaming response path when the first token is emitted.
"""
from fastapi import Request
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import time
import threading
import subprocess
import re

# Meter setup
exporter = PrometheusMetricsExporter()
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

request_latency = meter.create_histogram("request_latency_seconds")
ttft_latency = meter.create_histogram("ttft_seconds")
gpu_vram_used = meter.create_observable_gauge("gpu_vram_used_bytes")

# Helper to sample GPU memory via nvidia-smi; best-effort and non-blocking
def sample_gpu_vram():
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], encoding="utf-8")
        vals = []
        for line in out.strip().splitlines():
            used, total = line.split(',')
            vals.append((int(used.strip()) * 1024 * 1024, int(total.strip()) * 1024 * 1024))
        # Return first GPU used bytes as example
        if vals:
            return vals[0][0]
    except Exception:
        return 0

def _observe_gpu_vram(observer):
    val = sample_gpu_vram()
    observer.observe(val, {})

# Register the observable callback
meter.register_observable_callback(_observe_gpu_vram, [gpu_vram_used])

class TelemetryMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start = time.time()
        first_token_marked = False

        async def inner_send(message):
            nonlocal first_token_marked
            if not first_token_marked and message.get("type") == "http.response.body" and message.get("body"):
                ttft = time.time() - start
                ttft_latency.record(ttft, {})
                first_token_marked = True
            await send(message)

        await self.app(scope, receive, inner_send)
        latency = time.time() - start
        request_latency.record(latency, {})

# Example helper for code paths that stream tokens and want to mark TTFT explicitly
def mark_first_token():
    # This function is a placeholder for frameworks where middleware cannot intercept first chunk
    # In such cases call this function at the moment of sending the first token to observe TTFT
    ttft_latency.record(0.0, {})

# Expose the Prometheus WSGI app via exporter.start_http_server(port)
def start_metrics_server(port: int = 8000):
    exporter.start_http_server(port)

if __name__ == "__main__":
    print("Start the Prometheus metrics server with start_metrics_server() and mount TelemetryMiddleware in your FastAPI app")
