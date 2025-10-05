# Multi-Agent AI System

A sophisticated multi-agent AI system built with FastAPI, Redis, and Docker. The system consists of 9 specialized agents that communicate via REST APIs and share context through Redis memory.

## Agents

1. **Researcher** - Gathers and analyzes data
2. **Coder** - Writes and generates code
3. **Planner** - Schedules and organizes tasks
4. **Validator** - Tests and validates output
5. **Designer** - Creates UI/UX designs
6. **Analyst** - Processes metrics and analytics
7. **Security** - Audits security risks
8. **Deployer** - Manages CI/CD pipelines
9. **Monitor** - Tracks system performance

## Architecture

- **FastAPI**: REST API for agent communication
- **Redis**: Shared memory and context storage
- **Docker**: Containerized deployment
- **Retry Logic**: Built-in retry mechanism for resilience
- **Error Handling**: Comprehensive error handling across all agents

## Setup

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Redis

### Installation

1. Clone the repository:
```bash
git clone https://github.com/StayUp90/StayUpAgents.git
cd StayUpAgents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run with Docker:
```bash
docker-compose up -d
```

4. Run locally:
```bash
# Start Redis
docker run -d -p 6379:6379 redis:alpine

# Start the API server
python main.py
```

## API Endpoints

- `GET /` - Health check
- `POST /agents/{agent_name}/execute` - Execute an agent task
- `GET /agents/{agent_name}/status` - Get agent status
- `GET /context/{key}` - Get shared context
- `POST /context/{key}` - Set shared context

## Usage Example

```python
import requests

# Execute a research task
response = requests.post(
    "http://localhost:8000/agents/researcher/execute",
    json={"task": "Research Python best practices"}
)

# Get the result
print(response.json())
```

## Development

Run tests:
```bash
pytest tests/
```

## License

MIT License
