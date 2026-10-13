# Deployment Guide
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. DEPLOYMENT OVERVIEW

This document provides comprehensive deployment strategies for the AI-Powered Digital Bodyguard system using Docker, AWS, and Render.

### 1.1 Deployment Options

- **Docker**: Containerized deployment for local and cloud
- **AWS**: Full cloud infrastructure deployment
- **Render**: Simplified PaaS deployment

### 1.2 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (AWS ELB)               │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐          ┌──────────▼─────────┐
│   Frontend     │          │    Backend        │
│   (Nginx)      │◄─────────│   (FastAPI)       │
│   Port: 80/443 │          │   Port: 8000      │
└────────────────┘          └─────────┬───────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
            ┌───────▼──────┐  ┌───────▼──────┐  ┌─────▼──────┐
            │ PostgreSQL   │  │    Redis     │  │  Celery    │
            │   Port: 5432 │  │   Port: 6379 │  │  Worker    │
            └──────────────┘  └──────────────┘  └────────────┘
```

---

## 2. DOCKER DEPLOYMENT

### 2.1 Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.2 Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 2.3 Monitoring Agent Dockerfile

```dockerfile
# monitoring-agent/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_monitoring.txt .
RUN pip install --no-cache-dir -r requirements_monitoring.txt

COPY desktop_agent.py .
COPY process_monitor.py .
COPY resource_monitor.py .
COPY network_monitor.py .
COPY file_monitor.py .
COPY browser_monitor.py .
COPY data_transmitter.py .
COPY monitoring_service.py .

CMD ["python", "desktop_agent.py", "--backend-url", "${BACKEND_URL}", "--api-key", "${API_KEY}"]
```

### 2.4 Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    container_name: digital_bodyguard_db
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7.2-alpine
    container_name: digital_bodyguard_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build: ./backend
    container_name: digital_bodyguard_backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
      - DEBUG=False
    volumes:
      - ./backend:/app
      - ./models:/app/models
      - ./uploads:/app/uploads
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Celery Worker
  celery_worker:
    build: ./backend
    container_name: digital_bodyguard_celery_worker
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend:/app
      - ./models:/app/models
    depends_on:
      - db
      - redis
    command: celery -A app.celery_app worker --loglevel=info

  # Celery Beat
  celery_beat:
    build: ./backend
    container_name: digital_bodyguard_celery_beat
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    command: celery -A app.celery_app beat --loglevel=info

  # Frontend
  frontend:
    build: ./frontend
    container_name: digital_bodyguard_frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000

volumes:
  postgres_data:
  redis_data:
```

### 2.5 Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7.2-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
      - DEBUG=False
    volumes:
      - ./uploads:/app/uploads
      - ./models:/app/models
    depends_on:
      - db
      - redis
    restart: unless-stopped

  celery_worker:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./models:/app/models
    depends_on:
      - db
      - redis
    restart: unless-stopped

  celery_beat:
    build: ./backend
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 2.6 Deployment Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Rebuild and restart
docker-compose up -d --build

# Run database migrations
docker-compose exec backend alembic upgrade head

# Create superuser
docker-compose exec backend python -c "from app.database import SessionLocal; from app.models.user import User; from app.utils.security import get_password_hash; db = SessionLocal(); user = User(email='admin@example.com', password_hash=get_password_hash('Admin123!'), role='admin'); db.add(user); db.commit(); db.close()"
```

---

## 3. AWS DEPLOYMENT

### 3.1 AWS Architecture

```
┌─────────────────────────────────────────────────────────┐
│              AWS CloudFront (CDN)                        │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐          ┌──────────▼─────────┐
│   AWS ELB      │          │   AWS ALB         │
│   (HTTP/HTTPS) │          │   (Internal)      │
└───────┬────────┘          └──────────┬─────────┘
        │                              │
┌───────▼────────┐          ┌──────────▼─────────┐
│   ECS Task     │          │   ECS Task         │
│   Frontend     │          │   Backend          │
│   (Fargate)    │          │   (Fargate)        │
└────────────────┘          └──────────┬─────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
            ┌───────▼──────┐  ┌───────▼──────┐  ┌─────▼──────┐
            │   RDS        │  │   ElastiCache│  │  SQS/SNS   │
            │ PostgreSQL   │  │   Redis      │  │            │
            └──────────────┘  └──────────────┘  └────────────┘
```

### 3.2 AWS ECS Task Definition (Backend)

```json
{
  "family": "digital-bodyguard-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/digital-bodyguard-backend:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://USER:PASSWORD@RDS_ENDPOINT:5432/digital_bodyguard"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://ELASTICACHE_ENDPOINT:6379/0"
        },
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key"
        },
        {
          "name": "DEBUG",
          "value": "false"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:digital-bodyguard/db-password"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:digital-bodyguard/secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/digital-bodyguard-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:8000/health || exit 1"
        ],
        "interval": 30,
        "timeout": 10,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### 3.3 AWS ECS Task Definition (Frontend)

```json
{
  "family": "digital-bodyguard-frontend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "frontend",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/digital-bodyguard-frontend:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "VITE_API_URL",
          "value": "https://api.digitalbodyguard.com"
        },
        {
          "name": "VITE_WS_URL",
          "value": "wss://api.digitalbodyguard.com"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/digital-bodyguard-frontend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "wget --no-verbose --tries=1 --spider http://localhost/ || exit 1"
        ],
        "interval": 30,
        "timeout": 10,
        "retries": 3
      }
    }
  ]
}
```

### 3.4 AWS ECS Service Definition

```python
# aws/ecs_service.py
import boto3

def create_ecs_service():
    ecs = boto3.client('ecs')
    
    # Create backend service
    ecs.create_service(
        cluster='digital-bodyguard',
        serviceName='backend',
        taskDefinition='digital-bodyguard-backend',
        desiredCount=2,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-12345', 'subnet-67890'],
                'securityGroups': ['sg-12345'],
                'assignPublicIp': False
            }
        },
        loadBalancers=[
            {
                'targetGroupArn': 'arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/digital-bodyguard-backend/12345',
                'containerName': 'backend',
                'containerPort': 8000
            }
        ]
    )
    
    # Create frontend service
    ecs.create_service(
        cluster='digital-bodyguard',
        serviceName='frontend',
        taskDefinition='digital-bodyguard-frontend',
        desiredCount=2,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-12345', 'subnet-67890'],
                'securityGroups': ['sg-67890'],
                'assignPublicIp': True
            }
        }
    )
```

### 3.5 AWS RDS Configuration

```python
# aws/rds.py
import boto3

def create_rds_instance():
    rds = boto3.client('rds')
    
    response = rds.create_db_instance(
        DBInstanceIdentifier='digital-bodyguard-db',
        DBInstanceClass='db.t3.medium',
        Engine='postgres',
        EngineVersion='15.4',
        MasterUsername='admin',
        MasterUserPassword='SecurePassword123!',
        AllocatedStorage=20,
        StorageType='gp2',
        VpcSecurityGroupIds=['sg-12345'],
        DBSubnetGroupName='digital-bodyguard-subnet-group',
        BackupRetentionPeriod=7,
        MultiAZ=False,
        PubliclyAccessible=False,
        DeletionProtection=True
    )
    
    return response
```

### 3.6 AWS ElastiCache Configuration

```python
# aws/elasticache.py
import boto3

def create_redis_cluster():
    elasticache = boto3.client('elasticache')
    
    response = elasticache.create_replication_group(
        ReplicationGroupId='digital-bodyguard-redis',
        ReplicationGroupDescription='Redis cluster for Digital Bodyguard',
        NodeType='cache.t3.medium',
        NumCacheClusters=1,
        Engine='redis',
        EngineVersion='7.2',
        CacheSubnetGroupName='digital-bodyguard-cache-subnet-group',
        SecurityGroupIds=['sg-12345'],
        AutomaticFailoverEnabled=False
    )
    
    return response
```

### 3.7 AWS CloudFront Distribution

```python
# aws/cloudfront.py
import boto3

def create_cloudfront_distribution():
    cloudfront = boto3.client('cloudfront')
    
    response = cloudfront.create_distribution(
        DistributionConfig={
            'CallerReference': 'digital-bodyguard-' + str(int(time.time())),
            'Comment': 'Digital Bodyguard Frontend',
            'Enabled': True,
            'Origins': {
                'Quantity': 1,
                'Items': [
                    {
                        'Id': 'frontend-origin',
                        'DomainName': 'digital-bodyguard-frontend-12345.us-east-1.elb.amazonaws.com',
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only',
                            'OriginSslProtocols': {
                                'Quantity': 1,
                                'Items': ['TLSv1.2']
                            }
                        }
                    }
                ]
            },
            'DefaultCacheBehavior': {
                'TargetOriginId': 'frontend-origin',
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': ['GET', 'HEAD', 'OPTIONS'],
                'CachedMethods': ['GET', 'HEAD'],
                'ForwardedValues': {
                    'QueryString': False,
                    'Cookies': {'Forward': 'none'}
                },
                'MinTTL': 0,
                'DefaultTTL': 3600,
                'MaxTTL': 86400
            },
            'ViewerCertificate': {
                'ACMCertificateArn': 'arn:aws:acm:us-east-1:ACCOUNT_ID:certificate/12345',
                'SSLSupportMethod': 'sni-only',
                'MinimumProtocolVersion': 'TLSv1.2_2021'
            }
        }
    )
    
    return response
```

### 3.8 AWS Deployment Script

```bash
#!/bin/bash
# deploy_aws.sh

# Set AWS region
export AWS_REGION=us-east-1

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push backend image
cd backend
docker build -t digital-bodyguard-backend .
docker tag digital-bodyguard-backend:latest ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/digital-bodyguard-backend:latest
docker push ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/digital-bodyguard-backend:latest

# Build and push frontend image
cd ../frontend
docker build -t digital-bodyguard-frontend .
docker tag digital-bodyguard-frontend:latest ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/digital-bodyguard-frontend:latest
docker push ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/digital-bodyguard-frontend:latest

# Update ECS services
aws ecs update-service --cluster digital-bodyguard --service backend --force-new-deployment
aws ecs update-service --cluster digital-bodyguard --service frontend --force-new-deployment

echo "Deployment completed successfully!"
```

---

## 4. RENDER DEPLOYMENT

### 4.1 Render Architecture

Render provides a simplified PaaS deployment:

```
┌─────────────────────────────────────────┐
│         Render Load Balancer            │
└───────────────────┬─────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌───────▼────────┐
│   Web Service  │    │   Web Service  │
│   Frontend     │    │   Backend      │
│   (Docker)     │    │   (Docker)     │
└────────────────┘    └───────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼──────┐ ┌──▼──────────┐ ┌─▼──────────┐
        │ PostgreSQL   │ │   Redis     │ │  Cron Job │
        │   (Managed)  │ │  (Managed)  │ │  Celery    │
        └──────────────┘ └─────────────┘ └────────────┘
```

### 4.2 Render Backend Service

```yaml
# render.yaml (Backend)
services:
  - type: web
    name: digital-bodyguard-backend
    env: docker
    plan: starter
    dockerfilePath: ./backend/Dockerfile
    dockerContext: ./backend
    autoDeploy: false
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: digital-bodyguard-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: digital-bodyguard-redis
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: VIRUSTOTAL_API_KEY
        sync: false
    healthCheckPath: /health

databases:
  - name: digital-bodyguard-db
    databaseName: digital_bodyguard
    user: digital_bodyguard
    plan: starter
```

### 4.3 Render Frontend Service

```yaml
# render.yaml (Frontend)
services:
  - type: web
    name: digital-bodyguard-frontend
    env: docker
    plan: starter
    dockerfilePath: ./frontend/Dockerfile
    dockerContext: ./frontend
    autoDeploy: false
    envVars:
      - key: VITE_API_URL
        value: https://digital-bodyguard-backend.onrender.com
      - key: VITE_WS_URL
        value: wss://digital-bodyguard-backend.onrender.com

workers:
  - type: celery
    name: digital-bodyguard-celery
    env: docker
    plan: starter
    dockerfilePath: ./backend/Dockerfile
    dockerContext: ./backend
    numInstances: 1
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: digital-bodyguard-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: digital-bodyguard-redis
          property: connectionString
      - key: SECRET_KEY
        sync: false
    command: celery -A app.celery_app worker --loglevel=info
```

### 4.4 Render Redis Service

```yaml
# render.yaml (Redis)
services:
  - type: redis
    name: digital-bodyguard-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru
    ipAllowList: []
```

### 4.5 Render Deployment Commands

```bash
# Install Render CLI
npm install -g render-cli

# Login to Render
render login

# Deploy backend
render deploy ./backend --service-id=srv-xxxxx

# Deploy frontend
render deploy ./frontend --service-id=srv-yyyyy

# Deploy Celery worker
render deploy ./backend --service-id=srv-zzzzz --worker

# View logs
render logs --service-id=srv-xxxxx
```

---

## 5. ENVIRONMENT MANAGEMENT

### 5.1 Production Environment Variables

```bash
# .env.production
# Database
DB_USER=digital_bodyguard
DB_PASSWORD=secure_password
DB_NAME=digital_bodyguard

# Backend
SECRET_KEY=production-secret-key-change-me
VIRUSTOTAL_API_KEY=your-virustotal-api-key

# Frontend
VITE_API_URL=https://api.digitalbodyguard.com
VITE_WS_URL=wss://api.digitalbodyguard.com

# AWS (if using AWS)
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012
AWS_ECR_REPOSITORY=digital-bodyguard

# Render (if using Render)
RENDER_SERVICE_ID=srv-xxxxx
```

### 5.2 Secrets Management

```python
# aws/secrets_manager.py
import boto3
import json

def store_secret(secret_name, secret_value):
    """Store secret in AWS Secrets Manager"""
    client = boto3.client('secretsmanager')
    
    response = client.create_secret(
        Name=secret_name,
        SecretString=json.dumps(secret_value)
    )
    
    return response

def get_secret(secret_name):
    """Retrieve secret from AWS Secrets Manager"""
    client = boto3.client('secretsmanager')
    
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    
    return secret
```

---

## 6. MONITORING AND LOGGING

### 6.1 CloudWatch Monitoring

```python
# aws/cloudwatch.py
import boto3

def create_cloudwatch_alarms():
    cloudwatch = boto3.client('cloudwatch')
    
    # CPU utilization alarm
    cloudwatch.put_metric_alarm(
        AlarmName='digital-bodyguard-backend-high-cpu',
        AlarmDescription='Alert when CPU utilization exceeds 80%',
        Namespace='AWS/ECS',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'ServiceName',
                'Value': 'backend'
            }
        ],
        Statistic='Average',
        Period=300,
        EvaluationPeriods=2,
        Threshold=80,
        ComparisonOperator='GreaterThanThreshold',
        TreatMissingData='notBreaching'
    )
    
    # Memory utilization alarm
    cloudwatch.put_metric_alarm(
        AlarmName='digital-bodyguard-backend-high-memory',
        AlarmDescription='Alert when memory utilization exceeds 80%',
        Namespace='CWAgent',
        MetricName='mem_used_percent',
        Dimensions=[
            {
                'Name': 'ServiceName',
                'Value': 'backend'
            }
        ],
        Statistic='Average',
        Period=300,
        EvaluationPeriods=2,
        Threshold=80,
        ComparisonOperator='GreaterThanThreshold'
    )
```

### 6.2 CloudWatch Logs

```python
# aws/cloudwatch_logs.py
import boto3

def create_log_groups():
    logs = boto3.client('logs')
    
    # Create log group for backend
    logs.create_log_group(
        logGroupName='/ecs/digital-bodyguard-backend',
        retentionInDays=30
    )
    
    # Create log group for frontend
    logs.create_log_group(
        logGroupName='/ecs/digital-bodyguard-frontend',
        retentionInDays=30
    )
    
    # Create log group for celery
    logs.create_log_group(
        logGroupName='/ecs/digital-bodyguard-celery',
        retentionInDays=30
    )
```

### 6.3 Application Logging Configuration

```python
# logging_config.py (production)
import logging
import sys
from app.config import settings

def setup_production_logging():
    """Setup production logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # CloudWatch handler (if using AWS)
    try:
        import boto3
        logs = boto3.client('logs')
        
        # Create log stream
        logs.create_log_stream(
            logGroupName='/ecs/digital-bodyguard-backend',
            logStreamName='production'
        )
        
        logger.info("CloudWatch logging configured")
    except Exception as e:
        logger.warning(f"Could not configure CloudWatch logging: {e}")
    
    return logger
```

---

## 7. BACKUP AND DISASTER RECOVERY

### 7.1 Database Backup

```python
# aws/rds_backup.py
import boto3
from datetime import datetime

def create_rds_snapshot():
    """Create RDS snapshot"""
    rds = boto3.client('rds')
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    snapshot_id = f'digital-bodyguard-snapshot-{timestamp}'
    
    response = rds.create_db_snapshot(
        DBSnapshotIdentifier=snapshot_id,
        DBInstanceIdentifier='digital-bodyguard-db'
    )
    
    return response

def list_rds_snapshots():
    """List RDS snapshots"""
    rds = boto3.client('rds')
    
    response = rds.describe_db_snapshots(
        DBInstanceIdentifier='digital-bodyguard-db',
        SnapshotType='manual'
    )
    
    return response['DBSnapshots']
```

### 7.2 Automated Backup Script

```bash
#!/bin/bash
# backup.sh

# Backup database
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup_$(date +%Y%m%d).sql

# Compress backup
gzip backup_$(date +%Y%m%d).sql

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://digital-bodyguard-backups/

# Keep only last 7 days of backups
aws s3 ls s3://digital-bodyguard-backups/ | while read -r line; do
    file_date=$(echo $line | awk '{print $4}')
    file_name=$(echo $line | awk '{print $NF}')
    
    if [ "$file_date" -lt $(date -d "7 days ago" +%Y%m%d) ]; then
        aws s3 rm s3://digital-bodyguard-backups/$file_name
    fi
done
```

---

## 8. CI/CD PIPELINE

### 8.1 GitHub Actions (AWS)

```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: ${{ steps.login-ecr.outputs.registry }}/digital-bodyguard-backend:latest
      
      - name: Build and push frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: ${{ steps.login-ecr.outputs.registry }}/digital-bodyguard-frontend:latest
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster digital-bodyguard --service backend --force-new-deployment
          aws ecs update-service --cluster digital-bodyguard --service frontend --force-new-deployment
```

### 8.2 GitHub Actions (Render)

```yaml
# .github/workflows/deploy-render.yml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy Backend
        run: |
          curl -X POST https://api.render.com/v1/services/srv-xxxxx/deploys \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}"
      
      - name: Deploy Frontend
        run: |
          curl -X POST https://api.render.com/v1/services/srv-yyyyy/deploys \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}"
```

---

## 9. SSL/TLS CONFIGURATION

### 9.1 AWS Certificate Manager

```python
# aws/acm.py
import boto3

def request_ssl_certificate():
    """Request SSL certificate from ACM"""
    acm = boto3.client('acm')
    
    response = acm.request_certificate(
        DomainName='digitalbodyguard.com',
        SubjectAlternativeNames=['*.digitalbodyguard.com', 'api.digitalbodyguard.com'],
        ValidationMethod='DNS'
    )
    
    return response

def list_certificates():
    """List SSL certificates"""
    acm = boto3.client('acm')
    
    response = acm.list_certificates()
    
    return response['CertificateSummaryList']
```

### 9.2 Nginx SSL Configuration

```nginx
# nginx.conf (with SSL)
server {
    listen 443 ssl http2;
    server_name digitalbodyguard.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name digitalbodyguard.com;
    return 301 https://$host$request_uri;
}
```

---

## 10. SCALING STRATEGY

### 10.1 Auto Scaling Configuration

```python
# aws/autoscaling.py
import boto3

def configure_auto_scaling():
    """Configure ECS auto scaling"""
    application_autoscaling = boto3.client('application-autoscaling')
    
    # Register scalable target
    application_autoscaling.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/digital-bodyguard/backend',
        ScalableDimension='ecs:service:DesiredCount',
        MinCapacity=2,
        MaxCapacity=10
    )
    
    # Create scaling policy
    application_autoscaling.put_scaling_policy(
        PolicyName='backend-scale-out',
        PolicyType='TargetTrackingScaling',
        ResourceId='service/digital-bodyguard/backend',
        ScalableDimension='ecs:service:DesiredCount',
        ServiceNamespace='ecs',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
            }
        }
    )
```

### 10.2 Database Scaling

```python
# aws/rds_scaling.py
import boto3

def modify_rds_instance():
    """Modify RDS instance for scaling"""
    rds = boto3.client('rds')
    
    response = rds.modify_db_instance(
        DBInstanceIdentifier='digital-bodyguard-db',
        DBInstanceClass='db.t3.large',
        AllocatedStorage=50,
        StorageType='gp2',
        ApplyImmediately=True
    )
    
    return response
```

---

## 11. DEPLOYMENT CHECKLIST

### 11.1 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] SSL certificates obtained
- [ ] DNS records configured
- [ ] Firewall rules configured
- [ ] Monitoring and logging setup
- [ ] Backup strategy in place
- [ ] Disaster recovery plan documented
- [ ] Team trained on deployment process

### 11.2 Post-Deployment Checklist

- [ ] Services running and healthy
- [ ] Database connectivity verified
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] WebSocket connections working
- [ ] Celery tasks processing
- [ ] Monitoring data flowing
- [ ] Alerts being generated
- [ ] Performance metrics normal
- [ ] Error rates within limits

---

## 12. CONCLUSION

This document provides comprehensive deployment strategies for the AI-Powered Digital Bodyguard system including:

- **Docker Deployment**: Containerized deployment with Docker Compose
- **AWS Deployment**: Full cloud infrastructure with ECS, RDS, ElastiCache
- **Render Deployment**: Simplified PaaS deployment
- **Environment Management**: Production environment configuration
- **Monitoring**: CloudWatch monitoring and logging
- **Backup**: Database backup and disaster recovery
- **CI/CD**: Automated deployment pipelines
- **SSL/TLS**: Certificate management and configuration
- **Scaling**: Auto-scaling configuration
- **Checklists**: Pre and post-deployment verification

**Deployment Summary:**

- **Docker**: Quick local development and testing
- **AWS**: Production-grade cloud deployment with full control
- **Render**: Simplified PaaS deployment for rapid deployment

**Recommendation:** Start with Docker for development, use Render for staging, and AWS for production.

---

## APPENDICES

### Appendix A: Quick Start Deployment

```bash
# Docker deployment
git clone <repository>
cd digital-bodyguard
cp .env.example .env
# Edit .env with your values
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

### Appendix B: AWS Cost Estimation

- **ECS Fargate**: $0.04048 per vCPU-hour, $0.004445 per GB-hour
- **RDS PostgreSQL**: $0.023 per hour (db.t3.medium)
- **ElastiCache Redis**: $0.026 per hour (cache.t3.medium)
- **CloudFront**: $0.0075 per 10,000 requests
- **Data Transfer**: $0.09 per GB (first 10 GB free)
- **Estimated Monthly Cost**: ~$150-300 for small deployment

### Appendix C: Troubleshooting

```bash
# Check container logs
docker-compose logs backend

# Restart services
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend

# Check AWS ECS service status
aws ecs describe-services --cluster digital-bodyguard --services backend

# Check Render service status
render logs --service-id=srv-xxxxx
```

### Appendix D: Security Best Practices

- Use strong, unique passwords for all services
- Enable multi-factor authentication for AWS accounts
- Use AWS Secrets Manager for sensitive data
- Enable encryption at rest for RDS and EBS volumes
- Use SSL/TLS for all communications
- Regularly update and patch all services
- Implement network security groups and firewalls
- Enable CloudTrail for AWS API logging
- Regular security audits and penetration testing
