#!/usr/bin/env python3
"""
Benchmark script comparing regular vs speculative decoding latency.

Assumptions:
- A TGI HTTP endpoint is running at --url which accepts JSON payload:
    {"prompt": "...", "max_new_tokens": 32}
- An optional speculative endpoint at --spec_url supports speculative mode.
"""
import time
import requests
import argparse
import statistics

def single_request(url, payload, timeout=30):
    start = time.time()
    r = requests.post(url, json=payload, timeout=timeout)
    elapsed = time.time() - start
    return elapsed, r

def bench(url, payload, n=10):
    latencies = []
    for i in range(n):
        elapsed, resp = single_request(url, payload)
        if resp.status_code != 200:
            print("Request failed:", resp.status_code, resp.text[:200])
            continue
        latencies.append(elapsed)
    return latencies

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Standard decode endpoint")
    parser.add_argument("--spec_url", required=False, help="Speculative decoding endpoint")
    parser.add_argument("--prompt", default="Write a short summary of the industrial revolution.")
    parser.add_argument("--n", type=int, default=10)
    args = parser.parse_args()

    payload = {"prompt": args.prompt, "max_new_tokens": 32}
    print("Benchmarking standard decode...")
    std = bench(args.url, payload, n=args.n)
    if len(std) > 0:
        print("Standard decode: n=", len(std), "median=", statistics.median(std))
    else:
        print("Standard decode: no successful requests")
    if args.spec_url:
        print("Benchmarking speculative decode...")
        spec = bench(args.spec_url, payload, n=args.n)
        if len(spec) > 0:
            print("Speculative decode: n=", len(spec), "median=", statistics.median(spec))
        else:
            print("Speculative decode: no successful requests")

if __name__ == "__main__":
    main()
