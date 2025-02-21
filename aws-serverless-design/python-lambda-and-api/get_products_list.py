import boto3
import json

def lambda_handler(event, context):
    uuid = '14ba3d6a-a5ed-491b-a128-0a32b71a38c4'

    if 'headers' in event and 'random-uuid' in event["headers"]:
        uuid += f'-{event["headers"]["random-uuid"]}'

    dynamodb = boto3.client('dynamodb')
    products_key = {
        'id': {'S': uuid}
    }

    stocks_key = {
        'product_id': {'S': uuid}
    }

    # Retrieve from products table
    product_response = dynamodb.get_item(
        TableName='cmtr-7e60a31c-dynamodb-l-table-products',
        Key=products_key
    )
    product = product_response.get('Item')

    # Retrieve from stocks table
    stocks_response = dynamodb.get_item(
        TableName='cmtr-7e60a31c-dynamodb-l-table-stocks',
        Key=stocks_key
    )
    stock = stocks_response.get('Item')

    # Combine results
    result = product.copy()
    result['count'] = stock['count']

    return result