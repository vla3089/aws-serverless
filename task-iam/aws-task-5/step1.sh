#!/bin/zsh


aws iam put-role-policy \
    --role-name cmtr-7e60a31c-iam-sewk-iam_role \
    --policy-name cmtr-7e60a31c-use-kms-key-permission \
    --policy-document file://cmtr-7e60a31c-use-kms-key-permission.json
