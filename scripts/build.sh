#!/usr/bin/env bash

SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_ROOT="$SCRIPTS_DIR/.."

docker build -t rcblog -f "$SCRIPTS_DIR/Dockerfile" "$APP_ROOT"
