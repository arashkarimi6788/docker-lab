#!/usr/bin/env bash
# Smoke test for the running stack: /health, POST /items, GET /items.
# Usage: scripts/smoke_test.sh [base_url]   (default http://localhost:5000)
set -euo pipefail

BASE_URL="${1:-http://localhost:5000}"

echo "Waiting for app at $BASE_URL ..."
for i in $(seq 1 30); do
  if curl -fsS "$BASE_URL/health" >/dev/null 2>&1; then
    echo "App is up (after ${i}s)"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "App did not become healthy in 30s" >&2
    exit 1
  fi
  sleep 1
done

echo "--- GET /health"
health=$(curl -fsS "$BASE_URL/health")
echo "$health"
echo "$health" | grep -q '"status": *"ok"'

echo "--- POST /items"
name="ci-test-$(date +%s)"
created=$(curl -fsS -X POST "$BASE_URL/items" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$name\"}")
echo "$created"
echo "$created" | grep -q "\"name\": *\"$name\""

echo "--- GET /items"
items=$(curl -fsS "$BASE_URL/items")
echo "$items"
echo "$items" | grep -q "\"$name\""

echo "All smoke tests passed."
