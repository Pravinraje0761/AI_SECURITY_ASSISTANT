# Integration Guide
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. INTEGRATION OVERVIEW

This document provides comprehensive guidance for integrating all components of the AI-Powered Digital Bodyguard system.

### 1.1 Integration Components

- **ML Models**: Phishing, Malware, Behavior detection models
- **Backend API**: FastAPI REST API
- **Frontend**: React Dashboard
- **Monitoring Agent**: Desktop monitoring service
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: Celery with Redis

### 1.2 Integration Architecture

```
┌─────────────┐
│   Frontend   │
│   (React)    │
└──────┬──────┘
       │ HTTP/WebSocket
       ▼
┌─────────────┐
│   Backend    │
│   (FastAPI)  │
└──────┬──────┘
       │
       ├──────────────┬──────────────┬──────────────┐
       ▼              ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  ML Models  │ │  Database   │ │    Redis    │ │   Celery    │
│             │ │ (PostgreSQL)│ │             │ │             │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                      ▲
                      │
       ┌──────────────┴──────────────┐
       │                             │
┌─────────────┐              ┌─────────────┐
│  Monitoring │              │  Desktop    │
│   Agent     │◄─────────────│   Agent     │
└─────────────┘              └─────────────┘
```

---

## 2. ML MODEL INTEGRATION

### 2.1 Model Service Integration

```python
# services/phishing_service.py
import joblib
import os
from typing import Dict
from app.ml.phishing_model import PhishingDetector
from app.config import settings

class PhishingService:
    """Phishing detection service"""
    
    def __init__(self):
        self.model_dir = settings.PHISHING_MODEL_DIR
        self.detector = None
        self._load_model()
    
    def _load_model(self):
        """Load phishing detection model"""
        try:
            self.detector = PhishingDetector(self.model_dir)
            self.detector.load_models()
            print("Phishing model loaded successfully")
        except Exception as e:
            print(f"Error loading phishing model: {e}")
    
    def scan_url(self, url: str) -> Dict:
        """Scan URL for phishing"""
        if not self.detector:
            return {
                "is_phishing": False,
                "probability": 0.0,
                "error": "Model not loaded"
            }
        
        try:
            result = self.detector.predict_url(url)
            return {
                "is_phishing": result["ensemble"]["prediction"] == 1,
                "probability": result["ensemble"]["probability"],
                "model_predictions": result
            }
        except Exception as e:
            return {
                "is_phishing": False,
                "probability": 0.0,
                "error": str(e)
            }

# services/malware_service.py
import joblib
import os
import tempfile
from typing import Dict
from app.ml.malware_model import MalwareDetector
from app.config import settings

class MalwareService:
    """Malware detection service"""
    
    def __init__(self):
        self.model_dir = settings.MALWARE_MODEL_DIR
        self.detector = None
        self._load_model()
    
    def _load_model(self):
        """Load malware detection model"""
        try:
            self.detector = MalwareDetector(self.model_dir)
            self.detector.load_models()
            print("Malware model loaded successfully")
        except Exception as e:
            print(f"Error loading malware model: {e}")
    
    def scan_file(self, file_content: bytes, filename: str) -> Dict:
        """Scan file for malware"""
        if not self.detector:
            return {
                "is_malware": False,
                "probability": 0.0,
                "error": "Model not loaded"
            }
        
        try:
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name
            
            # Scan file
            result = self.detector.predict_file(tmp_file_path)
            
            # Clean up
            os.unlink(tmp_file_path)
            
            return {
                "is_malware": result["ensemble"]["prediction"] == 1,
                "probability": result["ensemble"]["probability"],
                "model_predictions": result
            }
        except Exception as e:
            return {
                "is_malware": False,
                "probability": 0.0,
                "error": str(e)
            }

# services/behavior_service.py
from app.ml.behavior_model import BehaviorAnalyzer
from app.config import settings

class BehaviorService:
    """Behavior analysis service"""
    
    def __init__(self):
        self.model_dir = settings.BEHAVIOR_MODEL_DIR
        self.analyzer = None
        self._load_model()
    
    def _load_model(self):
        """Load behavior analysis model"""
        try:
            self.analyzer = BehaviorAnalyzer(self.model_dir)
            self.analyzer.load_models()
            print("Behavior model loaded successfully")
        except Exception as e:
            print(f"Error loading behavior model: {e}")
    
    def analyze_behavior(self, behavior_data: Dict, user_id: str = None) -> Dict:
        """Analyze user behavior"""
        if not self.analyzer:
            return {
                "is_anomalous": False,
                "anomaly_score": 0.0,
                "error": "Model not loaded"
            }
        
        try:
            result = self.analyzer.predict_behavior(behavior_data, user_id)
            return {
                "is_anomalous": result["ensemble"]["prediction"] == 1,
                "anomaly_score": result["ensemble"]["anomaly_score"],
                "model_predictions": result,
                "baseline_comparison": result.get("baseline_comparison")
            }
        except Exception as e:
            return {
                "is_anomalous": False,
                "anomaly_score": 0.0,
                "error": str(e)
            }
    
    def update_baseline(self, user_id: str, behavior_data_list: list) -> Dict:
        """Update user behavior baseline"""
        if not self.analyzer:
            return {"error": "Model not loaded"}
        
        try:
            baseline = self.analyzer.baseline_manager.update_baseline(user_id, behavior_data_list)
            return {
                "user_id": user_id,
                "baseline_updated": True,
                "sample_count": baseline["sample_count"]
            }
        except Exception as e:
            return {"error": str(e)}
```

### 2.2 Backend API Integration

```python
# api/scan.py (updated with service integration)
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scan import ScanRequest, ScanResponse
from app.models.scan import Scan
from app.services.phishing_service import PhishingService
from app.services.malware_service import MalwareService
from app.utils.security import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

# Initialize services
phishing_service = PhishingService()
malware_service = MalwareService()

@router.post("/url", response_model=ScanResponse)
async def scan_url(
    request: ScanRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Scan URL for phishing"""
    if request.type != "phishing":
        raise HTTPException(status_code=400, detail="Invalid scan type")
    
    # Perform phishing scan using service
    result = phishing_service.scan_url(request.target)
    
    # Save scan to database
    scan = Scan(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type=request.type,
        target=request.target,
        result="malicious" if result["is_phishing"] else "benign",
        score=result["probability"],
        details=result
    )
    
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    return scan

@router.post("/file", response_model=ScanResponse)
async def scan_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Scan uploaded file for malware"""
    # Read file content
    content = await file.read()
    
    # Perform malware scan using service
    result = malware_service.scan_file(content, file.filename)
    
    # Save scan to database
    scan = Scan(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type="malware",
        target=file.filename,
        result="malicious" if result["is_malware"] else "benign",
        score=result["probability"],
        details=result
    )
    
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    return scan
```

---

## 3. MONITORING AGENT INTEGRATION

### 3.1 Monitoring Agent Configuration

```python
# config.py (monitoring agent)
import os
from pydantic_settings import BaseSettings

class MonitoringConfig(BaseSettings):
    """Monitoring agent configuration"""
    
    # Backend API
    BACKEND_URL: str = "http://localhost:8000"
    API_KEY: str = ""
    
    # Monitoring settings
    PROCESS_INTERVAL: int = 5
    RESOURCE_INTERVAL: int = 2
    NETWORK_INTERVAL: int = 5
    BROWSER_INTERVAL: int = 10
    
    # Paths to monitor
    MONITOR_DOWNLOADS: bool = True
    MONITOR_DESKTOP: bool = True
    CUSTOM_PATHS: list = []
    
    # Thresholds
    HIGH_CPU_THRESHOLD: float = 90.0
    HIGH_MEMORY_THRESHOLD: float = 90.0
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "monitoring_agent.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

config = MonitoringConfig()
```

### 3.2 Backend API Endpoints for Monitoring

```python
# api/monitoring.py (updated)
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.monitoring import MonitoringData
from app.utils.security import get_current_user
from typing import Dict, Any
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/data")
async def receive_monitoring_data(
    data: Dict[str, Any],
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """Receive monitoring data from desktop agent"""
    try:
        # Store monitoring data
        monitoring_data = MonitoringData(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=data.get("type"),
            data=data.get("data"),
            suspicious_count=data.get("suspicious_count", 0),
            created_at=datetime.utcnow()
        )
        
        db.add(monitoring_data)
        db.commit()
        
        # Process suspicious activities in background
        if data.get("suspicious_count", 0) > 0:
            if background_tasks:
                background_tasks.add_task(process_suspicious_activity, user_id, data)
        
        return {"status": "received", "data_type": data.get("type")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_suspicious_activity(user_id: str, data: Dict):
    """Process suspicious activity and generate alerts"""
    from app.services.alert_service import AlertService
    from app.websocket.manager import manager
    
    alert_service = AlertService()
    
    # Create alert
    alert = {
        "type": data.get("type"),
        "severity": "high" if data.get("suspicious_count", 0) > 1 else "medium",
        "title": f"Suspicious {data.get('type')} activity detected",
        "message": f"{data.get('suspicious_count')} suspicious activities detected",
        "data": data
    }
    
    alert_service.create_alert(user_id, alert)
    
    # Broadcast via WebSocket
    await manager.broadcast_alert(alert)

@router.post("/heartbeat")
async def receive_heartbeat(
    data: Dict,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Receive heartbeat from desktop agent"""
    # Update last seen timestamp in user record
    from app.models.user import User
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
    
    return {"status": "alive"}
```

---

## 4. FRONTEND-BACKEND INTEGRATION

### 4.1 API Client Configuration

```typescript
// src/services/api.ts (updated)
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await api.post('/api/v1/auth/refresh', {
          refresh_token: refreshToken
        })
        
        const { access_token } = response.data
        localStorage.setItem('token', access_token)
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
```

### 4.2 WebSocket Integration

```typescript
// src/services/websocketService.ts (updated)
import { io, Socket } from 'socket.io-client'

class WebSocketService {
  private socket: Socket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private listeners: Map<string, Function[]> = new Map()

  connect() {
    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    
    this.socket = io(WS_URL, {
      auth: {
        token: localStorage.getItem('token')
      },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: this.maxReconnectAttempts
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      this.reconnectAttempts++
    })

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error)
    })

    this.socket.on('new_alert', (data) => {
      this.notify('new_alert', data)
    })

    this.socket.on('threat_detected', (data) => {
      this.notify('threat_detected', data)
    })

    this.socket.on('monitoring_update', (data) => {
      this.notify('monitoring_update', data)
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)!.push(callback)
  }

  off(event: string, callback: Function) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      const index = callbacks.callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  private notify(event: string, data: any) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      callbacks.forEach((callback) => callback(data))
    }
  }
}

export default new WebSocketService()
```

### 4.3 Redux Integration with WebSocket

```typescript
// src/store/alertSlice.ts (updated)
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import alertService from '../services/alertService'
import websocketService from '../services/websocketService'

interface AlertState {
  alerts: any[]
  loading: boolean
  error: string | null
}

const initialState: AlertState = {
  alerts: [],
  loading: false,
  error: null,
}

export const fetchAlerts = createAsyncThunk('alerts/fetch', async () => {
  const response = await alertService.getAlerts()
  return response
})

const alertSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    addAlert: (state, action) => {
      state.alerts.unshift(action.payload)
    },
    setupWebSocketListeners: (state) => {
      // Setup WebSocket listeners
      websocketService.on('new_alert', (alert) => {
        state.alerts.unshift(alert)
      })
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAlerts.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.loading = false
        state.alerts = action.payload
      })
  },
})

export const { addAlert, setupWebSocketListeners } = alertSlice.actions
export default alertSlice.reducer
```

---

## 5. DATABASE INTEGRATION

### 5.1 Database Connection Pool

```python
# database.py (updated)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 5.2 Redis Cache Integration

```python
# cache.py
import redis
from app.config import settings

class Cache:
    """Redis cache wrapper"""
    
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
    
    def get(self, key: str):
        """Get value from cache"""
        return self.redis_client.get(key)
    
    def set(self, key: str, value: str, expire: int = 3600):
        """Set value in cache with expiration"""
        return self.redis_client.setex(key, expire, value)
    
    def delete(self, key: str):
        """Delete key from cache"""
        return self.redis_client.delete(key)
    
    def exists(self, key: str):
        """Check if key exists"""
        return self.redis_client.exists(key)

cache = Cache()
```

### 5.3 Cache Integration with API

```python
# api/dashboard.py (with caching)
from fastapi import APIRouter, Depends
from app.cache import cache
from app.utils.security import get_current_user

router = APIRouter()

@router.get("/security-score")
async def get_security_score(
    user_id: str = Depends(get_current_user)
):
    """Get security score with caching"""
    cache_key = f"security_score:{user_id}"
    
    # Try to get from cache
    cached_score = cache.get(cache_key)
    if cached_score:
        return {"score": float(cached_score), "cached": True}
    
    # Calculate score
    from app.database import SessionLocal
    from app.database import get_user_statistics
    
    db = SessionLocal()
    try:
        score = calculate_security_score(user_id, db)
        
        # Cache for 5 minutes
        cache.set(cache_key, str(score), expire=300)
        
        return {"score": score, "cached": False}
    finally:
        db.close()
```

---

## 6. CELERY TASK INTEGRATION

### 6.1 Celery Configuration

```python
# celery_app.py
from celery import Celery
from app.config import settings

celery_app = Celery(
    "digital_bodyguard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Schedule periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-old-data": {
        "task": "app.tasks.cleanup_old_data",
        "schedule": 86400.0,  # Daily
    },
    "calculate-security-scores": {
        "task": "app.tasks.calculate_all_security_scores",
        "schedule": 3600.0,  # Hourly
    },
}
```

### 6.2 Background Tasks

```python
# tasks.py
from celery import shared_task
from app.database import SessionLocal
from app.models.alert import Alert
from app.models.monitoring import MonitoringData
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_monitoring_data(data: dict):
    """Process monitoring data in background"""
    from app.services.alert_service import AlertService
    
    alert_service = AlertService()
    
    # Check for suspicious activities
    if data.get("suspicious_count", 0) > 0:
        alert = {
            "type": data.get("type"),
            "severity": "high",
            "title": f"Suspicious {data.get('type')} activity",
            "message": f"{data.get('suspicious_count')} suspicious activities detected",
            "data": data
        }
        # Create alert (user_id would be extracted from data)
        alert_service.create_alert(data.get("user_id"), alert)
    
    return {"status": "processed"}

@shared_task
def cleanup_old_data(days_to_keep: int = 90):
    """Clean up old monitoring data"""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        # Delete old monitoring data
        deleted = db.query(MonitoringData).filter(
            MonitoringData.created_at < cutoff_date
        ).delete()
        
        db.commit()
        logger.info(f"Deleted {deleted} old monitoring records")
        
        return {"deleted_count": deleted}
    finally:
        db.close()

@shared_task
def calculate_all_security_scores():
    """Calculate security scores for all users"""
    from app.models.user import User
    from app.database import calculate_security_score
    
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            score = calculate_security_score(user.id, db)
            # Cache the score
            from app.cache import cache
            cache.set(f"security_score:{user.id}", str(score), expire=3600)
        
        return {"processed_users": len(users)}
    finally:
        db.close()
```

### 6.3 Task Integration with API

```python
# api/scan.py (with Celery)
from fastapi import APIRouter, Depends, BackgroundTasks
from app.tasks import process_scan_result

router = APIRouter()

@router.post("/url")
async def scan_url_async(
    request: ScanRequest,
    user_id: str = Depends(get_current_user),
    background_tasks: BackgroundTasks = None
):
    """Scan URL asynchronously"""
    # Submit task to Celery
    task = process_scan_result.delay(request.type, request.target, user_id)
    
    return {
        "task_id": task.id,
        "status": "processing"
    }
```

---

## 7. DOCKER COMPOSE INTEGRATION

### 7.1 Complete Docker Compose

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: digital_bodyguard
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: digital_bodyguard
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U digital_bodyguard"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7.2-alpine
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
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://digital_bodyguard:${DB_PASSWORD}@db:5432/digital_bodyguard
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
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
    environment:
      - DATABASE_URL=postgresql://digital_bodyguard:${DB_PASSWORD}@db:5432/digital_bodyguard
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./backend:/app
      - ./models:/app/models
    depends_on:
      - db
      - redis
    command: celery -A app.celery_app worker --loglevel=info

  # Celery Beat Scheduler
  celery_beat:
    build: ./backend
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    command: celery -A app.celery_app beat --loglevel=info

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000
      - VITE_WS_URL=ws://backend:8000

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
  redis_data:
```

### 7.2 Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream frontend {
        server frontend:80;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # WebSocket
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }

    server {
        listen 443 ssl http2;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://frontend;
        }

        location /api/ {
            proxy_pass http://backend;
        }

        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

---

## 8. ENVIRONMENT CONFIGURATION

### 8.1 Environment Variables

```bash
# .env (root directory)
# Database
DB_PASSWORD=your_secure_password

# Backend
SECRET_KEY=your-secret-key-change-in-production
VIRUSTOTAL_API_KEY=your-virustotal-api-key

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### 8.2 Configuration Management

```python
# config.py (backend - updated)
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    # Application
    APP_NAME: str = "AI Digital Bodyguard API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # Redis
    REDIS_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Model directories
    PHISHING_MODEL_DIR: str = "./models/phishing"
    MALWARE_MODEL_DIR: str = "./models/malware"
    BEHAVIOR_MODEL_DIR: str = "./models/behavior"
    
    # VirusTotal
    VIRUSTOTAL_API_KEY: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024
    UPLOAD_DIR: str = "uploads"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## 9. INTEGRATION TESTING

### 9.1 End-to-End Test

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db, engine, Base
from app.models.user import User
from app.utils.security import get_password_hash

client = TestClient(app)

@pytest.fixture
def db():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_full_scan_workflow(db):
    """Test complete scan workflow"""
    # 1. Register user
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "Test123!",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 200
    
    # 2. Login
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "Test123!"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # 3. Scan URL
    response = client.post(
        "/api/v1/scan/url",
        json={"type": "phishing", "target": "http://example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    scan_result = response.json()
    assert "result" in scan_result
    
    # 4. Get scan history
    response = client.get(
        "/api/v1/scan/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    history = response.json()
    assert len(history) > 0
    
    # 5. Get alerts
    response = client.get(
        "/api/v1/alerts",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_monitoring_data_workflow(db):
    """Test monitoring data workflow"""
    # Create user
    user = User(
        email="monitoring@example.com",
        password_hash=get_password_hash("Test123!"),
        first_name="Monitoring",
        last_name="User"
    )
    db.add(user)
    db.commit()
    
    # Login
    response = client.post("/api/v1/auth/login", data={
        "username": "monitoring@example.com",
        "password": "Test123!"
    })
    token = response.json()["access_token"]
    
    # Send monitoring data
    response = client.post(
        "/api/v1/monitoring/data",
        json={
            "type": "process",
            "data": {"processes": []},
            "suspicious_count": 0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### 9.2 Frontend Integration Test

```typescript
// tests/integration/scan.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Scan from '../../pages/Scan'
import { store } from '../../store'

const queryClient = new QueryClient()

test('URL scan integration', async () => {
  render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Scan />
        </BrowserRouter>
      </QueryClientProvider>
    </Provider>
  )
  
  // Find URL scanner
  const urlInput = screen.getByLabelText(/Enter URL to scan/i)
  const scanButton = screen.getByRole('button', { name: /Scan/i })
  
  // Enter URL
  fireEvent.change(urlInput, { target: { value: 'http://example.com' } })
  
  // Click scan
  fireEvent.click(scanButton)
  
  // Wait for result
  await waitFor(() => {
    expect(screen.getByText(/URL is safe/i)).toBeInTheDocument()
  })
})
```

---

## 10. DEPLOYMENT INTEGRATION

### 10.1 Production Deployment Script

```bash
#!/bin/bash
# deploy.sh

echo "Deploying AI Digital Bodyguard..."

# Stop existing containers
docker-compose down

# Pull latest images
docker-compose pull

# Build images
docker-compose build

# Run database migrations
docker-compose run backend alembic upgrade head

# Start services
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 30

# Run health checks
docker-compose exec backend python -c "from app.database import engine; engine.connect()"

echo "Deployment completed successfully!"
```

### 10.2 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest backend/tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

---

## 11. MONITORING AND LOGGING

### 11.1 Application Monitoring

```python
# monitoring.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI

# Metrics
scan_requests_total = Counter('scan_requests_total', 'Total scan requests')
scan_duration_seconds = Histogram('scan_duration_seconds', 'Scan duration in seconds')

def init_monitoring(app: FastAPI):
    """Initialize monitoring"""
    @app.middleware("http")
    async def monitor_requests(request, call_next):
        scan_requests_total.inc()
        with scan_duration_seconds.time():
            response = await call_next(request)
        return response
    
    @app.get("/metrics")
    async def metrics():
        return generate_latest()
```

### 11.2 Centralized Logging

```python
# logging_config.py
import logging
import sys
from app.config import settings

def setup_logging():
    """Setup centralized logging"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create loggers
    api_logger = logging.getLogger("app.api")
    ml_logger = logging.getLogger("app.ml")
    monitoring_logger = logging.getLogger("app.monitoring")
    
    return {
        "api": api_logger,
        "ml": ml_logger,
        "monitoring": monitoring_logger
    }

loggers = setup_logging()
```

---

## 12. CONCLUSION

This document provides comprehensive integration guidance for the AI-Powered Digital Bodyguard system including:

- **ML Model Integration**: Service layer for phishing, malware, behavior models
- **Backend API Integration**: REST API endpoints with model services
- **Monitoring Agent Integration**: Desktop agent communication with backend
- **Frontend-Backend Integration**: API client, WebSocket, Redux integration
- **Database Integration**: Connection pooling, Redis caching
- **Celery Integration**: Background tasks and scheduled jobs
- **Docker Compose**: Complete multi-container setup
- **Environment Configuration**: Centralized configuration management
- **Integration Testing**: End-to-end test examples
- **Deployment**: Production deployment scripts and CI/CD
- **Monitoring**: Prometheus metrics and centralized logging

**Next Steps:**
1. Set up development environment
2. Configure all environment variables
3. Run database migrations
4. Train and deploy ML models
5. Start all services with Docker Compose
6. Run integration tests
7. Deploy to production

---

## APPENDICES

### Appendix A: Startup Order

```
1. PostgreSQL Database
2. Redis Cache
3. Backend API
4. Celery Worker
5. Celery Beat
6. Frontend
7. Nginx Reverse Proxy
```

### Appendix B: Health Check Endpoints

```python
# Add to main.py
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    health_status = {
        "status": "healthy",
        "services": {}
    }
    
    # Check database
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        from app.cache import cache
        cache.redis_client.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check ML models
    try:
        from app.services.phishing_service import phishing_service
        if phishing_service.detector:
            health_status["services"]["phishing_model"] = "healthy"
        else:
            health_status["services"]["phishing_model"] = "unloaded"
    except Exception as e:
        health_status["services"]["phishing_model"] = f"unhealthy: {str(e)}"
    
    return health_status
```

### Appendix C: Troubleshooting

```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend

# Check database connection
docker-compose exec backend python -c "from app.database import engine; engine.connect()"

# Check Redis connection
docker-compose exec redis redis-cli ping
```
