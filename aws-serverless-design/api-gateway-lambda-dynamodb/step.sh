#!/bin/bash

aws apigatewayv2 update-route \
    --api-id 8ambbtt4me \
    --route-id vp39xk5 \
    --route-key "GET /contacts"

# step 2
aws lambda add-permission \
    --function-name cmtr-7e60a31c-api-gwlp-lambda-contacts \
    --statement-id AllowExecutionFromAPIGateway2 \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --region eu-central-1
