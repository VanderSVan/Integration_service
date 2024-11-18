#!/usr/bin/env bash

set -e

/usr/bin/entrypoint_alembic.sh

if [ -z "$API_PORT" ]; then
  API_PORT=8000
fi

if [ -z "$API_LOG_LEVEL" ]; then
  API_LOG_LEVEL=info
fi

if [ -z "$API_ENV" ]; then
  API_ENV="production"
fi

if [ -z "$API_WORKER_COUNT" ]; then
  API_WORKER_COUNT=4
fi

echo
echo "API_PORT: ${API_PORT}"
echo "API_WORKER_COUNT: ${API_WORKER_COUNT}"
echo

uvicorn integration_service.launchers.api:app \
    --host 0.0.0.0 \
    --port "${API_PORT}" \
    --log-level "${API_LOG_LEVEL}" \
    --workers 4 \
    --timeout-keep-alive 1200


