Running Ollama (or similar local model server) as an edge inference service

Overview
This folder contains a production-ready systemd unit (ollama.service) to run a local model inference server and an async streaming client (client_stream.py) to test latency and streaming behavior.

Best practices
- Run the server as a non-root user with resource limits.
- Use systemd's Restart=on-failure and set CPU/memory accounting.
- Expose health endpoints on the server for readiness/liveness.

Usage
1. Copy ollama.service to /etc/systemd/system/ollama.service
2. Reload systemd: sudo systemctl daemon-reload
3. Start and enable: sudo systemctl enable --now ollama.service
4. Run client: python3 client_stream.py --url http://localhost:11434/v1/stream --prompt "Hello world"
