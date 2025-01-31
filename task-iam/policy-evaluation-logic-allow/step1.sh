#!/bin/zsh

aws iam put-role-policy \
    --role-name cmtr-7e60a31c-iam-pela-iam_role \
    --policy-name cmtr-7e60a31c-allow-list-buckets \
    --policy-document file://allow-list-all-buckets-policy.json

aws s3api put-bucket-policy \
    --bucket cmtr-7e60a31c-iam-pela-bucket-1-8055897 \
    --policy file://bucket-policy.json
