#!/bin/bash -ex


which docker
which date
which mkdir
which aws


CONTAINER=$(docker ps --latest --format {{.ID}})
DATE=$(date +%Y-%m-%d)
S3_BUCKET=2030.hex7.com
S3_PREFIX=scores
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


echo make scores s3 directory
if ! aws s3 ls s3://${S3_BUCKET}/${S3_PREFIX}; then
  aws s3 mb s3://${S3_BUCKET}/${S3_PREFIX} --output text
  aws s3api put-object-acl --bucket ${S3_BUCKET} \
                           --key ${S3_PREFIX} \
                           --acl public-read \
                           --output text
else
  echo s3://${S3_BUCKET}/${S3_PREFIX} exists
fi


echo uploading scores file
aws s3 cp ${SAVE_PATH}/${FILE} s3://${S3_BUCKET}/${S3_PREFIX}/${FILE}

echo test upload success
aws s3 ls s3://${S3_BUCKET}/${S3_PREFIX}/${FILE}

echo put scores file acl
aws s3api put-object-acl --bucket ${S3_BUCKET} \
                         --key ${S3_PREFIX}/${FILE} \
                         --acl public-read \
                         --output text
