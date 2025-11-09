"""
REST API server for structured OpenAI completions
Usage:
    export OPENAI_API_KEY="your-api-key-here"
    python api_server.py
"""

from flask import Flask, request, jsonify
from typing import Dict, Any
import os
import sys
from openai import OpenAI
from pydantic import BaseModel, create_model
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def structured_completion(system_prompt: str, user_prompt: str, json_schema: Dict[str, Any],
                         schema_name: str = "response_schema",
                         model: str = "gpt-5") -> Dict[str, Any]:
    """
    Execute a structured completion using OpenAI's API with response format enforcement.

    Args:
        system_prompt: System message for the model
        user_prompt: User message/query
        json_schema: JSON schema defining the expected response structure
        schema_name: Name for the schema
        model: OpenAI model to use

    Returns:
        Parsed JSON response matching the schema
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "schema": json_schema
                }
            }
        )

        # Parse the JSON response
        response_content = completion.choices[0].message.content
        return json.loads(response_content)

    except Exception as e:
        raise Exception(f"Structured completion failed: {str(e)}")


@app.route('/api/structured-completion', methods=['POST'])
def api_structured_completion():
    """
    Generic endpoint for structured completions.
    
    POST body example:
    {
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "What is 2+2?",
        "json_schema": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"}
            },
            "required": ["answer"],
            "additionalProperties": false
        },
        "schema_name": "math_answer",
        "model": "gpt-5"  // optional
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['system_prompt', 'user_prompt', 'json_schema']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Optional fields with defaults
        schema_name = data.get('schema_name', 'response_schema')
        model = data.get('model', 'gpt-5')
        
        # Execute structured completion
        result = structured_completion(
            system_prompt=data['system_prompt'],
            user_prompt=data['user_prompt'],
            json_schema=data['json_schema'],
            schema_name=schema_name,
            model=model
        )
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("ERROR: OPENAI_API_KEY not configured properly!")
        print("Please set a valid OpenAI API key in your .env file")
        sys.exit(1)

    # Get port from environment or use default
    port = int(os.environ.get("PORT", 7070))

    # Run server (debug=False in production)
    app.run(host='0.0.0.0', port=port, debug=False)
