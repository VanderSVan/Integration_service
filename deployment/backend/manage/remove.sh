#!/usr/bin/env bash

set -e

cd ../..

set -a
source "$PWD"/components/backend/.env
set +a

cd deployment/backend

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=integration-service-dev
  echo "The development containers are removing ..."
  docker compose -f docker-compose.dev.yml down
  echo "The development images are removing ..."
  docker rmi \
    integration-service-dev-backend \
    integration-service-dev-task_worker
  ;;
*)
  export COMPOSE_PROJECT_NAME=integration-service
  ;;
esac
