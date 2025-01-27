from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json

_LOG = get_logger(__name__)


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        print(json.dumps(event))  # Logs the event for inspection
        return {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
    

HANDLER = HelloWorld()

def lambda_handler(event, context):
    print(json.dumps(event))  # Logs the event for inspection
    # Check if the HTTP method is GET and the path is /hello
    if event.get("httpMethod") == "GET" and event.get("path") == "/hello":
        return {
            "statusCode": 200,
            "message": "Hello from Lambda"
        }
    else:
        # Bad request syntax or unsupported method. Request path: /cmtr-7e60a31c. HTTP method: GET"
        # 
        return {
            "statusCode": 400,
            "message": "Bad request syntax or unsupported method. Request path: {0}. HTTP method: {1}".format(event.get("httpMethod"), event.get("path"))
        }

