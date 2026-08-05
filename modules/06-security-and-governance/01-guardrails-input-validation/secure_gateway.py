"""
Secure Gateway Example
- FastAPI gateway that validates input text and prevents prompt injection and PII leakage.
- This is an illustrative example and should be hardened for production.
"""
import re
import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import httpx

# Basic PII regex examples (very simplified)
PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN-like
    re.compile(r"\b\d{16}\b"),  # credit-card-like
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),  # email
]

MAX_INPUT_LENGTH = int(os.environ.get("MAX_INPUT_LENGTH", "4000"))

class Query(BaseModel):
    query: str
    request_id: str = "auto"

app = FastAPI()

def contains_pii(text: str) -> bool:
    for p in PII_PATTERNS:
        if p.search(text):
            return True
    return False

def basic_prompt_injection_check(text: str) -> bool:
    # simple heuristics: blocked tokens, system prompt leakage attempts
    blocked = ["ignore previous", "do not follow instructions", "system:"]
    low = text.lower()
    return any(tok in low for tok in blocked)

@app.post('/gateway/query')
async def gateway_query(payload: Query):
    if len(payload.query) > MAX_INPUT_LENGTH:
        raise HTTPException(status_code=413, detail="Input too long")
    if contains_pii(payload.query):
        raise HTTPException(status_code=400, detail="PII detected in input")
    if basic_prompt_injection_check(payload.query):
        raise HTTPException(status_code=400, detail="Possible prompt injection")

    # Forward to downstream LLM service (example)
    llm_url = os.environ.get('LLM_ENDPOINT', 'http://localhost:8000/generate')
    async with httpx.AsyncClient() as client:
        resp = await client.post(llm_url, json={'query': payload.query, 'request_id': payload.request_id}, timeout=30.0)
    return resp.json()
