#!/bin/bash -ex


DOWNLOAD_SITE=1
S3_BUCKET=2030.hex7.com


echo "run 2030 docker container"
bash run.sh


echo "make bucket and set policy"
if aws s3 ls "s3://$S3_BUCKET" 2>&1 | grep -q 'NoSuchBucket'; then
  aws s3api create-bucket --bucket ${S3_BUCKET} --object-ownership BucketOwnerPreferred
  aws s3api delete-public-access-block --bucket ${S3_BUCKET}
  aws s3api put-bucket-policy --bucket ${S3_BUCKET} --policy file://s3_bucket_policy.json
fi

echo "make temp directory"
rm -rf tmp
mkdir -pv tmp
cd tmp


echo "download html and images"
if [ "${DOWNLOAD_SITE}" == "1" ]; then
  wget --recursive --level 2 --no-clobber --page-requisites --adjust-extension --convert-links localhost
fi


echo "upload to s3 static website"
aws s3 cp --recursive --acl public-read ./localhost/ s3://${S3_BUCKET}/ 
aws s3 website s3://${S3_BUCKET} --index-document index.html


echo "kill 2030 docker container"
cd ..
bash kill.sh
