from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

import json
import boto3
import uuid
import os
from datetime import datetime

_LOG = get_logger(__name__)


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        # todo implement business logic
        _LOG.info(f'{event}')

        region_name = os.environ['region']            
        _LOG.info(f'region_name: {region_name}')
        target_table = os.environ['target_table']
        _LOG.info(f'target_table: {target_table}')

        dynamodb = boto3.resource("dynamodb", region_name=region_name)
        audit_table = dynamodb.Table(target_table)

        for record in event["Records"]:
            if record["eventName"] not in ("INSERT", "MODIFY"):
                _LOG.info(f'Skip record: {record}')
                continue
            _LOG.info(f'Processing record: {record}')
            new_image = record["dynamodb"].get("NewImage", {})
            old_image = record["dynamodb"].get("OldImage", {})

            item_key = new_image["key"]["S"]
            modification_time = datetime.utcnow().isoformat() + "Z"

            if record["eventName"] == "INSERT":
            # New configuration item added
                audit_entry = {
                    "id": str(uuid.uuid4()),
                    "itemKey": item_key,
                    "modificationTime": modification_time,
                    "newValue": {
                        "key": new_image["key"]["S"],
                        "value": int(new_image["value"]["N"]),
                    },
                }
            elif record["eventName"] == "MODIFY":
                # Existing configuration item updated
                for key in new_image:
                    if key in old_image and new_image[key] != old_image[key]:
                        audit_entry = {
                            "id": str(uuid.uuid4()),
                            "itemKey": item_key,
                            "modificationTime": modification_time,
                            "updatedAttribute": key,
                            "oldValue": int(old_image[key]["N"]),
                            "newValue": int(new_image[key]["N"]),
                        }
        
            # Store audit entry in the Audit table
            _LOG.info(f'Store audit entry in the Audit table: {audit_entry}')
            audit_table.put_item(Item=audit_entry)
    
        return {"statusCode": 200, "body": "Audit records processed."}
    

HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
