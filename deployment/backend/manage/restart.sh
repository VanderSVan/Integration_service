#!/usr/bin/env bash

set -e

cd ../..

# Включаем автоматическое экспортирование переменных
set -a
source "$PWD"/components/backend/.env
cd deployment/backend
# Отключаем автоматическое экспортирование переменных
set +a

case "$1" in
--dev)
  export COMPOSE_PROJECT_NAME=integration-service-dev
  echo "The development containers are restarting ..."
  docker compose -f docker-compose.dev.yml down
  docker compose -f docker-compose.dev.yml up --build --scale task_worker=2
  ;;
*)
  export COMPOSE_PROJECT_NAME=integration-service
  ;;
esac