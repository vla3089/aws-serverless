# aws-serverless


# task04

Lambda Function 1: sqs_handler
SQS Queue: async_queue
Lambda Function 2: sns_handler
SNS Topic: lambda_topic


syndicate generate project --name task04
cd task04
generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name sqs_handler \
    --runtime python

syndicate generate lambda \
    --name sns_handler \
    --runtime python

syndicate generate meta sqs_queue \
    --resource_name async_queue

syndicate generate meta sns_topic \
    --resource_name lambda_topic \
    --region eu-central-1


# task05

syndicate generate project --name task05
cd task05
generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name api_handler \
    --runtime python

syndicate generate meta api_gateway \
    --resource_name task5_api \
    --deploy_stage api

syndicate generate meta api_gateway_resource \
    --api_name task5_api \
    --path events

syndicate generate meta api_gateway_resource_method \
    --api_name task5_api \
     --path "/events" --method POST --lambda_name api_handler

syndicate generate meta dynamodb \
    --resource_name Events \
    --hash_key_name id \
    --hash_key_type S \
    --sort_key_name created_at \
    --sort_key_type S