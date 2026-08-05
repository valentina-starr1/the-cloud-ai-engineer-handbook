Hugging Face Text Generation Inference (TGI) with speculative decoding

Overview
This module documents a Docker Compose setup to run Hugging Face TGI with model cache volumes and GPU allocation, plus a benchmark script that compares standard decoding to speculative decoding endpoints.

Notes
- Speculative decoding requires a TGI or model server implementation that supports early token proposals and rescoring.
- The benchmark compares round-trip latency across multiple requests to show tradeoffs.

Usage
- docker compose -f tgi-docker-compose.yml up --build
- python benchmark_tgi.py --url http://localhost:8080/generate
