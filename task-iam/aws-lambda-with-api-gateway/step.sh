#!/bin/zsh

# step 1
aws iam attach-role-policy \
    --role-name cmtr-7e60a31c-iam-lp-iam_role \
    --policy-arn arn:aws:iam::aws:policy/AWSLambda_ReadOnlyAccess

# step 2
aws lambda add-permission \
    --function-name cmtr-7e60a31c-iam-lp-lambda \
    --statement-id AllowExecutionFromAPIGateway2 \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --region eu-central-1
