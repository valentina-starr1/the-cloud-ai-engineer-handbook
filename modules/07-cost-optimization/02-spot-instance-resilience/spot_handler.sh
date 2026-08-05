#!/usr/bin/env bash
# spot_handler.sh
# Simple script polling the AWS Spot interruption notice endpoint and triggering a graceful shutdown hook.

METADATA_URL="http://169.254.169.254/latest/meta-data/spot/instance-action"
HOOK_URL="http://localhost:8080/shutdown-hook"  # Example local hook

while true; do
  # Query IMDS v1 endpoint for spot termination action. If 200, the body contains the action and time.
  response=$(curl -s -o /dev/null -w "%{http_code}" $METADATA_URL || true)
  if [ "$response" == "200" ]; then
    echo "Spot interruption detected, calling shutdown hook"
    # Attempt to notify the local process to checkpoint and exit
    curl -s -X POST $HOOK_URL || true
    # Sleep a bit to avoid tight loop, but keep checking until termination
    sleep 5
  fi
  sleep 10
done
