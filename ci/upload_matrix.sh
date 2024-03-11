#!/bin/bash -ex


which docker
which date
which mkdir
which aws


CONTAINER=$(docker ps --latest --format {{.ID}})
S3_BUCKET=2030.hex7.com
SAVE_FILE=scores_matrix.json
SAVE_PATH=tmp


echo ensure variables
echo CONTAINER ${CONTAINER}
echo S3_BUCKET ${S3_BUCKET}
echo SAVE_FILE ${SAVE_FILE}
echo SAVE_PATH ${SAVE_PATH}


echo ensure tmp directory
mkdir -pv ${SAVE_PATH}


echo copy score data out of container
docker cp "${CONTAINER}:/static/${SAVE_FILE}" "${SAVE_PATH}"


echo ensure data copy out success
cat ${SAVE_PATH}/${SAVE_FILE}

echo upload to s3
aws s3 cp ${SAVE_PATH}/${SAVE_FILE} s3://${S3_BUCKET}/${SAVE_FILE}

echo set acl
aws s3api put-object-acl --bucket 2030.hex7.com --key ${SAVE_FILE} --acl public-read
