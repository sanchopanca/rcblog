#!/usr/bin/env bash

killall caddy

docker stop rcblog-web
docker rm rcblog-web

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog
