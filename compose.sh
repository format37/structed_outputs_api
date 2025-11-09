#!/bin/bash

# Structured Outputs API Docker Compose Helper Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compose file
COMPOSE_FILE="docker-compose.prod.yml"

# Function to check .env file
check_env() {
    if [ ! -f .env ]; then
        echo -e "${RED}ERROR: .env file not found!${NC}"
        echo -e "${YELLOW}Please create .env file with your OpenAI API key:${NC}"
        echo ""
        echo "  cp .env.example .env"
        echo "  # Then edit .env and add your actual OPENAI_API_KEY"
        echo ""
        return 1
    fi

    # Check if API key is set properly
    if grep -q "your_openai_api_key_here\|your_key" .env 2>/dev/null; then
        echo -e "${RED}ERROR: .env file contains placeholder API key!${NC}"
        echo -e "${YELLOW}Please edit .env and add your actual OpenAI API key${NC}"
        return 1
    fi

    if ! grep -q "OPENAI_API_KEY=" .env 2>/dev/null; then
        echo -e "${RED}ERROR: OPENAI_API_KEY not found in .env file!${NC}"
        return 1
    fi

    return 0
}

case "$1" in
    up)
        if ! check_env; then
            exit 1
        fi
        echo -e "${GREEN}Starting Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE up -d
        echo -e "${GREEN}API available at: http://localhost:7070${NC}"
        ;;
    down)
        echo -e "${YELLOW}Stopping Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE down
        ;;
    build)
        if ! check_env; then
            exit 1
        fi
        echo -e "${GREEN}Building Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE build
        ;;
    logs)
        docker compose -f $COMPOSE_FILE logs -f
        ;;
    restart)
        if ! check_env; then
            exit 1
        fi
        echo -e "${YELLOW}Restarting Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE restart
        ;;
    status)
        docker compose -f $COMPOSE_FILE ps
        ;;
    test)
        echo -e "${GREEN}Testing API health...${NC}"
        curl -s http://localhost:7070/health | python -m json.tool || echo -e "${RED}API not responding${NC}"
        ;;
    dev)
        # Development mode - runs without Docker
        if ! check_env; then
            exit 1
        fi
        echo -e "${GREEN}Starting API in development mode...${NC}"
        python api_server.py
        ;;
    *)
        echo "Usage: $0 {up|down|build|logs|restart|status|test|dev}"
        echo ""
        echo "Commands:"
        echo "  up       - Start the API server in background (production)"
        echo "  down     - Stop the API server"
        echo "  build    - Build the Docker image"
        echo "  logs     - Show and follow logs"
        echo "  restart  - Restart the API server"
        echo "  status   - Show container status"
        echo "  test     - Test API health endpoint"
        echo "  dev      - Run API in development mode (no Docker)"
        exit 1
        ;;
esac