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
    -p 5000:5000 --link rethinkdb-rcblog \
    --restart=always \
     rcblog
