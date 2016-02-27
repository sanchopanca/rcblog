#!/usr/bin/env bash

docker build -t rcblog .
docker build -t rcblog-init-db -f Dockerfile_init_db .
docker build -t rcblog-tests -f Dockerfile_tests .
