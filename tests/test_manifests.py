import os
import json

def validate_manifest(path: str) -> bool:
    # Naive validator: check that JSON or YAML files exist and are non-empty
    try:
        with open(path, 'r') as f:
            content = f.read().strip()
            return len(content) > 0
    except Exception:
        return False

if __name__ == '__main__':
    # Example usage: validate top-level module manifests
    repo_root = os.path.dirname(os.path.dirname(__file__))
    sample_paths = [
        os.path.join(repo_root, 'modules', '05-observability', '02-grafana-ai-dashboard', 'dashboard.json'),
    ]
    for p in sample_paths:
        print(p, 'OK' if validate_manifest(p) else 'MISSING')
