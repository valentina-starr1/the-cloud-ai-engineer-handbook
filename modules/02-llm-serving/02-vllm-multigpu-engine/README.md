vLLM production runtime with PagedAttention and Tensor Parallelism

Overview
This folder documents configuration and a startup launcher for running vLLM with Ray-based tensor parallelism across multiple GPUs (example: 4 GPUs). It covers memory limits, PagedAttention, and how to tune batch sizes and prefetching.

Design notes
- PagedAttention reduces host memory pressure.
- Tensor parallelism shards large layers across GPUs to increase effective model size.
- Use Ray (or other orchestration) to manage worker placement and GPU assignment.

Files
- vllm_config.json: engine configuration for memory and attention
- server_launch.sh: launcher that starts Ray head and runs vllm worker with tensor parallelism
