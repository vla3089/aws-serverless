import json

def lambda_handler(event, context):
    print(json.dumps(event))  # Logs the event for inspection
    # Check if the HTTP method is GET and the path is /hello
    if event.get("httpMethod") == "GET" and event.get("path") == "/hello":
        content = {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
        return {
            "statusCode" : 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": content,
            "isBase64Encoded": False
        }
    else:
        content = {
            "statusCode": 400,
            "message": "Bad request syntax or unsupported method. Request path: {0}. HTTP method: {1}".format(event.get("httpMethod"), event.get("path"))
        }
        return {
            "statusCode" : 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": content,
            "isBase64Encoded": False
        }