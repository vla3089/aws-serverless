from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        _LOG
        method = event["requestContext"]["http"]["method"]
        path = event.get("requestContext").get("http").get("path")

        if method == "GET" and path == "/hello":
            content = {
                "statusCode": 200,
                "message": "Hello from Lambda"
            }
            return {
                'statusCode': 200,
                'body': content
            }
        else:
            return {
                "statusCode": 400,
                "message": "Bad request syntax or unsupported method. Request path: {0}. HTTP method: {1}".format(path, method)
            }            

        
    

HANDLER = HelloWorld()

def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
