#!/bin/bash

which docker
which date
which mkdir
which aws

CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
S3_BUCKET=2030.hex7.com
FILE=scores-${DATE}.json
SAVE_PATH=tmp

echo ensure variables
echo ${CONTAINER} ${S3_BUCKET} ${DATE} ${FILE} ${SAVE_PATH}

echo ensure tmp directory
mkdir -pv ${SAVE_PATH}

echo copy score data out of container
docker cp "${CONTAINER}:/data/${FILE}" "${SAVE_PATH}"

echo ensure data copy out success
cat ${SAVE_PATH}/${FILE}

echo "FILE_NAME=${FILE}" >> $GITHUB_OUTPUT
echo "FILE_PATH=${SAVE_PATH}" >> $GITHUB_OUTPUT
