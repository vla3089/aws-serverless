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