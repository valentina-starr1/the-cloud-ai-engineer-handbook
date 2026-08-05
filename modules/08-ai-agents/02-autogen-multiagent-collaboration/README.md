# AutoGen Multi-Agent Collaboration

This module demonstrates an architecture for multiple autonomous agents collaborating to solve engineering tasks. It includes configuration for agent roles, system prompts, and a simple Python runner to simulate agent dialogues.

Principles:

- Define clear roles and tool access per agent (e.g., UserProxyAgent, AssistantAgent, CoderAgent).
- Use message channels with provenance and rate limits.
- Restrict tool invocation to authorized agents and audit all tool outputs.
