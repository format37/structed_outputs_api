#!/bin/bash

# Trading Agent Request using curl
# Same request as simple_trading_request.py

API_URL="http://127.0.0.1:7070/api/structured-completion"

# Make the request with curl
curl -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d '{
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
      "additionalProperties": false
    },
    "schema_name": "trading_decision"
  }' | python -m json.tool