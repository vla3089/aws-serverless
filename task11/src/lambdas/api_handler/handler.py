import json
import os

import boto3

cognito_client = boto3.client('cognito-idp',
                              os.environ.get('region', 'eu-central-1'))
CUP_ID = os.environ.get('cup_id')
CLIENT_ID = os.environ.get('cup_client_id')


def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    request_path = event['resource']
    email = body.get('email')
    password = body.get('password')

    if request_path == '/login':
        return login(email, password)
    elif request_path == '/signup':
        return signup(email, password)
    else:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({'message': 'Unknown request path'})
        }


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
        return {"statusCode": 200}
    except Exception:
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
    except Exception:
        return {"statusCode": 400}
    

