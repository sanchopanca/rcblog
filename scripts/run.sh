#!/usr/bin/env bash

mkdir -p /srv/rethinkd-data

docker run -d \
    --name rethinkdb-rcblog \
    -v /srv/rethink-data:/data \
    --restart=always \
    rethinkdb:2

sleep 5

docker run -d \
    --name rcblog-web \
    -p 8000:8000 --link rethinkdb-rcblog \
    --restart=always \
     rcblog

nohup caddy -conf etc/Caddyfile &
