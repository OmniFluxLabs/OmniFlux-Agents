# 🤖 OmniFlux Agents - Multi-Agent AI System

**Developed by OmniFlux Labs**

A powerful, extensible multi-agent AI system where specialized agents collaborate to solve complex tasks. Built with Python using a clean **MVC architecture**, featuring AI integration, web interface, and real-time WebSocket capabilities.

## 🏗️ Architecture

OmniFlux Agents has been refactored to use a **Model-View-Controller (MVC)** architecture pattern with specialized controllers, achieving:

- ✅ **73% code reduction** in main application (530 → 143 lines)
- ✅ **9 specialized controllers** managing 22 API endpoints
- ✅ **92.5% average test coverage** across all controllers
- ✅ **Clean separation of concerns** for better maintainability
- ✅ **Real-time WebSocket** for live workflow updates

### Controller Organization

```
web_interface/
├── app.py                    # Main FastAPI application (143 lines)
└── controllers/
    ├── health.py            # Health checks (2 endpoints)
    ├── statistics.py        # System statistics (1 endpoint)
    ├── agents.py            # Agent management (3 endpoints)
    ├── workflows.py         # Workflow execution (4 endpoints)
    ├── templates.py         # Template management (3 endpoints)
    ├── schedules.py         # Scheduled workflows (2 endpoints)
    ├── settings.py          # Configuration (4 endpoints)
    ├── websocket.py         # Real-time updates (1 endpoint)
    └── dashboard.py         # Dashboard data (2 endpoints)
```

📖 **[View Complete Architecture Documentation →](ARCHITECTURE.md)**

### Key Benefits

| Benefit | Impact |
|---------|--------|
| **Separation of Concerns** | Each controller handles specific domain logic |
| **Testability** | Controllers tested independently (92.5% coverage) |
| **Maintainability** | Changes isolated to relevant controllers |
| **Scalability** | Easy to add new controllers for new features |
| **Code Organization** | Clear structure with logical grouping |

## ✨ Features

### 🧠 **Core Multi-Agent System**
- **Planner Agent**: Breaks down complex tasks into manageable subtasks
- **Researcher Agent**: Gathers and analyzes information from various sources
- **Coder Agent**: Implements solutions with clean, tested code
- **Reviewer Agent**: Provides quality assurance and feedback
- **Coordinator Agent**: Manages workflows and orchestrates agent collaboration

### 🚀 **Advanced Features**
- **AI Integration**: Support for OpenAI GPT, Anthropic Claude, and Google Gemini
- **Web Interface**: Modern, responsive dashboard for managing agents and workflows
- **CLI Interface**: Command-line tools for developers and automation
- **Real-time Updates**: WebSocket support for live workflow monitoring
- **Docker Support**: Containerized deployment with Docker Compose
- **Extensible Architecture**: Easy to add new agent types and capabilities

### 🔧 **Technical Highlights**
- **Async/Await**: Built on Python asyncio for high performance
- **Type Safety**: Full type hints and Pydantic models
- **Testing**: Comprehensive test suite with pytest
- **Configuration**: Flexible JSON-based configuration system
- **Logging**: Structured logging with multiple output formats
- **Error Handling**: Robust error handling and retry mechanisms

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/OmniFluxLabs/OmniFluxAgents.git
cd OmniFluxAgents
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up the database (Optional but recommended)**
```bash
# Initialize database and create tables
python setup_database.py --init

# Or reset database if needed (WARNING: deletes all data)
python setup_database.py --reset
```

4. **Run the basic example**
```bash
python example_basic.py
```

### 🎮 **Using the CLI**

```bash
# Show system status
python cli.py status

# Run a basic workflow
python cli.py run "Build a weather application"

# Run with AI enhancement (requires API keys)
python cli.py ai "Create a data analysis tool"

# Interactive mode
python cli.py --interactive
```

### 🌐 **Using the Web Interface**

1. **Start the web server**
```bash
# Start with standard controllers
python run_web.py

# Or start with extended features
python run_web_extended.py
```

2. **Access the dashboard**
- **Main Dashboard**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

3. **Start workflows**
Use the dashboard to create and monitor agent workflows in real-time via WebSocket connections

4. **Use the REST API**
```bash
# Check system health
curl http://localhost:8000/health

# Get statistics
curl http://localhost:8000/api/statistics

# Start a workflow
curl -X POST http://localhost:8000/api/workflows/start \
  -H "Content-Type: application/json" \
  -d '{"description": "Build a calculator", "use_ai": true}'
```

### 🐳 **Docker Deployment**

1. **Using Docker Compose (Recommended)**
```bash
docker-compose up -d
```

2. **Using Docker directly**
```bash
docker build -t omniflux-agents .
docker run -p 8000:8000 omniflux-agents
```

## 📖 Detailed Usage

### Basic Workflow via Web API

```python
import requests

# Start a workflow
response = requests.post('http://localhost:8000/api/workflows/start', json={
    "description": "Build a web scraping tool with data visualization",
    "use_ai": True,
    "priority": "high"
})

workflow_id = response.json()['workflow_id']
print(f"Workflow started: {workflow_id}")

# Check workflow status
status = requests.get(f'http://localhost:8000/api/workflows/{workflow_id}')
print(f"Status: {status.json()}")

# Get all workflows
workflows = requests.get('http://localhost:8000/api/workflows/')
print(f"Total workflows: {len(workflows.json())}")
```

### Using Controllers Directly

```python
from web_interface.controllers.workflows import start_workflow, get_workflow
from web_interface.controllers.agents import create_agent, list_agents

# Start a workflow using the controller
workflow_request = {
    "description": "Build a REST API",
    "use_ai": True,
    "priority": "high"
}
result = start_workflow(workflow_request)
print(f"Workflow ID: {result['workflow_id']}")

# Create a custom agent
agent_data = {
    "name": "DataAnalyzer",
    "role": "data_analyst",
    "specialization": "Financial data analysis"
}
agent = create_agent(agent_data)
print(f"Agent created: {agent['name']}")

# List all agents
agents = list_agents()
print(f"Total agents: {len(agents)}")
```

### AI-Enhanced Agents

```python
from ai_integration import AIManager
from extended_agents import ExtendedAgentFactory

# Initialize AI manager
ai_manager = AIManager()

# Create enhanced agent with AI capabilities
researcher = EnhancedAgent(
    name="AI Researcher",
    role="researcher",
    ai_manager=ai_manager
)

# Process task with AI
result = await researcher.process_with_ai(
    "Research the latest trends in machine learning"
)
```

### WebSocket Real-time Updates

```javascript
// Connect to WebSocket for live updates
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
    console.log('Connected to OmniFlux Agents WebSocket');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'workflow_started':
            console.log('New workflow:', data.workflow_id);
            break;
        case 'task_completed':
            console.log('Task completed:', data.task_id);
            break;
        case 'workflow_completed':
            console.log('Workflow finished:', data.workflow_id);
            break;
        case 'agent_created':
            console.log('New agent:', data.agent_name);
            break;
        case 'settings_updated':
            console.log('Settings changed');
            break;
    }
};
```

### Custom Agent

```python
from omniflux_agents_main import Agent, AgentRole

class CustomAgent(Agent):
    def __init__(self, name: str = "CustomAgent"):
        super().__init__(name, AgentRole.RESEARCHER)
    
    async def process_task(self, task):
        # Your custom logic here
        return {"result": "Custom processing completed"}

# Register with the system
from web_interface.controllers.agents import register_custom_agent
register_custom_agent(CustomAgent)

## ⚙️ Configuration

OmniFlux Agents uses a robust configuration management system that supports different environments (development, production) and allows for flexible configuration access.

### Environment-Based Configuration

Configuration files are stored in the `config` directory with naming convention `config_<environment>.json`, such as:
- `config/config_development.json` - Used in development environment
- `config/config_production.json` - Used in production environment

The environment can be specified through:
1. Environment variable: `ENVIRONMENT=production`
2. Command-line argument: `--env production`
3. Programmatically: `set_environment("production")`

### Environment Variables in Configuration

Configuration files support environment variable substitution using the pattern `${VARIABLE_NAME}`:

```json
{
  "security": {
    "jwt_secret": "${JWT_SECRET}"
  }
}
```

### Using the Configuration System

#### In Python code:
```python
# Import the configuration manager
from config_manager import get_config_value, get_config, set_environment

# Get a specific configuration value using dot notation
log_level = get_config_value("logging.level", "INFO")
max_tasks = get_config_value("system.max_concurrent_tasks", 5)

# Get the entire configuration dictionary
config = get_config()

# Change the environment
set_environment("production")
```

#### From command line:
```bash
# Run with specific environment
python run_web.py --env production

# Run with specific log level
python run_web.py --log-level DEBUG

# Run with custom config file
python run_web.py --config-path my_config.json
```

### Configuration File Structure

The configuration file follows this structure:

```json
{
  "system": {
    "name": "OmniFlux Agents",
    "version": "1.0.0",
    "environment": "development",
    "log_level": "INFO",
    "max_concurrent_tasks": 10,
    "task_timeout": 3600
  },
  "storage": {
    "type": "database",
    "database": {
      "type": "sqlite",
      "name": "omniflux_agents.db",
      "path": "./data/omniflux_agents.db"
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/omniflux_agents.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "max_file_size_mb": 10,
    "backup_count": 5
  },
  "agents": {
    "researcher": {
      "enabled": true,
      "max_search_results": 10,
      "cache_results": true
    },
    "coder": {
      "enabled": true,
      "language": "python",
      "auto_format": true
    }
  },
  "web_interface": {
    "enabled": true,
    "host": "0.0.0.0",
    "port": 8000,
    "reload": false
  }
}
```

### Database Management

The system supports persistent storage using SQLAlchemy with SQLite (default) or PostgreSQL/MySQL.

```bash
# Initialize database
python setup_database.py --init

# View database statistics
python setup_database.py --stats

# Export data to JSON
python setup_database.py --export

# Create backup
python setup_database.py --backup

# Reset database (WARNING: deletes all data)
python setup_database.py --reset
```

## 🧪 Testing

OmniFlux Agents has comprehensive test coverage across all controllers.

### Test Coverage Summary

| Controller | Tests | Coverage | Status |
|------------|-------|----------|--------|
| health.py | 12 | 100% | ✅ Excellent |
| statistics.py | 8 | 95% | ✅ Excellent |
| agents.py | 25 | 92% | ✅ Excellent |
| workflows.py | 35 | 90% | ✅ Good |
| templates.py | 30 | 93% | ✅ Excellent |
| schedules.py | 20 | 91% | ✅ Excellent |
| settings.py | 28 | 94% | ✅ Excellent |
| websocket.py | 15 | 85% | ✅ Good |
| dashboard.py | 12 | 95% | ✅ Excellent |
| **Average** | **180+** | **92.5%** | **✅ Excellent** |

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=web_interface --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_workflows.py -v

# Run tests for specific controller
pytest tests/test_agents.py::TestAgentController -v
```

### Test Files Structure

```
tests/
├── test_health.py          # Health endpoint tests
├── test_statistics.py      # Statistics endpoint tests
├── test_agents.py          # Agent management tests
├── test_workflows.py       # Workflow execution tests
├── test_templates.py       # Template management tests
├── test_schedules.py       # Scheduled workflow tests
├── test_settings.py        # Settings management tests
├── test_websocket.py       # WebSocket connection tests
└── test_dashboard.py       # Dashboard endpoint tests
```

📖 **[View Complete Testing Documentation →](PHASE2_COMPLETE.md)**

## 📊 API Reference

OmniFlux Agents provides a comprehensive REST API with 22 endpoints across 9 controllers.

### Quick API Overview

**System Endpoints:**
- `GET /health` - Basic health check
- `GET /api/status` - Detailed system status
- `GET /api/statistics` - System-wide statistics

**Agent Management:**
- `GET /api/agents/` - List all agents
- `POST /api/agents/` - Create new agent
- `GET /api/agents/roles` - Get available roles

**Workflow Management:**
- `POST /api/workflows/start` - Start new workflow
- `GET /api/workflows/` - List workflows (50 most recent)
- `GET /api/workflows/{workflow_id}` - Get workflow details
- `DELETE /api/workflows/{workflow_id}` - Delete workflow

**Template Management:**
- `GET /api/templates/` - List all templates
- `POST /api/templates/` - Create custom template
- `GET /api/templates/categories` - Get template categories

**Scheduling:**
- `GET /api/scheduled/` - List scheduled workflows
- `POST /api/scheduled/` - Create scheduled workflow

**Settings:**
- `GET /api/settings/` - Get current settings
- `PUT /api/settings/` - Update settings
- `POST /api/settings/reload` - Reload from files
- `GET /api/settings/schema` - Get settings schema

**Dashboard:**
- `GET /api/dashboard/` - Get dashboard summary
- `GET /api/dashboard/stats` - Get dashboard statistics

**Real-time:**
- `WS /ws` - WebSocket connection for live updates

### Interactive Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Examples

**Start a Workflow:**
```bash
curl -X POST http://localhost:8000/api/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build a REST API",
    "use_ai": true,
    "priority": "high"
  }'
```

**Get Workflow Status:**
```bash
curl http://localhost:8000/api/workflows/workflow_20241010_103000
```

**Create Custom Agent:**
```bash
curl -X POST http://localhost:8000/api/agents/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DataAnalyzer",
    "role": "data_analyst",
    "specialization": "Financial analysis"
  }'
```

**WebSocket Connection (JavaScript):**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'workflow_completed') {
    console.log('Workflow completed:', data.workflow_id);
  }
};
```

📖 **[View Complete API Documentation →](API_REFERENCE.md)**

## 🚀 Deployment

### Production Deployment

1. **Using Docker Compose (Recommended)**
```bash
# Production deployment
docker-compose -f docker-compose.yml up -d

# With custom configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

2. **Using the deployment script**
```bash
# Linux/Mac
./deploy.sh

# Windows
deploy.bat
```

3. **Manual deployment**
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python setup_database.py --init

# Start web interface (MVC architecture)
python run_web.py

# Or start with extended features
python run_web_extended.py

# Or with specific configuration
ENVIRONMENT=production python run_web.py
```

### Environment-Specific Configuration

#### Development
```bash
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEBUG=true
```

#### Production
```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false
```

### Health Checks

The MVC architecture provides multiple health check endpoints:

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system status
curl http://localhost:8000/api/status

# Get system statistics
curl http://localhost:8000/api/statistics
```

📖 **[View Complete Deployment Guide →](DEPLOYMENT.md)**

## 🔧 Development

### Project Structure (MVC Architecture)

```
OmniFluxAgents/
├── web_interface/
│   ├── app.py                     # Main FastAPI app (143 lines)
│   ├── controllers/               # MVC Controllers
│   │   ├── health.py             # Health check endpoints
│   │   ├── statistics.py         # Statistics endpoints
│   │   ├── agents.py             # Agent management
│   │   ├── workflows.py          # Workflow execution
│   │   ├── templates.py          # Template management
│   │   ├── schedules.py          # Scheduled workflows
│   │   ├── settings.py           # Configuration management
│   │   ├── websocket.py          # WebSocket connections
│   │   └── dashboard.py          # Dashboard data
│   ├── templates/                # HTML templates (View)
│   └── static/                   # Static files (CSS/JS)
├── database/
│   ├── models.py                 # Database models
│   └── connection.py             # Database connection
├── tests/
│   ├── test_health.py            # Controller tests
│   ├── test_statistics.py
│   ├── test_agents.py
│   ├── test_workflows.py
│   ├── test_templates.py
│   ├── test_schedules.py
│   ├── test_settings.py
│   ├── test_websocket.py
│   └── test_dashboard.py
├── omniflux_agents_main.py       # Core agent system (Model)
├── ai_integration.py             # AI provider integrations
├── cli.py                        # Command line interface
├── config.json                   # Configuration
├── requirements.txt              # Dependencies
├── Dockerfile                    # Docker configuration
└── docker-compose.yml            # Docker Compose
```

### Adding New Controllers

1. **Create the controller file**
```python
# web_interface/controllers/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/my-feature", tags=["my-feature"])

@router.get("/")
async def list_items():
    """List all items"""
    return {"items": []}

@router.post("/")
async def create_item(data: dict):
    """Create new item"""
    return {"id": "new_item_id"}
```

2. **Register in app.py**
```python
# web_interface/app.py
from web_interface.controllers import my_feature

app.include_router(my_feature.router)
```

3. **Add tests**
```python
# tests/test_my_feature.py
from fastapi.testclient import TestClient
from web_interface.app import app

client = TestClient(app)

def test_list_items():
    response = client.get("/api/my-feature/")
    assert response.status_code == 200
```

### Adding New Agents

1. **Create the agent class**
```python
from omniflux_agents_main import Agent, AgentRole

class MyCustomAgent(Agent):
    def __init__(self, name: str = "MyCustomAgent"):
        super().__init__(name, AgentRole.RESEARCHER)  # Or create new role
    
    async def process_task(self, task):
        # Implement your logic
        return {"custom_result": "Success"}
```

2. **Add to the system**
```python
system.add_agent(MyCustomAgent("CustomAgent"))
```

### Adding New AI Providers

1. **Implement the provider**
```python
from ai_integration import AIProvider

class MyAIProvider(AIProvider):
    async def generate_response(self, prompt: str, **kwargs):
        # Implement API call
        return AIResponse(content="Response", provider="my_provider", model="my_model")
```

2. **Register with AIManager**
```python
ai_manager.providers["my_provider"] = MyAIProvider(api_key, model)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Clone your fork**
```bash
git clone https://github.com/OmniFluxLabs/OmniFluxAgents.git
cd OmniFluxAgents
```

3. **Install development dependencies**
```bash
pip install -r requirements.txt
pip install -e .
```

4. **Run tests**
```bash
# Run all controller tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=web_interface --cov-report=html --cov-report=term

# Run specific controller tests
pytest tests/test_workflows.py -v

# Run tests in parallel
pytest tests/ -n auto
```

5. **Make your changes and test**
   - Follow the MVC architecture pattern
   - Add controller tests to relevant files in `tests/`
   - Aim for 90%+ test coverage on new code
   - Update documentation in relevant files

6. **Submit a pull request**
   - Ensure all tests pass (92.5%+ coverage)
   - Update API_REFERENCE.md if adding new endpoints
   - Update ARCHITECTURE.md if changing structure
   - Follow commit message conventions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Google for Gemini models
- FastAPI for the web framework
- The Python community for excellent libraries

## 📞 Support

- **Documentation**: [Wiki](https://github.com/OmniFluxLabs/OmniFluxAgents/wiki)
- **Issues**: [GitHub Issues](https://github.com/OmniFluxLabs/OmniFluxAgents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OmniFluxLabs/OmniFluxAgents/discussions)
- **Email**: support@omnifluxlabs.com

---

**Made with ❤️ by OmniFlux Labs**