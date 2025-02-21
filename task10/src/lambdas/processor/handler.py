import json
import uuid
import boto3
import requests
import os
from decimal import Decimal

# Weather API URL
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.419998&hourly=temperature_2m"

def convert_floats_to_decimal(obj):
    """Recursively convert float values to Decimal."""
    if isinstance(obj, float):
        return Decimal(str(obj))  # Convert float to string first to avoid precision issues
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats_to_decimal(v) for v in obj]
    return obj

def fetch_weather():
    """Fetch weather data from the API."""
    response = requests.get(WEATHER_API_URL)
    response.raise_for_status()  # Raises an error for bad responses (4xx and 5xx)
    return response.json()

def transform_data(weather_data):
    """Extract and transform relevant data into required format."""
    transformed_data = {
        "id": str(uuid.uuid4()),
        "forecast": {
            "latitude": weather_data["latitude"],
            "longitude": weather_data["longitude"],
            "generationtime_ms": weather_data["generationtime_ms"],
            "utc_offset_seconds": weather_data["utc_offset_seconds"],
            "timezone": weather_data["timezone"],
            "timezone_abbreviation": weather_data["timezone_abbreviation"],
            "elevation": weather_data["elevation"],
            "hourly": {
                "time": weather_data["hourly"]["time"],
                "temperature_2m": weather_data["hourly"]["temperature_2m"]
            },
            "hourly_units": {
                "time": weather_data["hourly_units"]["time"],
                "temperature_2m": weather_data["hourly_units"]["temperature_2m"]
            }
        }
    }
    return convert_floats_to_decimal(transformed_data)

def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb")
    table_name = os.getenv("target_table", "Weather")
    table = dynamodb.Table(table_name)
    
    """AWS Lambda function handler."""
    try:
        weather_data = fetch_weather()
        transformed_data = transform_data(weather_data)
        table.put_item(Item=transformed_data)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Weather data stored successfully!", "id": transformed_data["id"]})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
