#!/bin/bash

which docker
which date
which mkdir
which aws

CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
mkdir -pv tmp/data
docker cp "${CONTAINER}:/data/scores-${DATE}.json" "tmp/data/"
aws s3 cp ./tmp/data/scores-${DATE}.json s3://${S3_BUCKET}/scores-${DATE}.json
