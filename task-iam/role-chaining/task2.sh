#!/bin/zsh


aws iam attach-role-policy \
    --role-name cmtr-7e60a31c-iam-ar-iam_role-readonly \
    --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

