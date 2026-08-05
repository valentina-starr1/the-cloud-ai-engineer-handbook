# Guardrails: Input Validation and Security

This module explains patterns to prevent prompt injection, PII leakage, and toxicity in production LLM systems. It includes a sample Guardrails AI XML schema and a secure gateway that validates inputs before forwarding to model endpoints.

Key practices:

- Strict input schema validation (length, allowed characters, no control sequences).
- Sensitive-data detectors (PII regex checks) and token filtering.
- Output structure enforcement using guardrail schemas and post-processing.
- Rate limit and consent checks at the gateway.

See rail_spec.xml for a sample Guardrails schema and secure_gateway.py for an example FastAPI gateway enforcing validation.
