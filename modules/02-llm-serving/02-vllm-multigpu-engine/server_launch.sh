#!/usr/bin/env bash
# Launcher script to initialize a Ray cluster and start vLLM with tensor parallelism across 4 GPUs.
set -euo pipefail

NUM_GPUS=4
RAY_HEAD_PORT=6379
RAY_TEMP_DIR="/tmp/ray_vllm"

# Start Ray head (local single-machine cluster)
echo "Starting Ray head..."
ray stop || true
ray start --head --port=${RAY_HEAD_PORT} --local-mode=false --include-dashboard false --temp-dir ${RAY_TEMP_DIR}
sleep 2

# Start a vLLM worker process pinned to all GPUs using ray for placement.
# This example assumes vllm has a CLI entrypoint `vllm.serve` that accepts ray/tensor-parallel options.
CONFIG_FILE="$(dirname "$0")/vllm_config.json"

echo "Launching vLLM with Ray tensor parallelism (num_gpus=${NUM_GPUS})..."
python3 - <<PY
import subprocess, json, os, sys
cfg = json.load(open("${CONFIG_FILE}"))
print("Loaded config:", cfg["engine"]["paged_attention"])
# Launch pattern: start multiple ray actors, each bound to a GPU, and use a coordinator to route requests.
# This is a best-practice starter script; production orchestration should use a K8s-based Ray operator.
cmd = [
    "python3", "-m", "vllm.server", 
    "--config", "${CONFIG_FILE}",
    "--ray", "true",
    "--num-gpus", str(${NUM_GPUS})
]
print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
PY

echo "vLLM launch complete. Check logs for runtime diagnostics."
