import json
import logging
import os
import re

import boto3
import uuid
from datetime import datetime

client = boto3.client('cognito-idp', os.environ.get('region', 'eu-central-1'))
dynamodb = boto3.client('dynamodb', os.environ.get('region', 'eu-central-1'))
CUP_ID = os.environ.get('cup_id')
CLIENT_ID = os.environ.get('cup_client_id')
TABLES_TABLE = os.getenv("tables_table")
RESERVATIONS_TABLE = os.getenv("reservations_table")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps(event, indent=4))    
    request_path = event['resource']
    request_method = event['httpMethod']

    if request_path == '/signin' and request_method == "POST":
        body = json.loads(event['body'])
        response = signin(body.get('email'), body.get('password'))
    elif request_path == '/signup' and request_method == "POST":
        body = json.loads(event['body'])
        response = signup(body.get('email'), body.get('password'))
    elif request_path == '/tables' and request_method == "POST":
        body = json.loads(event['body'])
        response = create_table(body)
    elif request_path == '/tables' and request_method == "GET":
        response = get_tables()
    elif event["httpMethod"] == "GET" and event["resource"] == "/tables/{tableId}":
        return get_table(event["pathParameters"]["tableId"])
    elif event["httpMethod"] == "POST" and event["resource"] == "/reservations":
        body = json.loads(event['body'])
        return make_reservation(body)
    elif event["httpMethod"] == "POST" and event["resource"] == "/reservations":
        return get_reservations()
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
        item = {
            "id": {"N": str(body["id"])},
            "number": {"N": str(body["number"])},
            "places": {"N": str(body["places"])},
            "isVip": {"BOOL": body["isVip"]},
        }

        if "minOrder" in body:
            item["minOrder"] = {"N": str(body["minOrder"])}

        logger.info(f'Tables table name: {TABLES_TABLE}')
        logger.info(f'Item to put to dynamodb: {json.dumps(item)}')
        
        dynamodb.put_item(
            TableName = TABLES_TABLE,
            Item=item)
        return {"statusCode": 200, "body": json.dumps({"id": body["id"]})}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}

def get_tables():
    try:
        response = dynamodb.scan(TableName = TABLES_TABLE)
        tables = []
        
        for item in response.get("Items", []):
            logger.info(f'Item to put to dynamodb: {json.dumps(item)}')
            table = {
                "id": int(item["id"]["N"]),
                "number": int(item["tableNumber"]["N"]),
                "places": int(item["places"]["N"]),
                "isVip": item["isVip"]["BOOL"]
            }
            if "minOrder" in item:
                table["minOrder"] = int(item["minOrder"]["N"])
            
            tables.append(table)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"tables": tables})
        }
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}

def get_table(table_id):
    try:
        response = dynamodb.get_item(TableName = TABLES_TABLE, Key={"id": {"N" : str(table_id)}})        
        if "Item" not in response:
            raise Exception("Table not found")
        
        logger.info(f'Item to put to dynamodb: {json.dumps(response)}')
        item = {
                "id": int(response["Item"]["id"]["N"]),
                "number": int(response["Item"]["tableNumber"]["N"]),
                "places": int(response["Item"]["places"]["N"]),
                "isVip": response["Item"]["isVip"]["BOOL"]
            }
        return {"statusCode": 200, "body": json.dumps(item)}
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}
    
def make_reservation(body):
    try:
        # Validate required fields
        required_fields = ["tableNumber", "clientName", "phoneNumber", "date", "slotTimeStart", "slotTimeEnd"]
        if not all(field in body for field in required_fields):
            raise "Missing required fields"
        
        # Validate date format
        datetime.strptime(body["date"], "%Y-%m-%d")
        

        # Check if table exists
        table_response = dynamodb.get_item(TableName=TABLES_TABLE, Key={"tableNumber": {"N": str(body["tableNumber"])}})
        if "Item" not in table_response:
            raise "Table not found"
        
        # Check for conflicting reservations
        existing_reservations = dynamodb.scan(
            TableName=RESERVATIONS_TABLE,
            FilterExpression="tableNumber = :tableNum AND #date = :date AND ((slotTimeStart <= :endTime AND slotTimeEnd >= :startTime))",
            ExpressionAttributeNames={"#date": "date"},
            ExpressionAttributeValues={
                ":tableNum": {"N": str(body["tableNumber"])},
                ":date": {"S": body["date"]},
                ":startTime": {"S": body["slotTimeStart"]},
                ":endTime": {"S": body["slotTimeEnd"]}
            }
        )

        if existing_reservations.get("Count", 0) > 0:
            raise "conflicting reservations"

        # Generate a unique reservation ID
        reservation_id = str(uuid.uuid4())
        
        # Create reservation item
        reservation = {
            "id": {"S": reservation_id},
            "tableNumber": {"N": str(body["tableNumber"])},
            "clientName": {"S": body["clientName"]},
            "phoneNumber": {"S": body["phoneNumber"]},
            "date": {"S": body["date"]},
            "slotTimeStart": {"S": body["slotTimeStart"]},
            "slotTimeEnd": {"S": body["slotTimeEnd"]}
        }

        logger.info(f'Item to put to dynamodb: {json.dumps(reservation)}')
        
        # Store in DynamoDB
        dynamodb.put_item(TableName=RESERVATIONS_TABLE, Item=reservation)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"reservationId": reservation_id})
        }
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}
    
def get_reservations():
    try:
        response = dynamodb.scan(TableName=RESERVATIONS_TABLE)
        reservations = []
        
        for item in response.get("Items", []):
            reservations.append({
                "tableNumber": int(item["tableNumber"]["N"]),
                "clientName": item["clientName"]["S"],
                "phoneNumber": item["phoneNumber"]["S"],
                "date": item["date"]["S"],
                "slotTimeStart": item["slotTimeStart"]["S"],
                "slotTimeEnd": item["slotTimeEnd"]["S"]
            })
        
        return {
            "statusCode": 200,
            "body": json.dumps({"reservations": reservations})
        }
    except Exception as e:
        error_log = {
            "error": str(e),
        }
        logger.exception(json.dumps(error_log, indent=4))  # Logs error with stack trace
        return {"statusCode": 400}