#!/usr/bin/env bash

docker run -d \
    --name rethinkdb-rcblog \
    rethinkdb:2

sleep 5

docker run --rm \
    -it \
    --name rcblog-web \
    --link rethinkdb-rcblog \
     rcblog \
     python3 -m unittest -v

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog
