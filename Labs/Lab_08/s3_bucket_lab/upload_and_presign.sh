#!/bin/bash

FILE=$1
BUCKET=$2
EXP=$3

# Upload file to S3
aws s3 cp "$FILE" "s3://$BUCKET/"

# Generate presigned URL
aws s3 presign "s3://$BUCKET/$FILE" --expires-in "$EXP"