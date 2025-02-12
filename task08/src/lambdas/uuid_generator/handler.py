from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda
import boto3
import uuid
import json
import datetime
import os

_LOG = get_logger(__name__)


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        s3 = boto3.client("s3")
        
        target_bucket = os.environ['target_bucket']
        _LOG.info(f'target_bucket: {target_bucket}')
        # Get execution start time in ISO 8601 format
        execution_time = datetime.datetime.utcnow().isoformat() + "Z"  # Ensuring UTC and 'Z' suffix

        # Generate 10 random UUIDs
        uuids = [str(uuid.uuid4()) for _ in range(10)]

        # Convert to JSON format
        file_content = json.dumps({"ids": uuids}, indent=4)

        # Define the S3 file name as the exact execution time
        file_name = execution_time  # Example: "2024-01-01T00:00:00.000Z"
        

        # Upload file to S3
        s3.put_object(
            Bucket=target_bucket,
            Key=file_name,
            Body=file_content,
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "UUIDs stored successfully",
                "file_name": file_name,
                "s3_bucket": target_bucket
            })
        }
    

HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
