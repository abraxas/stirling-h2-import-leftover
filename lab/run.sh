#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-stirling-h2-import-leftover}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="stirling-h2-import-leftover"
WITNESS="STIRLING-H2-IMPORT-WITNESS"
IMAGE_DEFAULT="stirlingtools/stirling-pdf:3.2.0-fat"
IMAGE_FALLBACKS=(
  "stirlingtools/stirling-pdf:3.2.0-fat"
  "docker.stirlingpdf.com/stirlingtools/stirling-pdf:3.2.0-fat"
)

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=120 stirling-pdf || true
  down
  exit 1
}

pick_image() {
  local img
  if [[ -n "${STIRLING_IMAGE:-}" ]]; then
    echo "== docker pull ${STIRLING_IMAGE} =="
    docker pull "${STIRLING_IMAGE}" || fail_setup "image-pull-failed"
    return
  fi
  for img in "${IMAGE_FALLBACKS[@]}"; do
    echo "== docker pull ${img} =="
    if docker pull "${img}"; then
      export STIRLING_IMAGE="${img}"
      return
    fi
    echo "IOC image-pull-miss ${img}"
  done
  fail_setup "image-pull-failed"
}

trap down EXIT

echo "== docker compose down (clean) =="
down

pick_image
export STIRLING_IMAGE="${STIRLING_IMAGE:-${IMAGE_DEFAULT}}"
echo "IOC image=${STIRLING_IMAGE}"

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 8); do
  if STIRLING_IMAGE="${STIRLING_IMAGE}" docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait GET /api/v1/info/status UP =="
ready=0
for i in $(seq 1 240); do
  code="$(curl -sS -o /tmp/stirling-h2-import-status.txt -w '%{http_code}' --max-time 8 \
    "http://127.0.0.1:18152/api/v1/info/status" || true)"
  if [[ "${code}" == "200" ]] && grep -q 'UP' /tmp/stirling-h2-import-status.txt; then
    ready=1
    echo "IOC stirling-ready attempt=${i} status=${code}"
    break
  fi
  echo "IOC stirling-wait attempt=${i} status=${code}"
  sleep 5
done
if [[ "${ready}" != 1 ]]; then
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 stirling-pdf || true
  fail_setup "stirling-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
