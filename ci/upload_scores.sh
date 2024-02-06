#!/bin/bash

which docker
which date
which mkdir
which aws

CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
S3_BUCKET=2030.hex7.com

echo ensure variables
echo ${CONTAINER} ${S3_BUCKET} ${DATE}

echo ensure tmp directory
mkdir -pv tmp/data

echo copy score data out of container
docker cp "${CONTAINER}:/data/scores-${DATE}.json" "tmp/data/"

echo ensure data copy out success
cat tmp/data/scores-${DATE}.json

echo copy score data to s3
aws s3 cp ./tmp/data/scores-${DATE}.json s3://${S3_BUCKET}/scores-${DATE}.json

echo test s3 file exists
aws s3 ls s3://${S3_BUCKET}

