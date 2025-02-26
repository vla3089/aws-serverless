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


# task 09

source .venv/bin/activate

syndicate generate project --name task09
cd task09
generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name api_handler \
    --runtime python


syndicate generate lambda_layer \
    --name sdk_layer \
    --runtime python \
    --link_with_lambda api_handler



syndicate create_deploy_target_bucket

syndicate clean; syndicate build && syndicate deploy


# task 10

syndicate generate project --name task10
cd task10

generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name processor \
    --runtime python

syndicate generate meta dynamodb \
    --resource_name Weather \
    --hash_key_name id \
    --hash_key_type S 

# task11

syndicate generate project --name task11
cd task11

generate config
export SDCT_CONF=...

syndicate generate lambda \
    --name api_handler \
    --runtime python

syndicate generate meta api_gateway \
    --resource_name task11_api \
    --deploy_stage api

syndicate generate meta cognito_user_pool \
    --resource_name simple-booking-userpool

syndicate generate meta api_gateway_authorizer \
    --api_name task11_api \
    --name task11_cognito_authorizer \
    --type COGNITO_USER_POOLS \
    --provider_name simple-booking-userpool

# sign in endpoint configuration
syndicate generate meta api_gateway_resource \
    --api_name task11_api \
    --path signin

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/signin" \
     --method POST \
     --integration_type lambda \
     --lambda_name api_handler

# sign up endpoint configuration
syndicate generate meta api_gateway_resource \
    --api_name task11_api \
    --path signup

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/signup" \
     --method POST \
     --integration_type lambda \
     --lambda_name api_handler

# tables endpoint configuration
syndicate generate meta api_gateway_resource \
    --api_name task11_api \
    --path tables

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/tables" \
     --method GET \
     --integration_type lambda \
     --lambda_name api_handler \
     --authorization_type CUSTOM \
     --authorizer_name task11_cognito_authorizer

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/tables" \
     --method POST \
     --integration_type lambda \
     --lambda_name api_handler \
     --authorization_type CUSTOM \
     --authorizer_name task11_cognito_authorizer

# # tables/{tableId}
syndicate generate meta api_gateway_resource \
    --api_name task11_api \
    --path tables/{tableId}

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/tables/{tableId}" \
     --method GET \
     --integration_type lambda \
     --lambda_name api_handler \
     --authorization_type CUSTOM \
     --authorizer_name task11_cognito_authorizer

# reservations endpoint configuration
syndicate generate meta api_gateway_resource \
    --api_name task11_api \
    --path reservations

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/reservations" \
     --method GET \
     --integration_type lambda \
     --lambda_name api_handler \
     --authorization_type CUSTOM \
     --authorizer_name task11_cognito_authorizer

syndicate generate meta api_gateway_resource_method \
    --api_name task11_api \
     --path "/reservations" \
     --method POST \
     --integration_type lambda \
     --lambda_name api_handler \
     --authorization_type CUSTOM \
     --authorizer_name task11_cognito_authorizer

# dynamodb tables generation

syndicate generate meta dynamodb \
    --resource_name Tables \
    --hash_key_name key \
    --hash_key_type S 

syndicate generate meta dynamodb \
    --resource_name Reservations \
    --hash_key_name key \
    --hash_key_type S 




# task 12

syndicate export \
    --rest-api-id c1ncb5r503 \
    --stage-name api \
    --export-type oas30 \
    --output-file openapi-spec.json


syndicate generate meta s3_bucket \
    --resource_name api-ui-hoster \
    --static_website_hosting True


syndicate generate swagger_ui \
  --name task12_api_ui \
  --path_to_spec z0rw4yfqw4_oas_v3.json \
  --target_bucket api-ui-hoster