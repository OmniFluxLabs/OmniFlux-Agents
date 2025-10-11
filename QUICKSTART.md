# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- Docker (optional, but recommended)

## Option 1: Run with Docker (Recommended)

This will start both the API server and Redis automatically.

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The API will be available at `http://localhost:8000`

## Option 2: Run Locally

### Step 1: Start Redis

```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install Redis locally and start it
redis-server
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start the API Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Usage

### Interactive API Documentation

Visit `http://localhost:8000/docs` in your browser to see the interactive Swagger UI.

### Using the Example Script

```bash
python example.py
```

This will demonstrate all 9 agents in action.

### Using cURL

```bash
# Health check
curl http://localhost:8000/

# List all agents
curl http://localhost:8000/agents

# Execute a research task
curl -X POST http://localhost:8000/agents/researcher/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Research Python best practices"}'

# Get agent status
curl http://localhost:8000/agents/researcher/status

# Get shared context
curl http://localhost:8000/context/latest_research
```

### Using Python

```python
import requests

# Execute a task
response = requests.post(
    "http://localhost:8000/agents/researcher/execute",
    json={"task": "Research AI trends", "task_id": "research_123"}
)
print(response.json())

# Get task status
response = requests.get("http://localhost:8000/tasks/research_123")
print(response.json())
```

## Available Agents

1. **researcher** - Gathers and analyzes data
2. **coder** - Writes and generates code
3. **planner** - Schedules and organizes tasks
4. **validator** - Tests and validates output
5. **designer** - Creates UI/UX designs
6. **analyst** - Processes metrics and analytics
7. **security** - Audits security risks
8. **deployer** - Manages CI/CD pipelines
9. **monitor** - Tracks system performance

## Agent Communication

Agents can share context through Redis:

1. **Researcher** stores research data → **Coder** uses it to generate code
2. **Coder** stores code → **Validator** tests it
3. **Validator** stores results → **Deployer** uses them to deploy
4. **Deployer** stores deployment info → **Monitor** tracks it

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## Troubleshooting

### Redis Connection Error

If you see "Redis connection failed":

1. Make sure Redis is running
2. Check that it's accessible on `localhost:6379`
3. Or update the environment variables:
   ```bash
   export REDIS_HOST=your-redis-host
   export REDIS_PORT=6379
   ```

### Port Already in Use

If port 8000 is already in use:

```bash
# Change the port in main.py or use environment variable
export API_PORT=8080
python main.py
```

## Development

### Project Structure

```
StayUpAgents/
├── agents/
│   ├── __init__.py          # All 9 agent implementations
│   └── base_agent.py        # Base agent class with retry logic
├── tests/
│   ├── test_agents.py       # Agent tests
│   └── test_memory.py       # Memory tests
├── main.py                  # FastAPI application
├── memory.py                # Redis memory manager
├── example.py               # Usage examples
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-container setup
└── README.md                # Documentation
```

### Adding a New Agent

1. Create a new agent class in `agents/__init__.py`:
   ```python
   class MyAgent(BaseAgent):
       def __init__(self, memory: RedisMemory):
           super().__init__("MyAgent", memory)
       
       def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
           # Your implementation
           return {"result": "success"}
   ```

2. Register it in `main.py`:
   ```python
   agents["myagent"] = MyAgent(memory)
   ```

3. Add tests in `tests/test_agents.py`

## Features

✅ 9 specialized AI agents  
✅ FastAPI REST API  
✅ Redis for shared memory  
✅ Docker deployment  
✅ Retry logic with exponential backoff  
✅ Comprehensive error handling  
✅ Context sharing between agents  
✅ Task tracking and status  
✅ Full test coverage  
✅ Interactive API documentation  

## Next Steps

- Integrate with real AI models (OpenAI, Anthropic, etc.)
- Add authentication and authorization
- Implement rate limiting
- Add more sophisticated agent orchestration
- Create a web UI dashboard
- Add metrics and monitoring with Prometheus
- Implement agent-to-agent direct communication
