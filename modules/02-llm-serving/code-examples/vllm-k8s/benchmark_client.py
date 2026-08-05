#!/usr/bin/env python3
"""
benchmark_client.py

Asynchronous benchmark client that exercises an OpenAI-compatible vLLM endpoint
by issuing concurrent /v1/completions requests and measuring tokens/sec throughput.

Requirements:
  pip install aiohttp

Usage:
  python benchmark_client.py --url http://vllm.example.com:8080/v1/completions --concurrency 8 --requests 100
"""

import argparse
import asyncio
import time
from typing import Dict

import aiohttp

DEFAULT_PROMPT = "Hello, please summarize the following text: The quick brown fox jumps over the lazy dog."

async def send_request(session: aiohttp.ClientSession, url: str, prompt: str, timeout: int = 30) -> Dict:
    payload = {
        "model": "my-model",
        "prompt": prompt,
        "max_tokens": 64,
        "temperature": 0.0,
    }
    async with session.post(url, json=payload, timeout=timeout) as resp:
        resp.raise_for_status()
        return await resp.json()


async def worker(name: int, url: str, prompt: str, requests_per_worker: int, results: list):
    conn = aiohttp.TCPConnector(limit=0)
    async with aiohttp.ClientSession(connector=conn) as session:
        for i in range(requests_per_worker):
            start = time.perf_counter()
            try:
                res = await send_request(session, url, prompt)
                elapsed = time.perf_counter() - start
                # Try to extract token usage if the server provides it; otherwise estimate by output length
                tokens = 0
                if isinstance(res, dict):
                    # OpenAI-compatible servers often return choices[0].text or choices[0].message
                    choices = res.get("choices") or []
                    if choices:
                        txt = choices[0].get("text") or choices[0].get("message", {}).get("content", "")
                        tokens = len(txt.split())
                results.append((elapsed, tokens))
            except Exception as e:
                results.append((None, 0))
                print(f"worker-{name} request {i} failed: {e}")


async def run_benchmark(url: str, prompt: str, concurrency: int, total_requests: int):
    requests_per_worker = total_requests // concurrency
    results = []
    tasks = [worker(i, url, prompt, requests_per_worker, results) for i in range(concurrency)]
    start = time.perf_counter()
    await asyncio.gather(*tasks)
    total_time = time.perf_counter() - start

    # Aggregate
    completed = [r for r in results if r[0] is not None]
    failed = [r for r in results if r[0] is None]
    total_tokens = sum(r[1] for r in completed)
    total_requests_done = len(completed)
    avg_latency = sum(r[0] for r in completed) / total_requests_done if total_requests_done else float('nan')
    throughput_rps = total_requests_done / total_time if total_time > 0 else float('nan')
    throughput_tps = total_tokens / total_time if total_time > 0 else float('nan')

    print("\nBenchmark Results")
    print("-----------------")
    print(f"Total requests sent: {total_requests}")
    print(f"Completed requests: {total_requests_done}")
    print(f"Failed requests: {len(failed)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Avg latency (s): {avg_latency:.3f}")
    print(f"Requests/sec: {throughput_rps:.2f}")
    print(f"Tokens/sec (est): {throughput_tps:.2f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="vLLM completions endpoint URL, e.g. http://host:8080/v1/completions")
    parser.add_argument("--concurrency", type=int, default=8, help="Number of concurrent workers")
    parser.add_argument("--requests", type=int, default=200, help="Total number of requests to send")
    parser.add_argument("--prompt", type=str, default=DEFAULT_PROMPT)
    args = parser.parse_args()

    asyncio.run(run_benchmark(args.url, args.prompt, args.concurrency, args.requests))


if __name__ == "__main__":
    main()
