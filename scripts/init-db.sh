#!/usr/bin/env bash

mkdir -p /srv/rethinkd-data

docker run -d \
    -v /srv/rethink-data:/data \
    --name rethinkdb-rcblog \
    rethinkdb:2

sleep 5

docker run --rm \
    -it \
    --name rcblog-web \
    --link rethinkdb-rcblog \
     rcblog \
     python3 init.py

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog