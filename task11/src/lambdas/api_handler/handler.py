import json
import logging
import os

import boto3

cognito_client = boto3.client('cognito-idp',
                              os.environ.get('region', 'eu-central-1'))
CUP_ID = os.environ.get('cup_id')
CLIENT_ID = os.environ.get('cup_client_id')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event, indent=4))
    body = json.loads(event['body'])
    request_path = event['resource']
    request_method = event['httpMethod']
    email = body.get('email')
    password = body.get('password')

    if request_path == '/login' & request_method == "POST":
        response = login(email, password)
    elif request_path == '/signup' & request_method == "POST":
        response = signup(email, password)
    else:
        response = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'message': 'Unknown request path'})
        }
    logger.info(json.dumps(response, indent=4))
    return response


def signup(email, password):
    try:
        cognito_client.admin_create_user(
            UserPoolId=CUP_ID,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ],
            MessageAction='SUPPRESS'
        )
        cognito_client.admin_set_user_password(
            UserPoolId=CUP_ID,
            Username=email,
            Password=password,
            Permanent=True
        )
        cognito_client.admin_confirm_sign_up(
            UserPoolId=CUP_ID,
            Username=email
        )
        return {"statusCode": 200}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}


def login(email, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return {"statusCode": 200, "body": json.dumps({"accessToken": response["AuthenticationResult"]["AccessToken"]})}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}
    

