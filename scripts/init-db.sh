#!/usr/bin/env bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./init.sh username password"
    exit 1
fi

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
     python3 init.py "$1" "$2"

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog