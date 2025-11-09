# Structured Outputs API Examples

This folder contains example scripts demonstrating various use cases for the Structured Outputs API.

## Available Examples

### Shell Scripts (curl)

#### `trading_request.sh`
Simple curl request exactly matching simple_trading_request.py:
```bash
# Basic request with formatted JSON output
./trading_request.sh
```

#### `trading_request_verbose.sh`
Enhanced version with health checks, colors, and formatted output:
```bash
# Verbose version with health check and colored output
./trading_request_verbose.sh

# Use different API endpoint
API_URL=http://localhost:8080/api/structured-completion ./trading_request_verbose.sh
```

### Python Scripts

#### 1. Simple Trading Request (`simple_trading_request.py`)
Minimal implementation exactly as specified:
```bash
python simple_trading_request.py
```

Output format:
```json
{
    "json": {
        "should_call_trading_agent": false,
        "comment": "Market is stable, no action needed"
    }
}
```

#### 2. Trading Agent Assistant (`trading_agent_assistant.py`)
Full-featured trading assistant with multiple examples:

**Features:**
- Tests 10 different market events
- Color-coded decisions (🚨 urgent, ✓ no action)
- Custom event support via command line
- Verbose mode for debugging

**Usage:**
```bash
# Run with default example events
python trading_agent_assistant.py

# Run with custom event
python trading_agent_assistant.py "Bitcoin crashes 50% overnight!"

# Run with verbose output
VERBOSE=1 python trading_agent_assistant.py

# Use different API endpoint
API_BASE_URL=http://localhost:8080 python trading_agent_assistant.py
```

## Prerequisites

1. **Start the API server:**
   ```bash
   cd ..
   ./compose.sh up
   ```

2. **Ensure `.env` file contains valid OpenAI API key:**
   ```bash
   # Check if configured
   grep OPENAI_API_KEY ../.env
   ```

3. **For Python scripts, install dependencies:**
   ```bash
   pip install requests python-dotenv
   ```

4. **For shell scripts with enhanced formatting (optional):**
   ```bash
   # Install jq for better JSON parsing (optional)
   sudo apt-get install jq  # Ubuntu/Debian
   brew install jq          # macOS
   ```

## Quick Test

Run all examples in sequence:
```bash
# Test with shell/curl
./trading_request.sh

# Test with Python (simple)
python simple_trading_request.py

# Test with Python (full version)
python trading_agent_assistant.py "The market is flat."
```

## Response Structure

All scripts return the same structured response:

```json
{
  "should_call_trading_agent": true|false,
  "comment": "Explanation of the decision"
}
```

- `should_call_trading_agent`: Boolean indicating if the trading agent should be activated
- `comment`: Brief reasoning for the decision

## Common Use Cases

### 1. Integration Testing
Use the shell scripts for quick integration tests:
```bash
# Quick health check and request
./trading_request_verbose.sh
```

### 2. Batch Processing
Process multiple events with the Python script:
```bash
for event in "Market crash!" "All stable" "Fed announcement"; do
    python trading_agent_assistant.py "$event"
done
```

### 3. Monitoring
Integrate into monitoring systems to evaluate market conditions:
```bash
# Cron job example
*/5 * * * * /path/to/trading_request.sh >> /var/log/trading_decisions.log
```

## Tips

- Shell scripts are ideal for quick tests and CI/CD pipelines
- Python scripts offer more flexibility and error handling
- Set `VERBOSE=1` to debug issues
- All scripts check server health before making requests
- Responses are consistently structured for easy parsing