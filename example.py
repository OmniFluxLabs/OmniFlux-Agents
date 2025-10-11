"""
Example usage of the Multi-Agent AI System.

This script demonstrates how to use the agent system via REST API.
Make sure to start the server first:
    python main.py
Or with Docker:
    docker-compose up -d
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 30  # Default timeout for API calls in seconds


def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")
    print(json.dumps(response.json(), indent=2))


def execute_agent_task(agent_name, task, task_id, step_num, description):
    """Execute a task on a specific agent."""
    response = requests.post(
        f"{BASE_URL}/agents/{agent_name}/execute",
        json={"task": task, "task_id": task_id},
        timeout=DEFAULT_TIMEOUT
    )
    print_response(f"{step_num}. {description}", response)
    return response


def get_system_info():
    """Perform initial system checks."""
    print("Multi-Agent AI System - Example Usage")
    print("=" * 60)
    
    # Health check
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print_response("1. Health Check", response)
    
    # List all agents
    response = requests.get(f"{BASE_URL}/agents", timeout=10)
    print_response("2. List All Agents", response)


def run_research_workflow():
    """Execute research and coding workflow."""
    # Research task
    execute_agent_task(
        "researcher",
        "Research best practices for microservices architecture",
        "research_001",
        3,
        "Researcher Agent - Execute Research"
    )
    
    # Get research context
    time.sleep(0.5)
    response = requests.get(f"{BASE_URL}/context/latest_research", timeout=5)
    print_response("4. Get Research Context", response)
    
    # Coding task
    execute_agent_task(
        "coder",
        "Create a microservice skeleton in Python",
        "code_001",
        5,
        "Coder Agent - Generate Code"
    )


def run_planning_workflow():
    """Execute planning and validation workflow."""
    # Planning task
    execute_agent_task(
        "planner",
        "Plan microservice deployment",
        "plan_001",
        6,
        "Planner Agent - Create Project Plan"
    )
    
    # Validation task
    execute_agent_task(
        "validator",
        "Validate generated code",
        "validate_001",
        7,
        "Validator Agent - Test Code"
    )


def run_design_and_analysis():
    """Execute design and analysis tasks."""
    # Design task
    execute_agent_task(
        "designer",
        "Design microservice dashboard UI",
        "design_001",
        8,
        "Designer Agent - Create UI/UX"
    )
    
    # Analytics task
    execute_agent_task(
        "analyst",
        "Analyze system performance metrics",
        "analyze_001",
        9,
        "Analyst Agent - Process Metrics"
    )
    
    # Security audit
    execute_agent_task(
        "security",
        "Audit microservice security",
        "security_001",
        10,
        "Security Agent - Security Audit"
    )


def run_deployment_workflow():
    """Execute deployment and monitoring tasks."""
    # Deployment task
    execute_agent_task(
        "deployer",
        "production",
        "deploy_001",
        11,
        "Deployer Agent - Manage CI/CD"
    )
    
    # Monitoring task
    execute_agent_task(
        "monitor",
        "all",
        "monitor_001",
        12,
        "Monitor Agent - Track Performance"
    )


def check_status():
    """Check agent and task status."""
    # Get agent status
    response = requests.get(f"{BASE_URL}/agents/researcher/status", timeout=5)
    print_response("13. Get Researcher Agent Status", response)
    
    # Get task status
    response = requests.get(f"{BASE_URL}/tasks/research_001", timeout=10)
    print_response("14. Get Task Status", response)


def main():
    """Demonstrate the multi-agent system."""
    get_system_info()
    run_research_workflow()
    run_planning_workflow()
    run_design_and_analysis()
    run_deployment_workflow()
    check_status()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Please make sure the server is running:")
        print("  python main.py")
        print("Or with Docker:")
        print("  docker-compose up -d")
    except Exception as e:
        print(f"\nError: {e}")
