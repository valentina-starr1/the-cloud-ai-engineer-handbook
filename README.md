# The Cloud AI Engineer Handbook

A comprehensive, open-source reference guide, architectural blueprint, and hands-on code curriculum for building, scaling, and deploying production-grade AI infrastructure on cloud-native platforms.

Key features

- Practical, end-to-end learning modules covering the full AI infrastructure lifecycle
- Hands-on examples, deployment templates, and reproducible labs
- Open-source community contributions, reviewable patterns, and battle-tested reference architectures
- Focus on production readiness: scalability, reliability, security, and cost efficiency

Learning Map

Below is a high-level map of the six core learning modules in this handbook.

```
+-------------------------------------------------------------+
|                  The Cloud AI Engineer Handbook             |
|                                                             |
|  [01] Cloud-Native Infrastructure & Containerization         |
|    - Docker, Kubernetes, Helm                               |
|                             |                               |
|  [02] LLM Serving & Acceleration    <--->   [03] Vector DBs  |
|    - vLLM, Ollama, TensorRT-LLM         - Qdrant, Milvus,    |
|                                           PGVector            |
|                             |                               |
|  [04] Distributed Training & Fine-Tuning Pipelines          |
|    - Ray, DeepSpeed                                         |
|                             |                               |
|  [05] AI Observability & Monitoring                         |
|    - Prometheus, Grafana, OpenTelemetry                     |
|                             |                               |
|  [06] Security, Auth & Cost Optimization in AI Workloads    |
+-------------------------------------------------------------+
```

Modules index (quick links)

- Module 01: modules/01-cloud-infrastructure/README.md
- Module 02: modules/02-llm-serving/README.md
- Module 03: modules/03-vector-databases/README.md
- Module 04: modules/04-distributed-training/README.md
- Module 05: modules/05-observability/README.md
- Module 06: modules/06-security-costs/README.md

Contribution Guidelines

We welcome community contributions. To keep the handbook high-quality, please follow these guidelines:

1. Code of conduct
   - Please follow a respectful, inclusive Code of Conduct (see CODE_OF_CONDUCT.md if present). Treat fellow contributors with respect.

2. How to contribute
   - Open an issue to discuss large changes or new module content before submitting a major pull request.
   - For small edits (typos, improvements), submit a pull request directly against the default branch.

3. Branches and commits
   - Create feature branches from the repository's default branch with a descriptive name: `feat/`, `fix/`, `docs/`, `chore/` prefixes are recommended.
   - Use Conventional Commits for messages. Example: `feat(init): build master architecture layout and modules index`.

4. Pull requests
   - Provide a clear PR description that summarizes the change, motivation, and any breaking impacts.
   - Link related issues using `Fixes #<issue-number>` when the PR resolves an issue.
   - Keep PRs focused and small where possible; large content additions should be split into smaller, reviewable PRs.

5. Documentation and content
   - Write clear, actionable guides and include runnable examples when possible.
   - Add diagrams, architecture sketches, and code snippets to illustrate concepts.
   - New modules should include a top-level README, learning objectives, prerequisites, and at least one hands-on lab or example.

6. Review and testing
   - All PRs must include CI checks where appropriate (linting, link-checks, or test runs).
   - Reviewers will verify clarity, correctness, and reproducibility. Address review comments promptly.

7. Licensing
   - Ensure contributed code and assets are compatible with this repo's license. If in doubt, open an issue for clarification.

Maintainers

- If you want to become a maintainer or take ownership of a module, open an issue describing your background and proposed responsibilities.

License

This repository is community-owned. Add or verify the LICENSE file in a follow-up change if needed.
