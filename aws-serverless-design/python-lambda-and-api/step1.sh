#!/bin/zsh

aws iam attach-role-policy \
    --role-name cmtr-7e60a31c-dynamodb-l-lambda-getProductsList \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess

aws iam attach-role-policy \
    --role-name cmtr-7e60a31c-dynamodb-l-lambda-createProduct \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws lambda update-function-code \
    --function-name cmtr-7e60a31c-dynamodb-l-lambda-getProductsList \
    --zip-file fileb://get_products_list.zip \
    --region eu-central-1

aws lambda update-function-code \
    --function-name cmtr-7e60a31c-dynamodb-l-lambda-createProduct \
    --zip-file fileb://create_product.zip \
    --region eu-central-1