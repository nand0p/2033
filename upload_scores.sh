#!/bin/bash

which docker
which date
which mkdir
which aws

CONTAINER=$(docker ps --latest --format {{.ID}})
echo $CONTAINER
DATE=$(date +%Y-%m-%d)
echo $DATE
mkdir -pv tmp/data
docker cp "${CONTAINER}:/data/scores-${DATE}.json" "tmp/data/"
find ./tmp/
