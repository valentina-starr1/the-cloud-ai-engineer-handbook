AI streaming ingestion Helm chart (ai-data-ingestion)

Overview
This chart is an opinionated blueprint for streaming ingestion components used by AI pipelines. It covers a StatefulSet-based design (for durable offsets/state) and a Deployment variant for stateless workers. The included template is a Deployment with HPA metrics and node affinity; you can extend it to a StatefulSet for Kafka/offset management where ordered, durable storage is required.

Key features
- Resource requests/limits and readiness/liveness probes
- Pod anti-affinity and node affinity for GPU/fast-storage placement
- HPA setup using custom/external metrics (placeholders for Prometheus or KEDA)
- Configurable environment via Helm values

Usage
1. Package or install:
   helm install ai-data-ingestion ./02-k8s-ai-ingestion-helm

2. To enable StatefulSet variant: copy templates/deployment.yaml -> templates/statefulset.yaml and adapt persistentVolumeClaims in values.

Notes
- This chart intentionally keeps templating minimal; you should wire in your metrics (Prometheus adapter or KEDA) for HPA scale-from/scale-to.
- For streaming systems (Kafka or Pulsar), prefer StatefulSets when local offset storage or local persistence is required.
