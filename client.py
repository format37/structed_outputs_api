#!/usr/bin/env python3
"""
Client for the Structured Outputs API
Usage: python client.py
"""

import requests
import json
from typing import Dict, Any

# API endpoint (using 127.0.0.1 for Docker access)
API_BASE_URL = "http://127.0.0.1:7070"


def call_structured_completion(
    system_prompt: str,
    user_prompt: str,
    json_schema: Dict[str, Any],
    schema_name: str = "response_schema",
    model: str = "gpt-4o-2024-08-06"
) -> Dict[str, Any]:
    """
    Call the structured completion API endpoint.

    Args:
        system_prompt: System message for the model
        user_prompt: User message/query
        json_schema: JSON schema defining the expected response structure
        schema_name: Name for the schema
        model: OpenAI model to use

    Returns:
        API response as dictionary
    """
    endpoint = f"{API_BASE_URL}/api/structured-completion"

    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "json_schema": json_schema,
        "schema_name": schema_name,
        "model": model
    }

    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "success": False}


def example_math_calculation():
    """Example: Simple math calculation"""
    print("\n=== Example 1: Math Calculation ===")

    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "number"},
            "explanation": {"type": "string"}
        },
        "required": ["answer", "explanation"],
        "additionalProperties": False
    }

    result = call_structured_completion(
        system_prompt="You are a helpful math tutor.",
        user_prompt="What is 234 + 567?",
        json_schema=schema,
        schema_name="math_answer"
    )

    print(f"Request: What is 234 + 567?")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result


def example_sentiment_analysis():
    """Example: Sentiment analysis"""
    print("\n=== Example 2: Sentiment Analysis ===")

    schema = {
        "type": "object",
        "properties": {
            "sentiment": {
                "type": "string",
                "enum": ["positive", "negative", "neutral"]
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1
            },
            "key_phrases": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["sentiment", "confidence", "key_phrases"],
        "additionalProperties": False
    }

    result = call_structured_completion(
        system_prompt="You are a sentiment analysis expert.",
        user_prompt="Analyze the sentiment of: 'The product exceeded my expectations! Great quality and fast shipping.'",
        json_schema=schema,
        schema_name="sentiment_analysis"
    )

    print(f"Text: 'The product exceeded my expectations! Great quality and fast shipping.'")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result


def example_entity_extraction():
    """Example: Extract entities from text"""
    print("\n=== Example 3: Entity Extraction ===")

    schema = {
        "type": "object",
        "properties": {
            "people": {
                "type": "array",
                "items": {"type": "string"}
            },
            "locations": {
                "type": "array",
                "items": {"type": "string"}
            },
            "dates": {
                "type": "array",
                "items": {"type": "string"}
            },
            "organizations": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["people", "locations", "dates", "organizations"],
        "additionalProperties": False
    }

    result = call_structured_completion(
        system_prompt="You are an entity extraction specialist.",
        user_prompt="Extract entities from: 'John Smith from Microsoft visited Paris on January 15, 2024, to meet with Marie Dubois from Google.'",
        json_schema=schema,
        schema_name="entity_extraction"
    )

    print(f"Text: 'John Smith from Microsoft visited Paris on January 15, 2024, to meet with Marie Dubois from Google.'")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result


def example_todo_list():
    """Example: Generate structured TODO list"""
    print("\n=== Example 4: TODO List Generation ===")

    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "task": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["high", "medium", "low"]
                        },
                        "estimated_hours": {"type": "number"}
                    },
                    "required": ["task", "priority", "estimated_hours"]
                }
            },
            "total_estimated_hours": {"type": "number"}
        },
        "required": ["title", "tasks", "total_estimated_hours"],
        "additionalProperties": False
    }

    result = call_structured_completion(
        system_prompt="You are a project management assistant.",
        user_prompt="Create a TODO list for building a simple web API with Flask including testing and documentation",
        json_schema=schema,
        schema_name="todo_list"
    )

    print(f"Request: Create TODO list for building a simple web API with Flask")
    print(f"Response: {json.dumps(result, indent=2)}")
    return result


def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n=== Testing Health Endpoint ===")

    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print(f"Health check: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        return False


def main():
    """Run all examples"""
    print("=" * 60)
    print("Structured Outputs API Client")
    print(f"API Server: {API_BASE_URL}")
    print("=" * 60)

    # Test health endpoint first
    if not test_health_endpoint():
        print("\n❌ API server is not responding. Please ensure it's running.")
        print("   Run: docker-compose -f docker-compose.prod.yml up")
        return

    print("\n✅ API server is healthy!\n")
    print("Running examples...")

    # Run examples
    try:
        example_math_calculation()
        example_sentiment_analysis()
        example_entity_extraction()
        example_todo_list()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")


if __name__ == "__main__":
    main()