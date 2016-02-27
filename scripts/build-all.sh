#!/usr/bin/env bash

SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_ROOT="$SCRIPTS_DIR/.."

docker build -t rcblog -f "$SCRIPTS_DIR/Dockerfile" "$APP_ROOT"
docker build -t rcblog-init-db -f "$SCRIPTS_DIR/Dockerfile_init_db" "$APP_ROOT"
docker build -t rcblog-tests -f "$SCRIPTS_DIR/Dockerfile_tests" "$APP_ROOT"
