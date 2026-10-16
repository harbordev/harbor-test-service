#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=== Simulating Local Harbor Deployment ==="
IMAGE_TAG="${1:-latest}"

echo "1. Building Docker image: harbor-test-service:$IMAGE_TAG"
docker build -t "harbor-test-service:$IMAGE_TAG" .

echo "2. Running container test on port 8000"
docker compose up -d

echo "3. Waiting for health check..."
for i in {1..15}; do
  if curl -s http://localhost:8000/health/live | grep -q "alive"; then
    echo "Service is healthy and live!"
    break
  fi
  echo "Waiting... ($i/15)"
  sleep 1
done

echo "4. Testing /api/v1/info endpoint"
curl -s http://localhost:8000/api/v1/info | jq . || curl -s http://localhost:8000/api/v1/info

echo ""
echo "=== Simulation Completed Successfully ==="
