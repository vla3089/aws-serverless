#!/bin/zsh

aws iam update-assume-role-policy \
    --role-name cmtr-7e60a31c-iam-ar-iam_role-readonly \
    --policy-document file://cmtr-7e60a31c-readonly-trust-relationship.json
