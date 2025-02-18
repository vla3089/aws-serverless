from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import json
import boto3
import os
import uuid
from datetime import datetime

_LOG = get_logger(__name__)

class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        _LOG.info(f'{event}')
        try:
            # Parse request body
            content = event.get('content', '{}')
            principalId = event.get('principalId')
            _LOG.info(f'Content: {content}')
            
            # Generate a unique ID for the event
            event_id = str(uuid.uuid4())
            _LOG.info(f'event_id: {event_id}')

            # Prepare item for DynamoDB
            item = {
                'id': event_id,
                'createdAt': datetime.utcnow().isoformat(),
                'principalId': principalId,
                'body': content
            }
            _LOG.info(f'Item to put to dynamodb: {item}')
            
            # Save to DynamoDB
            
            region_name = os.environ['region']
            target_table = os.environ['target_table']
            _LOG.info(f'region_name: {region_name}')
            _LOG.info(f'target_table: {target_table}')

            dynamodb = boto3.resource('dynamodb', region_name=region_name)

            table = dynamodb.Table(target_table)

            table.put_item(Item=item)
            
            # Return response
            return {
                'statusCode': 201,
                'body': item
            }
        except Exception as e:
            _LOG.info(json.dumps({'error': str(e)}))
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
