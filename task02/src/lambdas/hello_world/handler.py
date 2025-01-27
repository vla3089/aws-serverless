from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger(__name__)


class HelloWorld(AbstractLambda):

    def validate_request(self, event) -> dict:
        method = event["requestContext"]["http"]["method"]
        path = event.get("requestContext").get("http").get("path")
        if method != "GET" and path != "/hello":
            return {
                "statusCode": 400,
                "message": "Bad request syntax or unsupported method. Request path: {0}. HTTP method: {1}".format(path, method)
                }
        else:
            pass
        
    def handle_request(self, event, context):
        return {
            "message": "Hello from Lambda"
        }
    

HANDLER = HelloWorld()

def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
