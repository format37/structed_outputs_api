#!/usr/bin/env python3
"""
Simple Trading Agent Request
Exactly as specified in the requirements.
"""

import requests
import json

# API configuration
API_URL = "http://127.0.0.1:7070/api/structured-completion"

# Define the request exactly as specified
request_payload = {
    "system_prompt": "You are Assistant of the trading agent. You are listening for events and decide should u call agent or not, depending on importance of the event.",
    "user_prompt": "Event: The market is flat.",
    "json_schema": {
        "type": "object",
        "properties": {
            "should_call_trading_agent": {
                "type": "boolean"
            },
            "comment": {
                "type": "string"
            }
        },
        "required": ["should_call_trading_agent", "comment"],
        "additionalProperties": False
    },
    "schema_name": "trading_decision"
}

# Make the request
try:
    response = requests.post(API_URL, json=request_payload)
    response.raise_for_status()

    result = response.json()

    if result.get("success"):
        # Extract the structured response
        data = result.get("data", {})

        # Format output as specified
        output = {
            "json": {
                "should_call_trading_agent": data.get("should_call_trading_agent"),
                "comment": data.get("comment")
            }
        }

        print("Response:")
        print(json.dumps(output, indent=4))
    else:
        print(f"Error: {result.get('error')}")

except requests.exceptions.ConnectionError:
    print("Error: Cannot connect to API. Make sure the server is running.")
    print("Run: ./compose.sh up")
except Exception as e:
    print(f"Error: {e}")