#!/usr/bin/env python3
"""
Trading Agent Assistant Client

This script demonstrates how to use the Structured Outputs API to create
a decision-making assistant for a trading agent that evaluates market events.

Usage: python trading_agent_assistant.py
"""

import requests
import json
import sys
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API endpoint
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:7070")


def call_trading_assistant(event_description: str, model: str = "gpt-4o-2024-08-06") -> Dict[str, Any]:
    """
    Call the structured API to evaluate whether a trading event requires agent intervention.

    Args:
        event_description: Description of the market event
        model: OpenAI model to use

    Returns:
        Structured response with decision and comment
    """

    # Define the JSON schema for the response
    json_schema = {
        "type": "object",
        "properties": {
            "should_call_trading_agent": {
                "type": "boolean",
                "description": "Whether the trading agent should be called based on the event importance"
            },
            "comment": {
                "type": "string",
                "description": "Brief explanation of the decision"
            }
        },
        "required": ["should_call_trading_agent", "comment"],
        "additionalProperties": False
    }

    # System and user prompts
    system_prompt = (
        "You are Assistant of the trading agent. "
        "You are listening for events and decide should you call agent or not, "
        "depending on importance of the event."
    )

    user_prompt = f"Event: {event_description}"

    # Prepare the request payload
    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "json_schema": json_schema,
        "schema_name": "trading_decision",
        "model": model
    }

    # Make the API call
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/structured-completion",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out after 30 seconds"
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": f"Failed to connect to API at {API_BASE_URL}. Is the server running?"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }


def print_separator():
    """Print a visual separator."""
    print("-" * 60)


def main():
    """Run trading assistant examples with various market events."""

    print("=" * 60)
    print("Trading Agent Assistant - Market Event Analyzer")
    print(f"API Server: {API_BASE_URL}")
    print("=" * 60)
    print()

    # Test various market events
    market_events = [
        "The market is flat.",
        "Bitcoin just dropped 15% in the last hour!",
        "Slight increase in trading volume, up 2% from yesterday.",
        "BREAKING: Federal Reserve announces emergency rate cut of 75 basis points!",
        "EUR/USD is trading within normal range, volatility at 0.5%.",
        "Major exchange hack reported - $100M in assets potentially affected!",
        "Gold prices stable at $2,050 per ounce.",
        "Flash crash detected in S&P 500 futures, down 8% in 2 minutes!",
        "Quarterly earnings season begins next week.",
        "VIX spike to 45 - extreme fear in the market!"
    ]

    # Check if we should run all examples or just one
    if len(sys.argv) > 1:
        # Use command line argument as custom event
        custom_event = " ".join(sys.argv[1:])
        market_events = [custom_event]
        print(f"Analyzing custom event: {custom_event}")
        print()

    # Process each event
    for i, event in enumerate(market_events, 1):
        print(f"Event {i}: {event}")
        print_separator()

        result = call_trading_assistant(event)

        if result.get("success"):
            data = result.get("data", {})
            should_call = data.get("should_call_trading_agent", False)
            comment = data.get("comment", "No comment provided")

            # Display with color coding (if terminal supports it)
            if should_call:
                action = "🚨 CALL AGENT"
                color = "\033[91m"  # Red
            else:
                action = "✓ NO ACTION"
                color = "\033[92m"  # Green

            print(f"{color}Decision: {action}\033[0m")
            print(f"Reasoning: {comment}")

            # Show raw response in verbose mode
            if os.environ.get("VERBOSE") == "1":
                print(f"\nRaw response:")
                print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")

        print()

    # Summary
    print("=" * 60)
    print("Analysis complete!")

    if len(market_events) > 1:
        print("\nTip: Run with a custom event as argument:")
        print("  python trading_agent_assistant.py 'Your custom market event here'")
        print("\nSet VERBOSE=1 for detailed output:")
        print("  VERBOSE=1 python trading_agent_assistant.py")


if __name__ == "__main__":
    # Quick health check first
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ API server is not healthy. Status: {health_response.status_code}")
            print("Please ensure the server is running: ./compose.sh up")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to API server at {API_BASE_URL}")
        print(f"Error: {e}")
        print("\nPlease ensure the server is running:")
        print("  ./compose.sh up")
        sys.exit(1)

    # Run main program
    main()