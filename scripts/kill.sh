#!/usr/bin/env bash

docker stop rcblog-web
docker rm rcblog-web

docker stop rethinkdb-rcblog
docker rm rethinkdb-rcblog
