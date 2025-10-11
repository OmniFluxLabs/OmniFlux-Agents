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


def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")
    print(json.dumps(response.json(), indent=2))


def main(): print("Multi-Agent AI System - Example Usage\n" + "=" * 60 + "\n" + health_check())
    """Demonstrate the multi-agent system."""
    
    print("Multi-Agent AI System - Example Usage")
    print("=" * 60)
    
    # 1. Health check
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print_response("1. Health Check", response)
    
    # 2. List all agents
    response = requests.get(f"{BASE_URL}/agents", timeout=10)
    print_response("2. List All Agents", response)
    
    # 3. Research task
    response = requests.post(
        f"{BASE_URL}/agents/researcher/execute",
        json={
            "task": "Research best practices for microservices architecture",
            "task_id": "research_001"
        }
    )
    print_response("3. Researcher Agent - Execute Research", response)
    
    # 4. Get shared context (research results)
    time.sleep(0.5)
    response = requests.get(f"{BASE_URL}/context/latest_research", timeout=5)
    print_response("4. Get Research Context", response)
    
    # 5. Coding task (will use research context)
    response = requests.post(
        f"{BASE_URL}/agents/coder/execute",
        json={
            "task": "Create a microservice skeleton in Python",
            "task_id": "code_001"
        }
    )
    print_response("5. Coder Agent - Generate Code", response)
    
    # 6. Planning task
    response = requests.post(
        f"{BASE_URL}/agents/planner/execute",
        json={
            "task": "Plan microservice deployment",
            "task_id": "plan_001"
        }
    )
    print_response("6. Planner Agent - Create Project Plan", response)
    
    # 7. Validation task (will use code context)
    response = requests.post(
        f"{BASE_URL}/agents/validator/execute",
        json={
            "task": "Validate generated code",
            "task_id": "validate_001"
        }
    )
    print_response("7. Validator Agent - Test Code", response)
    
    # 8. Design task
    response = requests.post(
        f"{BASE_URL}/agents/designer/execute",
        json={
            "task": "Design microservice dashboard UI",
            "task_id": "design_001"
        }
    )
    print_response("8. Designer Agent - Create UI/UX", response)
    
    # 9. Analytics task
    response = requests.post(
        f"{BASE_URL}/agents/analyst/execute",
        json={
            "task": "Analyze system performance metrics",
            "task_id": "analyze_001"
        }
    )
    print_response("9. Analyst Agent - Process Metrics", response)
    
    # 10. Security audit
    response = requests.post(
        f"{BASE_URL}/agents/security/execute",
        json={
            "task": "Audit microservice security",
            "task_id": "security_001"
        }
    )
    print_response("10. Security Agent - Security Audit", response)
    
    # 11. Deployment task (will use validation context)
    response = requests.post(
        f"{BASE_URL}/agents/deployer/execute",
        json={
            "task": "production",
            "task_id": "deploy_001"
        }
    )
    print_response("11. Deployer Agent - Manage CI/CD", response)
    
    # 12. Monitoring task (will use deployment context)
    response = requests.post(
        f"{BASE_URL}/agents/monitor/execute",
        json={
            "task": "all",
            "task_id": "monitor_001"
        }
    )
    print_response("12. Monitor Agent - Track Performance", response)
    
    # 13. Get agent status
    response = requests.get(f"{BASE_URL}/agents/researcher/status", timeout=5)
    print_response("13. Get Researcher Agent Status", response)
    
    # 14. Get task status
    response = requests.get(f"{BASE_URL}/tasks/research_001", timeout=10)
    print_response("14. Get Task Status", response)
    
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
