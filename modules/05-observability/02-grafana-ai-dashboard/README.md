# Grafana AI Infrastructure Dashboard

This dashboard provides a real-time view into GPU cluster health and model server performance. Key panels:

- GPU Utilization: per-GPU usage percentage and temperature.
- GPU VRAM: usage vs total to show saturation.
- Model Request Queue Depth: measure of pending inference requests.
- TTFT and ITL timeseries and percentiles.
- Error Rates and OOM restarts.

Import the included dashboard.json into Grafana or provision using the datasource.yaml provisioning file.
