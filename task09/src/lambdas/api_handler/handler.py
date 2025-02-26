import json
import requests

# Define default latitude and longitude (Berlin, Germany)
DEFAULT_LATITUDE = 52.52
DEFAULT_LONGITUDE = 13.41

# Open-Meteo API URL template
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

def map_weather_data(input_data):
    mapped_data = {
        "latitude": input_data.get("latitude"),
        "longitude": input_data.get("longitude"),
        "generationtime_ms": input_data.get("generationtime_ms"),
        "utc_offset_seconds": input_data.get("utc_offset_seconds"),
        "timezone": input_data.get("timezone"),
        "timezone_abbreviation": input_data.get("timezone_abbreviation"),
        "elevation": input_data.get("elevation"),
        "hourly_units": input_data.get("hourly_units"),
        "hourly": {
            "time": input_data["hourly"]["time"],
            "temperature_2m": input_data["hourly"]["temperature_2m"],
            "relative_humidity_2m": input_data["hourly"].get("relative_humidity_2m", []),
            "wind_speed_10m": input_data["hourly"]["wind_speed_10m"],
        },
        "current_units": input_data.get("current_units"),
        "current": input_data.get("current"),
    }
    return mapped_data

def lambda_handler(event, context):
    print(event)
    """Lambda function to handle GET /weather requests"""
    
    # Validate HTTP method and path
    method = event["requestContext"]["http"]["method"]
    path = event.get("requestContext").get("http").get("path")
    if method != "GET" or path != "/weather":
        return {
            "statusCode": 400,
            "body": json.dumps({
                "statusCode": 400,
                "message": f"Bad request syntax or unsupported method. Request path: {path}. HTTP method: {method}"
            }),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        # Construct API request URL
        url = WEATHER_API_URL.format(DEFAULT_LATITUDE, DEFAULT_LONGITUDE)
        
        # Fetch weather data from Open-Meteo
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        weather_data = map_weather_data(response.json())

        return {
            "statusCode": 200,
            "body": json.dumps(weather_data),
            "headers": {"Content-Type": "application/json"}
        }

    except requests.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "message": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
