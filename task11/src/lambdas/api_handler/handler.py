import json
import logging
import os
import re

import boto3

client = boto3.client('cognito-idp', os.environ.get('region', 'eu-central-1'))
dynamodb = boto3.resource('dynamodb', os.environ.get('region', 'eu-central-1'))
CUP_ID = os.environ.get('cup_id')
CLIENT_ID = os.environ.get('cup_client_id')
TABLES_TABLE = os.getenv("tables_table")
RESERVATIONS_TABLE = os.getenv("reservations_table")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event, indent=4))
    body = json.loads(event['body'])
    request_path = event['resource']
    request_method = event['httpMethod']

    if request_path == '/signin' and request_method == "POST":
        response = signin(body.get('email'), body.get('password'))
    elif request_path == '/signup' and request_method == "POST":
        response = signup(body.get('email'), body.get('password'))
    elif request_path == '/tables' and request_method == "POST":
        response = create_table(body)
    elif request_path == '/tables' and request_method == "GET":
        response = get_tables(body)
    elif event["httpMethod"] == "GET" and event["resource"] == "/tables/{tableId}":
        return get_table(event["pathParameters"]["tableId"])
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

        """
        Enforces a custom password policy in AWS Cognito.
        - Password must be alphanumeric + only "$%^*-_"
        - Must be at least 12 characters long
        """
        # Regex for allowed password format
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$%^*\-_])[A-Za-z\d$%^*\-_]{12,}$"

        if not re.match(password_pattern, password):
            raise Exception("Password must be at least 12 characters and contain only letters, numbers, and '$%^*-_'.")

        client.admin_create_user(
            UserPoolId=CUP_ID,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ],
            MessageAction='SUPPRESS'
        )
        client.admin_set_user_password(
            UserPoolId=CUP_ID,
            Username=email,
            Password=password,
            Permanent=True
        )
        return {"statusCode": 200}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}


def signin(email, password):
    try:
        response = client.admin_initiate_auth(
            UserPoolId=CUP_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        logger.info(json.dumps(response, indent=4))
        return {"statusCode": 200, "body": json.dumps({"accessToken": response["AuthenticationResult"]["IdToken"]})}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}
    
def create_table(body):
    try:
        table = dynamodb.Table(TABLES_TABLE)

        item = {
            "id": body["id"],
            "number": body["number"],
            "places": body["places"],
            "isVip": body["isVip"],
            "minOrder": body.get("minOrder", None)
        }
        logger.info(f'Item to put to dynamodb: {item}')
        
        table.put_item(Item=item)
        return {"statusCode": 200, "body": json.dumps({"id": body["id"]})}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}

def get_tables():
    try:
        table = dynamodb.Table(TABLES_TABLE)
        response = table.scan()
        tables = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps({"tables": tables})}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}

def get_table(table_id):
    try:
        table = dynamodb.Table(TABLES_TABLE)
        response = table.get_item(Key={"id": int(table_id)})
        if "Item" not in response:
            raise Exception("Table not found")
        return {"statusCode": 200, "body": json.dumps(response["Item"])}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}