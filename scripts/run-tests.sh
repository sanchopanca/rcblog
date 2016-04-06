#!/usr/bin/env bash

docker run -d \
    --name rethinkdb-rcblog \
    rethinkdb:2

sleep 10

docker run --rm \
    -it \
    --name rcblog-web \
    --link rethinkdb-rcblog \
     rcblog \
     python3 -m unittest -v

RESULT=$?

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog

exit "$RESULT"