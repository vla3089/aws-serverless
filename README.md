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
     --path "/events" \
     --method POST \
     --integration_type lambda \
     --lambda_name api_handler

syndicate generate meta dynamodb \
    --resource_name Events \
    --hash_key_name id \
    --hash_key_type S \
    --sort_key_name created_at \
    --sort_key_type S


# task 06

# lambdas_alias_name: learn
# target_table: Audit

syndicate generate project --name task06
cd task06
generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name audit_producer \
    --runtime python

syndicate generate meta dynamodb \
    --resource_name Configuration \
    --hash_key_name key \
    --hash_key_type S 

syndicate generate meta dynamodb \
    --resource_name Audit \
    --hash_key_name id \
    --hash_key_type S 

add to the lambda event_sources:
{
    "resource_type": "dynamodb_trigger",
    "target_table": "Configuration",
    "batch_size": 1,
    "function_response_types": ["ReportBatchItemFailures"]
}

# task 07

syndicate generate project --name task07
cd task07
generate config
export SDCT_CONF=...

syndicate generate meta dynamodb \
    --resource_name Events \
    --hash_key_name id \
    --hash_key_type S 

syndicate generate appsync api --name "GraphQL_API"

syndicate generate appsync data_source \
    --api_name "GraphQL_API" \
    --name Events_Data_Source \
    --type AMAZON_DYNAMODB \
    --resource_name Events \
    --service_role_name appsync_role

syndicate generate appsync resolver \
    --api_name "GraphQL_API" \
    --kind UNIT \
    --type_name Mutation \
    --field_name createEvent \
    --data_source_name Events_Data_Source \
    --runtime JS

syndicate generate appsync resolver \
    --api_name "GraphQL_API" \
    --kind UNIT \
    --type_name Query \
    --field_name getEvent \
    --data_source_name Events_Data_Source \
    --runtime JS


# task 08
syndicate generate project --name task08
cd task08
generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name uuid_generator \
    --runtime python

syndicate generate meta s3_bucket \
    --resource_name uuid-storage

syndicate generate meta cloudwatch_event_rule \
    --resource_name uuid_trigger \
    --rule_type schedule \
    --expression "cron(* * * * ? *)" 
