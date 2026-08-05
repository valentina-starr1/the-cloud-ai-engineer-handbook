# Spot Instance Resilience & Model Checkpointing

Patterns for surviving AWS spot interruptions during training and long-running tasks. Key ideas:

- Listen for the EC2 Instance Metadata Service (IMDS) termination notice.
- Gracefully checkpoint model state and upload to durable storage (S3, GCS) within the two-minute window.
- Use incremental checkpoints and atomic renames to avoid partial uploads.
- Resume logic should detect the most recent complete checkpoint.

Included:
- spot_handler.sh: lightweight shell watcher for AWS termination notices.
- checkpoint_manager.py: Python module to upload checkpoints to S3 on SIGTERM/SIGINT.
