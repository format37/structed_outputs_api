#!/bin/bash

# Trading Agent Request with curl - Verbose version
# Includes error handling and formatted output

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="${API_URL:-http://127.0.0.1:7070/api/structured-completion}"

echo "=================================="
echo "Trading Agent Request (curl)"
echo "API: $API_URL"
echo "=================================="
echo

# Check if server is running
echo "Checking API health..."
if ! curl -s -f "http://127.0.0.1:7070/health" > /dev/null 2>&1; then
    echo -e "${RED}Error: API server is not responding${NC}"
    echo "Please start the server: ./compose.sh up"
    exit 1
fi
echo -e "${GREEN}✓ API server is healthy${NC}"
echo

# Prepare the JSON payload
JSON_PAYLOAD='{
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
}'

# Make the request
echo "Sending request..."
echo "Event: 'The market is flat.'"
echo

RESPONSE=$(curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Check if curl succeeded
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to make request${NC}"
    exit 1
fi

# Parse and display the response
if command -v jq &> /dev/null; then
    # If jq is installed, use it for pretty formatting
    SUCCESS=$(echo "$RESPONSE" | jq -r '.success')

    if [ "$SUCCESS" = "true" ]; then
        SHOULD_CALL=$(echo "$RESPONSE" | jq -r '.data.should_call_trading_agent')
        COMMENT=$(echo "$RESPONSE" | jq -r '.data.comment')

        echo "Response:"
        echo "========="

        if [ "$SHOULD_CALL" = "true" ]; then
            echo -e "${RED}🚨 Decision: CALL AGENT${NC}"
        else
            echo -e "${GREEN}✓ Decision: NO ACTION${NC}"
        fi

        echo "Comment: $COMMENT"
        echo
        echo "Formatted JSON:"
        echo "$RESPONSE" | jq '{json: {should_call_trading_agent: .data.should_call_trading_agent, comment: .data.comment}}'
    else
        ERROR=$(echo "$RESPONSE" | jq -r '.error')
        echo -e "${RED}Error from API: $ERROR${NC}"
    fi
else
    # Fallback to python json.tool if jq is not installed
    echo "Response:"
    echo "$RESPONSE" | python -m json.tool

    # Try to extract key fields using grep and sed (less reliable but works)
    if echo "$RESPONSE" | grep -q '"success": true'; then
        echo
        echo -e "${GREEN}✓ Request succeeded${NC}"
    else
        echo
        echo -e "${RED}✗ Request failed${NC}"
    fi
fi