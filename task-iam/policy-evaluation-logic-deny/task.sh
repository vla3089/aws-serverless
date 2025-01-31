#!/bin/zsh

aws iam attach-role-policy \
    --role-name cmtr-7e60a31c-iam-peld-iam_role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws s3api put-bucket-policy --bucket cmtr-7e60a31c-iam-peld-bucket-2937822 --policy file://existing-policy.json
