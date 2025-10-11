# Contributing to StayUpAgents

Thank you for your interest in contributing to the Multi-Agent AI System!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/StayUpAgents.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (required for development)
docker run -d -p 6379:6379 redis:alpine

# Run the server
python main.py

# Run tests
pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add type hints where appropriate

## Adding a New Agent

1. Create the agent class in `agents/__init__.py`:

```python
class MyNewAgent(BaseAgent):
    """Description of what this agent does."""
    
    def __init__(self, memory: RedisMemory):
        super().__init__("MyNewAgent", memory)
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's task."""
        # Your implementation here
        result = {
            "task": task.get("task"),
            "result": "success"
        }
        return result
```

2. Register it in `main.py`:

```python
agents["mynewagent"] = MyNewAgent(memory)
```

3. Add tests in `tests/test_agents.py`:

```python
def test_my_new_agent(mock_memory):
    """Test MyNewAgent."""
    agent = MyNewAgent(mock_memory)
    task = {"task": "Test task"}
    result = agent.execute(task)
    assert "result" in result
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Writing Tests

- Use pytest fixtures for setup
- Mock external dependencies (Redis, APIs)
- Test both success and failure cases
- Aim for high coverage (>80%)

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files are included

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guide
```

## Reporting Bugs

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.9.7]
- Redis: [e.g., 7.0]
- Docker: [e.g., 20.10.17]

**Logs**
Include relevant logs or error messages
```

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How could this be implemented?

**Alternatives**
Any alternative solutions considered?
```

## Code Review Process

1. Automated tests run on PR creation
2. Code review by maintainers
3. Address feedback
4. Approval and merge

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the Code of Conduct

## Questions?

- Open an issue for discussion
- Tag it with `question`
- Be specific about what you need help with

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
