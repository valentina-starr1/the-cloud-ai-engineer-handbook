#!/usr/bin/env python3
"""
Async HTTP streaming client to consume server-sent tokens and measure latency.

Usage:
  python client_stream.py --url http://localhost:11434/v1/stream --prompt "The quick brown fox"
"""
import asyncio
import aiohttp
import time
import argparse
from typing import AsyncGenerator

async def stream_completion(session: aiohttp.ClientSession, url: str, prompt: str):
    payload = {"prompt": prompt, "stream": True}
    start = time.time()
    async with session.post(url, json=payload) as resp:
        if resp.status != 200:
            text = await resp.text()
            raise RuntimeError(f"Server returned {resp.status}: {text}")
        token_count = 0
        async for raw in resp.content:
            t = time.time()
            elapsed = t - start
            chunk = raw.decode(errors='ignore')
            token_count += 1
            print(f"[{elapsed:.3f}s] chunk: {chunk.strip()}")
        total = time.time() - start
        print(f"Completed stream, tokens/chunks: {token_count}, total time: {total:.3f}s")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--prompt", required=True)
    args = parser.parse_args()
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
        await stream_completion(session, args.url, args.prompt)

if __name__ == "__main__":
    asyncio.run(main())
