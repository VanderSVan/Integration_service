#!/usr/bin/env bash

set -e

echo "Starting task worker..."
python -m integration_service.launchers.task_worker
