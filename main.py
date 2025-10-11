from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
from memory import RedisMemory
from agents import (
    ResearcherAgent, CoderAgent, PlannerAgent, ValidatorAgent,
    DesignerAgent, AnalystAgent, SecurityAgent, DeployerAgent, MonitorAgent
)

app = FastAPI(
    title="Multi-Agent AI System",
    description="A sophisticated multi-agent system with REST API communication",
    version="1.0.0"
)

# Initialize Redis memory
try:
    memory = RedisMemory()
except Exception as e:
    print(f"Warning: Redis connection failed: {e}")
    print("Make sure Redis is running. You can start it with: docker run -d -p 6379:6379 redis:alpine")
    memory = None

# Initialize agents
agents = {}
if memory:
    agents = {
        "researcher": ResearcherAgent(memory),
        "coder": CoderAgent(memory),
        "planner": PlannerAgent(memory),
        "validator": ValidatorAgent(memory),
        "designer": DesignerAgent(memory),
        "analyst": AnalystAgent(memory),
        "security": SecurityAgent(memory),
        "deployer": DeployerAgent(memory),
        "monitor": MonitorAgent(memory)
    }


class TaskRequest(BaseModel):
    task: str
    task_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ContextRequest(BaseModel):
    value: Any


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Multi-Agent AI System",
        "agents": list(agents.keys()),
        "redis_connected": memory is not None
    }


@app.post("/agents/{agent_name}/execute")
async def execute_agent(agent_name: str, request: TaskRequest):
    """Execute a task using a specific agent."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    if agent_name not in agents:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available agents: {list(agents.keys())}"
        )
    
    agent = agents[agent_name]
    task_data = {
        "task": request.task,
        "task_id": request.task_id,
        "metadata": request.metadata or {}
    }
    
    result = agent.process_task(task_data)
    return result


@app.get("/agents/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """Get the current status of an agent."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    if agent_name not in agents:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available agents: {list(agents.keys())}"
        )
    
    agent = agents[agent_name]
    return agent.get_status()


@app.get("/agents")
async def list_agents():
    """List all available agents."""
    return {
        "agents": [
            {
                "name": name,
                "status": agent.get_status() if memory else {"status": "unavailable"}
            }
            for name, agent in agents.items()
        ]
    }


@app.get("/context/{key}")
async def get_context(key: str):
    """Retrieve shared context from memory."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    value = memory.get(f"context:{key}")
    if value is None:
        raise HTTPException(status_code=404, detail=f"Context key '{key}' not found")
    
    return {"key": key, "value": value}


@app.post("/context/{key}")
async def set_context(key: str, request: ContextRequest):
    """Store shared context in memory."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    success = memory.set(f"context:{key}", request.value)
    return {"key": key, "success": success}


@app.delete("/context/{key}")
async def delete_context(key: str):
    """Delete a context key from memory."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    success = memory.delete(f"context:{key}")
    if not success:
        raise HTTPException(status_code=404, detail=f"Context key '{key}' not found")
    
    return {"key": key, "deleted": success}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a specific task."""
    if not memory:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    
    status = memory.get(f"task:{task_id}:status")
    if not status:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    
    task_info = {
        "task_id": task_id,
        "status": status,
        "agent": memory.get(f"task:{task_id}:agent"),
        "started_at": memory.get(f"task:{task_id}:started_at"),
        "completed_at": memory.get(f"task:{task_id}:completed_at"),
        "failed_at": memory.get(f"task:{task_id}:failed_at"),
        "result": memory.get(f"task:{task_id}:result"),
        "error": memory.get(f"task:{task_id}:error")
    }
    
    return task_info


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
