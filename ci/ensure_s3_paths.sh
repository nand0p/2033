#!/bin/bash

aws s3 ls s3://2030.hex7.com
aws s3 mb s3://2030.hex7.com/slow
aws s3 ls s3://2030.hex7.com/slow
aws s3 mb s3://2030.hex7.com/fast
aws s3 ls s3://2030.hex7.com/fast

aws s3api put-object-acl --bucket 2030.hex7.com --key /slow --acl public-read
aws s3api put-object-acl --bucket 2030.hex7.com --key /fast --acl public-read
