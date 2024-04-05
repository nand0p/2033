#!/bin/bash -ex


aws s3 mb s3://2033.hex7.com/slow/
aws s3 cp ./ci/touch s3://2033.hex7.com/slow/touch
aws s3 ls s3://2033.hex7.com/slow/

aws s3 mb s3://2033.hex7.com/fast/
aws s3 cp ./ci/touch s3://2033.hex7.com/slow/touch
aws s3 ls s3://2033.hex7.com/fast/

aws s3 ls s3://2033.hex7.com

aws s3api put-object-acl --bucket 2033.hex7.com --key /slow/touch --acl public-read
aws s3api put-object-acl --bucket 2033.hex7.com --key /fast/touch --acl public-read
