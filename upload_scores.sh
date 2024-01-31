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
find ./data/
docker cp "${CONTAINER}:/data/scores-${DATE}.json" "tmp/data/"
find ./tmp/
#aws s3 cp ./tmp/data/scores-${DATE}.json s3://${S3_BUCKET}/scores-${DATE}.json
