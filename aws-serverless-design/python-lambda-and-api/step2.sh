#!/bin/zsh

API_ID="s2ymfd8h9c"

# aws apigatewayv2 create-route \
#     --api-id $API_ID \
#     --route-key "POST /products" \

# aws apigatewayv2 create-route \
#     --api-id $API_ID \
#     --route-key "GET /products" \

# aws apigatewayv2 create-integration --api-id $API_ID \
#     --integration-type AWS_PROXY \
#     --integration-method GET \
#     --integration-uri arn:aws:lambda:eu-central-1:905418349556:function:cmtr-7e60a31c-dynamodb-l-lambda-getProductsList \
#     --payload-format-version 2.0

# aws apigatewayv2 create-integration --api-id $API_ID \
#     --integration-type AWS_PROXY \
#     --integration-method POST \
#     --integration-uri arn:aws:lambda:eu-central-1:905418349556:function:cmtr-7e60a31c-dynamodb-l-lambda-createProduct \
#     --payload-format-version 2.0


# aws lambda add-permission \
#     --function-name cmtr-7e60a31c-dynamodb-l-lambda-getProductsList \
#     --statement-id AllowExecutionFromAPIGateway2 \
#     --action lambda:InvokeFunction \
#     --principal apigateway.amazonaws.com \
#     --source-arn arn:aws:apigateway:eu-central-1::/apis/s2ymfd8h9c/routes/w0nm92b


# aws lambda add-permission \
#     --function-name cmtr-7e60a31c-dynamodb-l-lambda-createProduct \
#     --statement-id AllowExecutionFromAPIGateway3 \
#     --action lambda:InvokeFunction \
#     --principal apigateway.amazonaws.com \
#     --source-arn arn:aws:apigateway:eu-central-1::/apis/s2ymfd8h9c/routes/6g5gqq7

aws apigatewayv2 update-route \
    --api-id $API_ID \
    --route-id 6g5gqq7 \
    --target integrations/wvwdgxg

aws apigatewayv2 update-route \
    --api-id $API_ID \
    --route-id w0nm92b \
    --target integrations/2gffwnc


