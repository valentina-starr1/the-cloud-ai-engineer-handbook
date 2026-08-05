from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import multiprocess
import time
import os

# Simple Prometheus metrics exported by middleware
registry = CollectorRegistry(auto_describe=False)
TTFT = Gauge('llm_ttft_seconds', 'Time to first token', ['model', 'deployment'], registry=registry)
ITL = Gauge('llm_internal_token_latency_seconds', 'Internal token latency', ['model', 'deployment'], registry=registry)
GPU_VRAM_USAGE = Gauge('gpu_vram_usage_bytes', 'GPU VRAM usage in bytes', ['gpu_id', 'instance'], registry=registry)
GPU_VRAM_TOTAL = Gauge('gpu_vram_total_bytes', 'GPU VRAM total in bytes', ['gpu_id', 'instance'], registry=registry)

class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Attach start time for request-level TTFT collection
        request.state._start_time = time.time()
        # Continue to handler
        response = await call_next(request)
        # If a header is set by the app indicating first token time, record it
        try:
            first_token_time = float(response.headers.get('X-First-Token-Time', '0'))
        except Exception:
            first_token_time = 0.0
        model = request.headers.get('x-model-name', 'unknown')
        deployment = request.headers.get('x-deployment', 'unknown')
        if first_token_time > 0:
            TTFT.labels(model=model, deployment=deployment).set(first_token_time)
        # Add GPU metrics if present in response headers (apps or exporters may set these)
        try:
            gpu_usage = int(response.headers.get('X-GPU-VRAM-Usage', '0'))
            gpu_total = int(response.headers.get('X-GPU-VRAM-Total', '0'))
            gpu_id = response.headers.get('X-GPU-ID', 'gpu0')
            instance = os.environ.get('HOSTNAME', 'unknown')
            if gpu_total > 0:
                GPU_VRAM_USAGE.labels(gpu_id=gpu_id, instance=instance).set(gpu_usage)
                GPU_VRAM_TOTAL.labels(gpu_id=gpu_id, instance=instance).set(gpu_total)
        except Exception:
            pass
        return response

# Expose a Prometheus scrape endpoint that merges with the global collector
from fastapi import APIRouter
router = APIRouter()

@router.get('/metrics')
async def metrics():
    # In multiprocess setups, use the PROMETHEUS_MULTIPROC_DIR mechanism externally
    output = generate_latest(registry)
    return Response(content=output, media_type=CONTENT_TYPE_LATEST)
