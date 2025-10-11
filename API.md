# API Documentation

## Base URL

```
http://localhost:8000
```

When deployed, replace with your actual domain.

## Authentication

Currently, the API is open. For production, implement authentication using:
- JWT tokens
- API keys
- OAuth 2.0

## Endpoints

### Health Check

#### `GET /`

Check if the API is running and get system status.

**Response:**
```json
{
  "status": "online",
  "service": "Multi-Agent AI System",
  "agents": ["researcher", "coder", "planner", ...],
  "redis_connected": true
}
```

**Status Codes:**
- `200 OK`: Service is running

---

### List All Agents

#### `GET /agents`

Get a list of all available agents and their current status.

**Response:**
```json
{
  "agents": [
    {
      "name": "researcher",
      "status": {
        "agent": "Researcher",
        "status": "idle",
        "timestamp": "2024-01-01T12:00:00"
      }
    },
    ...
  ]
}
```

**Status Codes:**
- `200 OK`: Success

---

### Execute Agent Task

#### `POST /agents/{agent_name}/execute`

Execute a task using a specific agent.

**Path Parameters:**
- `agent_name` (string): Name of the agent to use
  - Available: `researcher`, `coder`, `planner`, `validator`, `designer`, `analyst`, `security`, `deployer`, `monitor`

**Request Body:**
```json
{
  "task": "Your task description",
  "task_id": "optional-task-id",
  "metadata": {
    "key": "value"
  }
}
```

**Response (Success):**
```json
{
  "status": "success",
  "task_id": "research_001",
  "agent": "Researcher",
  "result": {
    "query": "Your task description",
    "sources_analyzed": 10,
    "key_findings": [...],
    "summary": "...",
    "confidence": 0.85
  }
}
```

**Response (Error):**
```json
{
  "status": "error",
  "task_id": "research_001",
  "agent": "Researcher",
  "error": "Error message"
}
```

**Status Codes:**
- `200 OK`: Task executed (check status field for success/error)
- `404 Not Found`: Agent not found
- `503 Service Unavailable`: Redis not connected

**Examples:**

```bash
# Researcher
curl -X POST http://localhost:8000/agents/researcher/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Research AI trends in 2024"}'

# Coder
curl -X POST http://localhost:8000/agents/coder/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Create a REST API in Python"}'

# Security
curl -X POST http://localhost:8000/agents/security/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Audit API security"}'
```

---

### Get Agent Status

#### `GET /agents/{agent_name}/status`

Get the current status of a specific agent.

**Path Parameters:**
- `agent_name` (string): Name of the agent

**Response:**
```json
{
  "agent": "Researcher",
  "status": "idle",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Status Codes:**
- `200 OK`: Success
- `404 Not Found`: Agent not found
- `503 Service Unavailable`: Redis not connected

---

### Get Context

#### `GET /context/{key}`

Retrieve shared context from memory.

**Path Parameters:**
- `key` (string): Context key to retrieve

**Response:**
```json
{
  "key": "latest_research",
  "value": {
    "query": "...",
    "findings": [...]
  }
}
```

**Status Codes:**
- `200 OK`: Context found
- `404 Not Found`: Key not found
- `503 Service Unavailable`: Redis not connected

---

### Set Context

#### `POST /context/{key}`

Store shared context in memory.

**Path Parameters:**
- `key` (string): Context key to set

**Request Body:**
```json
{
  "value": {
    "any": "data",
    "you": "want"
  }
}
```

**Response:**
```json
{
  "key": "my_context",
  "success": true
}
```

**Status Codes:**
- `200 OK`: Context stored
- `503 Service Unavailable`: Redis not connected

---

### Delete Context

#### `DELETE /context/{key}`

Delete a context key from memory.

**Path Parameters:**
- `key` (string): Context key to delete

**Response:**
```json
{
  "key": "my_context",
  "deleted": true
}
```

**Status Codes:**
- `200 OK`: Context deleted
- `404 Not Found`: Key not found
- `503 Service Unavailable`: Redis not connected

---

### Get Task Status

#### `GET /tasks/{task_id}`

Get the status and details of a specific task.

**Path Parameters:**
- `task_id` (string): Task ID to query

**Response:**
```json
{
  "task_id": "research_001",
  "status": "completed",
  "agent": "Researcher",
  "started_at": "2024-01-01T12:00:00",
  "completed_at": "2024-01-01T12:01:30",
  "failed_at": null,
  "result": {
    "query": "...",
    "findings": [...]
  },
  "error": null
}
```

**Status Codes:**
- `200 OK`: Task found
- `404 Not Found`: Task not found
- `503 Service Unavailable`: Redis not connected

---

## Agent-Specific Details

### Researcher Agent

**Purpose:** Gathers and analyzes data

**Input:** `task` - Research query or topic

**Output:**
```json
{
  "query": "Research topic",
  "sources_analyzed": 10,
  "key_findings": ["Finding 1", "Finding 2", ...],
  "summary": "Summary text",
  "confidence": 0.85
}
```

**Context:** Stores results as `latest_research`

---

### Coder Agent

**Purpose:** Generates code

**Input:** `task` - Code requirements

**Output:**
```json
{
  "requirements": "Requirements text",
  "code": "# Generated code...",
  "language": "python",
  "files_generated": ["main.py", "utils.py"],
  "lines_of_code": 150,
  "used_research": true
}
```

**Context:** 
- Uses `latest_research` if available
- Stores results as `latest_code`

---

### Planner Agent

**Purpose:** Creates project plans

**Input:** `task` - Project name

**Output:**
```json
{
  "project": "Project name",
  "phases": [
    {"phase": "Research", "duration": "2 days", "status": "pending"},
    ...
  ],
  "total_duration": "10 days",
  "dependencies": ["Phase1 -> Phase2", ...]
}
```

**Context:** Stores results as `project_plan`

---

### Validator Agent

**Purpose:** Tests and validates outputs

**Input:** `task` - Target to validate

**Output:**
```json
{
  "target": "Target name",
  "tests_run": 25,
  "tests_passed": 23,
  "tests_failed": 2,
  "code_coverage": 0.92,
  "quality_score": 0.88,
  "issues_found": ["Issue 1", "Issue 2"],
  "validated_code": true
}
```

**Context:**
- Uses `latest_code` if available
- Stores results as `validation_result`

---

### Designer Agent

**Purpose:** Creates UI/UX designs

**Input:** `task` - Design requirements

**Output:**
```json
{
  "requirements": "Requirements text",
  "design_system": "Material Design 3",
  "color_palette": ["#1976D2", "#424242", "#F5F5F5"],
  "components": ["Navigation", "Dashboard", ...],
  "wireframes": 8,
  "mockups": 5,
  "accessibility_score": 0.95
}
```

**Context:** Stores results as `ui_design`

---

### Analyst Agent

**Purpose:** Processes metrics and analytics

**Input:** `task` - Data source to analyze

**Output:**
```json
{
  "data_source": "Source name",
  "metrics_analyzed": 15,
  "key_metrics": {
    "performance": 0.87,
    "efficiency": 0.91,
    "user_satisfaction": 0.84
  },
  "trends": ["Trend 1", "Trend 2"],
  "recommendations": ["Rec 1", "Rec 2"]
}
```

**Context:** Stores results as `analytics_report`

---

### Security Agent

**Purpose:** Audits security risks

**Input:** `task` - Target to audit

**Output:**
```json
{
  "target": "Target name",
  "vulnerabilities_found": 2,
  "severity_levels": {
    "critical": 0,
    "high": 1,
    "medium": 1,
    "low": 0
  },
  "issues": [
    {"type": "SQL Injection", "severity": "high", "file": "database.py"},
    ...
  ],
  "compliance_score": 0.82,
  "recommendations": ["Rec 1", "Rec 2"],
  "audited_code": true
}
```

**Context:**
- Uses `latest_code` if available
- Stores results as `security_report`

---

### Deployer Agent

**Purpose:** Manages CI/CD pipelines

**Input:** `task` - Environment name (e.g., "production", "staging")

**Output:**
```json
{
  "environment": "production",
  "pipeline_status": "success",
  "stages": [
    {"stage": "Build", "status": "passed", "duration": "2m 30s"},
    {"stage": "Test", "status": "passed", "duration": "5m 10s"},
    {"stage": "Deploy", "status": "passed", "duration": "1m 45s"}
  ],
  "deployment_url": "https://production.example.com",
  "rollback_available": true,
  "validated_before_deploy": true
}
```

**Context:**
- Uses `validation_result` if available
- Stores results as `deployment_info`

---

### Monitor Agent

**Purpose:** Tracks system performance

**Input:** `task` - System to monitor (e.g., "all", "api", "database")

**Output:**
```json
{
  "system": "all",
  "uptime": "99.95%",
  "response_time_avg": "120ms",
  "error_rate": "0.02%",
  "cpu_usage": "45%",
  "memory_usage": "62%",
  "active_users": 1250,
  "alerts": [
    {"type": "warning", "message": "Memory usage approaching threshold"}
  ],
  "monitoring_deployment": true
}
```

**Context:**
- Uses `deployment_info` if available
- Stores results as `monitoring_data`

---

## Error Handling

All endpoints may return error responses:

### 400 Bad Request
Invalid request parameters

### 404 Not Found
Resource not found

### 503 Service Unavailable
Redis connection not available

### Error Response Format
```json
{
  "detail": "Error description"
}
```

---

## Rate Limiting

Currently not implemented. For production, consider:
- Limit: 100 requests per minute per IP
- Use Redis for distributed rate limiting
- Return `429 Too Many Requests` when exceeded

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for alternative ReDoc documentation.
