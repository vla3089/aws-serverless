#!/bin/zsh

aws iam put-role-policy \
    --role-name cmtr-7e60a31c-iam-ar-iam_role-assume \
    --policy-name cmtr-7e60a31c-assume-role-policy \
    --policy-document file://cmtr-7e60a31c-assume-role-policy.json
