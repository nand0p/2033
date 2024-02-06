#!/bin/bash

which docker
which date
which mkdir
which aws

CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
S3_BUCKET=2030.hex7.com
FILE=scores-${DATE}.json

echo ensure variables
echo ${CONTAINER} ${S3_BUCKET} ${DATE} ${FILE}

echo ensure tmp directory
mkdir -pv tmp/data

echo copy score data out of container
docker cp "${CONTAINER}:/data/${FILE}" "tmp/data/"

echo ensure data copy out success
cat tmp/data/${FILE}

echo "FILE=./tmp/data/${FILE}" >> $GITHUB_OUTPUT
