# Deployment Guide

This guide covers deploying the Multi-Agent AI System in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

---

## Local Development

### Prerequisites
- Python 3.9+
- Redis server

### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/StayUp90/StayUpAgents.git
cd StayUpAgents
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start Redis:**
```bash
# Option 1: Docker
docker run -d -p 6379:6379 redis:alpine

# Option 2: Local installation
redis-server
```

5. **Run the application:**
```bash
python main.py
```

6. **Access the API:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Start all services:**
```bash
docker-compose up -d
```

2. **View logs:**
```bash
docker-compose logs -f
```

3. **Stop services:**
```bash
docker-compose down
```

4. **Rebuild after changes:**
```bash
docker-compose up -d --build
```

### Using Docker Only

1. **Build the image:**
```bash
docker build -t stayup-agents:latest .
```

2. **Run Redis:**
```bash
docker run -d --name redis -p 6379:6379 redis:alpine
```

3. **Run the application:**
```bash
docker run -d \
  --name stayup-agents \
  -p 8000:8000 \
  -e REDIS_HOST=redis \
  --link redis:redis \
  stayup-agents:latest
```

---

## Cloud Deployment

### AWS (Elastic Container Service)

1. **Build and push to ECR:**
```bash
# Authenticate with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and tag
docker build -t stayup-agents .
docker tag stayup-agents:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/stayup-agents:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/stayup-agents:latest
```

2. **Create ECS Task Definition:**
```json
{
  "family": "stayup-agents",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/stayup-agents:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "REDIS_HOST",
          "value": "<elasticache-endpoint>"
        }
      ]
    }
  ]
}
```

3. **Use ElastiCache for Redis:**
- Create Redis cluster in ElastiCache
- Update REDIS_HOST in environment variables

### Google Cloud Platform (Cloud Run)

1. **Build and push to GCR:**
```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Build and push
docker build -t gcr.io/<project-id>/stayup-agents .
docker push gcr.io/<project-id>/stayup-agents
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy stayup-agents \
  --image gcr.io/<project-id>/stayup-agents \
  --platform managed \
  --region us-central1 \
  --set-env-vars REDIS_HOST=<memorystore-ip>
```

3. **Use Memorystore for Redis:**
- Create Redis instance in Memorystore
- Configure VPC connector for Cloud Run

### Azure (Container Instances)

1. **Build and push to ACR:**
```bash
# Login to ACR
az acr login --name <registry-name>

# Build and push
docker build -t <registry-name>.azurecr.io/stayup-agents .
docker push <registry-name>.azurecr.io/stayup-agents
```

2. **Deploy with Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name stayup-agents \
  --image <registry-name>.azurecr.io/stayup-agents \
  --ports 8000 \
  --environment-variables REDIS_HOST=<redis-cache-endpoint>
```

3. **Use Azure Cache for Redis:**
- Create Redis cache
- Update connection settings

### Heroku

1. **Create Heroku app:**
```bash
heroku create stayup-agents
```

2. **Add Redis addon:**
```bash
heroku addons:create heroku-redis:hobby-dev
```

3. **Deploy:**
```bash
git push heroku main
```

4. **Set environment variables:**
```bash
heroku config:set REDIS_HOST=<redis-url>
```

---

## Kubernetes Deployment

### Using Kubernetes

1. **Create namespace:**
```bash
kubectl create namespace stayup-agents
```

2. **Deploy Redis:**
```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: stayup-agents
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: stayup-agents
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

3. **Deploy API:**
```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stayup-agents
  namespace: stayup-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: stayup-agents
  template:
    metadata:
      labels:
        app: stayup-agents
    spec:
      containers:
      - name: api
        image: stayup-agents:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_HOST
          value: "redis"
        - name: REDIS_PORT
          value: "6379"
---
apiVersion: v1
kind: Service
metadata:
  name: stayup-agents
  namespace: stayup-agents
spec:
  type: LoadBalancer
  selector:
    app: stayup-agents
  ports:
  - port: 80
    targetPort: 8000
```

4. **Apply configurations:**
```bash
kubectl apply -f redis-deployment.yaml
kubectl apply -f api-deployment.yaml
```

---

## Production Considerations

### Security

1. **Enable Authentication:**
```python
# Add to main.py
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

@app.post("/agents/{agent_name}/execute")
async def execute_agent(
    agent_name: str,
    request: TaskRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Validate token
    # ... existing code
```

2. **Secure Redis:**
```bash
# docker-compose.yml
services:
  redis:
    command: redis-server --requirepass ${REDIS_PASSWORD}
```

3. **Use HTTPS:**
- Configure SSL/TLS certificates
- Use reverse proxy (nginx, Caddy)
- Enable CORS properly

### Performance

1. **Use Redis Cluster:**
```yaml
# For high availability
services:
  redis-master:
    image: redis:alpine
  redis-replica-1:
    image: redis:alpine
    command: redis-server --replicaof redis-master 6379
```

2. **Scale API instances:**
```bash
docker-compose up -d --scale api=3
```

3. **Add caching:**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

### Monitoring

1. **Add Prometheus metrics:**
```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

2. **Add health checks:**
```python
@app.get("/health")
async def health():
    # Check Redis connection
    # Check agent status
    # Return health status
```

3. **Add logging:**
```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log", maxBytes=10000000, backupCount=5
)
logging.basicConfig(handlers=[handler], level=logging.INFO)
```

### Backup and Recovery

1. **Redis persistence:**
```bash
# Enable RDB snapshots
redis-server --save 900 1 --save 300 10
```

2. **Backup strategy:**
- Regular Redis backups
- Environment configuration backups
- Code version control

### Environment Variables

Production environment variables:

```bash
# .env (DO NOT commit to git)
REDIS_HOST=production-redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=secure-password
API_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/agents/{agent_name}/execute")
@limiter.limit("100/minute")
async def execute_agent(...):
    # ... existing code
```

---

## Troubleshooting

### Common Issues

1. **Redis connection failed:**
- Check Redis is running
- Verify REDIS_HOST and REDIS_PORT
- Check network connectivity

2. **Port already in use:**
- Change port in docker-compose.yml
- Or stop conflicting service

3. **Docker build fails:**
- Clear Docker cache: `docker system prune -a`
- Check Dockerfile syntax

4. **Tests fail:**
- Ensure dependencies installed
- Check Redis is available for tests

### Getting Help

- Check logs: `docker-compose logs`
- Review documentation
- Open an issue on GitHub

---

## Next Steps

After deployment:

1. Configure monitoring and alerts
2. Set up automated backups
3. Implement authentication
4. Configure CI/CD pipeline
5. Add custom agents as needed
6. Integrate with AI services (OpenAI, etc.)

For more information, see:
- [README.md](README.md)
- [API Documentation](API.md)
- [Architecture Guide](ARCHITECTURE.md)
