#!/bin/bash

# Structured Outputs API Docker Compose Helper Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compose file
COMPOSE_FILE="docker-compose.prod.yml"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}Please add your OPENAI_API_KEY to .env file${NC}"
fi

case "$1" in
    up)
        echo -e "${GREEN}Starting Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE up -d
        echo -e "${GREEN}API available at: http://localhost:7070${NC}"
        ;;
    down)
        echo -e "${YELLOW}Stopping Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE down
        ;;
    build)
        echo -e "${GREEN}Building Structured Outputs API...${NC}"
        docker compose -f $COMPOSE_FILE build
        ;;
    logs)
        docker compose -f $COMPOSE_FILE logs -f
        ;;
    restart)
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
    *)
        echo "Usage: $0 {up|down|build|logs|restart|status|test}"
        echo ""
        echo "Commands:"
        echo "  up       - Start the API server in background"
        echo "  down     - Stop the API server"
        echo "  build    - Build the Docker image"
        echo "  logs     - Show and follow logs"
        echo "  restart  - Restart the API server"
        echo "  status   - Show container status"
        echo "  test     - Test API health endpoint"
        exit 1
        ;;
esac