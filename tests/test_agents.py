import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app
from memory import RedisMemory
from agents import ResearcherAgent, CoderAgent


@pytest.fixture
def mock_memory():
    """Create a mock Redis memory for testing."""
    memory = Mock(spec=RedisMemory)
    memory.set.return_value = True
    memory.get.return_value = None
    memory.delete.return_value = True
    memory.exists.return_value = False
    return memory


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "agents" in data


def test_list_agents(client):
    """Test listing all agents."""
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert isinstance(data["agents"], list)


def test_execute_agent_invalid_name(client):
    """Test executing a non-existent agent."""
    response = client.post(
        "/agents/invalid_agent/execute",
        json={"task": "Test task"}
    )
    # Should return 404 or 503 depending on Redis connection
    assert response.status_code in [404, 503]


def test_researcher_agent(mock_memory):
    """Test the Researcher agent."""
    agent = ResearcherAgent(mock_memory)
    
    task = {"task": "Research AI trends"}
    result = agent.execute(task)
    
    assert "query" in result
    assert "key_findings" in result
    assert "summary" in result
    assert result["query"] == "Research AI trends"


def test_coder_agent(mock_memory):
    """Test the Coder agent."""
    agent = CoderAgent(mock_memory)
    
    task = {"task": "Create a Python function"}
    result = agent.execute(task)
    
    assert "code" in result
    assert "language" in result
    assert "files_generated" in result
    assert result["language"] == "python"


def test_agent_retry_logic(mock_memory):
    """Test that agents have retry logic."""
    agent = ResearcherAgent(mock_memory)
    
    # Test that the agent has retry capability
    assert hasattr(agent, "_retry_wrapper")
    assert agent.max_retries == 3


def test_agent_process_task(mock_memory):
    """Test the process_task method with error handling."""
    agent = ResearcherAgent(mock_memory)
    
    task = {"task": "Test task", "task_id": "test_123"}
    result = agent.process_task(task)
    
    assert "status" in result
    assert "task_id" in result
    assert "agent" in result
    assert result["agent"] == "Researcher"


def test_agent_status(mock_memory):
    """Test getting agent status."""
    agent = ResearcherAgent(mock_memory)
    
    status = agent.get_status()
    
    assert "agent" in status
    assert "status" in status
    assert "timestamp" in status
    assert status["agent"] == "Researcher"


def test_agent_context_sharing(mock_memory):
    """Test that agents can share context."""
    agent = ResearcherAgent(mock_memory)
    
    # Test set_context
    agent.set_context("test_key", {"data": "test"})
    mock_memory.set.assert_called()
    
    # Test get_context
    agent.get_context("test_key")
    mock_memory.get.assert_called()
