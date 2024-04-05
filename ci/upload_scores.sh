#!/bin/bash -ex


which docker
which date
which mkdir
which aws


CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
S3_BUCKET=2033.hex7.com
FILE_FAST=fast-${DATE}.json
FILE_SLOW=slow-${DATE}.json
SAVE_PATH=tmp


echo ensure variables
echo CONTAINER ${CONTAINER}
echo S3_BUCKET ${S3_BUCKET}
echo DATE ${DATE}
echo FILE_FAST ${FILE_FAST}
echo FILE_SLOW ${FILE_SLOW}
echo SAVE_PATH ${SAVE_PATH}


echo ensure tmp directory
mkdir -pv ${SAVE_PATH}


echo copy score data out of container
docker cp "${CONTAINER}:/data/${FILE_FAST}" "${SAVE_PATH}"
docker cp "${CONTAINER}:/data/${FILE_SLOW}" "${SAVE_PATH}"


echo ensure data copy out success
cat ${SAVE_PATH}/${FILE_FAST}
cat ${SAVE_PATH}/${FILE_SLOW}
echo "FILE_FAST=${FILE_FAST}" >> $GITHUB_OUTPUT
echo "FILE_SLOW=${FILE_SLOW}" >> $GITHUB_OUTPUT
echo "FILE_PATH=${SAVE_PATH}" >> $GITHUB_OUTPUT
