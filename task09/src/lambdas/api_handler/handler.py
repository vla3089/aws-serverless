from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
from layers.sdk_layer import OpenMeteoClient

_LOG = get_logger(__name__)


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        client = OpenMeteoClient()
        forecast = client.get_forecast()

        return {
            "statusCode": 200,
            "body": forecast
        }
    

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
