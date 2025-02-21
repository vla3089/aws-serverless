#!/bin/zsh

aws lambda update-function-code \
    --function-name cmtr-7e60a31c-lambda-fgufc-lambda \
    --zip-file fileb://lambda_function.zip \
    --region eu-central-1
