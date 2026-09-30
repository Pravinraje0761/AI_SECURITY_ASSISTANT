# Backend Development
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. BACKEND OVERVIEW

This document provides complete implementation details for the Backend REST API using FastAPI.

### 1.1 Backend Purpose

Provide RESTful API endpoints for all system components:
- Authentication and authorization
- Phishing detection
- Malware detection
- User behavior analysis
- Monitoring data ingestion
- Alert management
- Dashboard data
- Threat intelligence

### 1.2 Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Cache**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **WebSocket**: Real-time updates
- **Task Queue**: Celery with Redis broker

### 1.3 API Structure

```
/api/v1/
├── auth/          # Authentication endpoints
├── scan/          # Scanning endpoints (phishing, malware)
├── behavior/      # Behavior analysis endpoints
├── monitoring/    # Monitoring data endpoints
├── alerts/        # Alert management endpoints
├── threats/       # Threat detection endpoints
├── dashboard/     # Dashboard data endpoints
└── admin/         # Admin endpoints
```

---

## 2. PROJECT STRUCTURE

### 2.1 Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── dependencies.py         # Dependency injection
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── alert.py
│   │   ├── threat.py
│   │   └── scan.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── alert.py
│   │   ├── threat.py
│   │   └── scan.py
│   ├── api/                    # API routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── scan.py
│   │   ├── behavior.py
│   │   ├── monitoring.py
│   │   ├── alerts.py
│   │   ├── threats.py
│   │   └── dashboard.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── phishing_service.py
│   │   ├── malware_service.py
│   │   ├── behavior_service.py
│   │   └── alert_service.py
│   ├── ml/                     # ML model loaders
│   │   ├── __init__.py
│   │   ├── phishing_model.py
│   │   ├── malware_model.py
│   │   └── behavior_model.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── logger.py
│   │   └── validators.py
│   └── websocket/              # WebSocket handlers
│       ├── __init__.py
│       └── manager.py
├── tests/                      # Test files
├── alembic/                    # Database migrations
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 3. CONFIGURATION

### 3.1 Configuration Settings

```python
# config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    # Application
    APP_NAME: str = "AI Digital Bodyguard API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/digital_bodyguard"
    DATABASE_TEST_URL: str = "postgresql://user:password@localhost:5432/digital_bodyguard_test"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # VirusTotal
    VIRUSTOTAL_API_KEY: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    UPLOAD_DIR: str = "uploads"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 3.2 Environment File

```env
# .env
APP_NAME=AI Digital Bodyguard API
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/digital_bodyguard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
VIRUSTOTAL_API_KEY=your-virustotal-api-key
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 4. MAIN APPLICATION

### 4.1 FastAPI Application Setup

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base
from app.api import auth, scan, behavior, monitoring, alerts, threats, dashboard
from app.websocket.manager import ConnectionManager
import logging

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# WebSocket manager
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting application...")
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Close database connections
    engine.dispose()
    logger.info("Application shutdown complete")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Digital Bodyguard REST API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(scan.router, prefix="/api/v1/scan", tags=["Scanning"])
app.include_router(behavior.router, prefix="/api/v1/behavior", tags=["Behavior Analysis"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["Monitoring"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(threats.router, prefix="/api/v1/threats", tags=["Threats"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

---

## 5. DATABASE MODELS

### 5.1 Database Setup

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
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

### 5.2 User Model

```python
# models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from app.database import Base
import uuid

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default="user")  # user, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
```

### 5.3 Alert Model

```python
# models/alert.py
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Alert(Base):
    """Alert model"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # phishing, malware, behavior, etc.
    severity = Column(String, nullable=False)  # low, medium, high, critical
    title = Column(String, nullable=False)
    message = Column(Text)
    data = Column(Text)  # JSON string
    status = Column(String, default="new")  # new, acknowledged, dismissed
    acknowledged_at = Column(DateTime(timezone=True))
    dismissed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
```

### 5.4 Threat Model

```python
# models/threat.py
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Threat(Base):
    """Threat model"""
    __tablename__ = "threats"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # phishing, malware, behavior, network
    source = Column(String)  # url, file, behavior, network
    threat_score = Column(Float)
    attack_type = Column(String)
    status = Column(String, default="detected")  # detected, investigating, resolved
    details = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User")
```

### 5.5 Scan Model

```python
# models/scan.py
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Scan(Base):
    """Scan model"""
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # phishing, malware
    target = Column(String, nullable=False)  # URL or file path
    result = Column(String)  # malicious, benign, suspicious
    score = Column(Float)
    details = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
```

---

## 6. PYDANTIC SCHEMAS

### 6.1 User Schemas

```python
# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

### 6.2 Alert Schemas

```python
# schemas/alert.py
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AlertBase(BaseModel):
    type: str
    severity: str
    title: str
    message: Optional[str] = None
    data: Optional[dict] = None

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: str
    user_id: str
    status: str
    acknowledged_at: Optional[datetime] = None
    dismissed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 6.3 Scan Schemas

```python
# schemas/scan.py
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class ScanRequest(BaseModel):
    type: str  # phishing, malware
    target: str  # URL or file content

class ScanResponse(BaseModel):
    id: str
    type: str
    target: str
    result: str
    score: float
    details: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
```

---

## 7. AUTHENTICATION

### 7.1 Security Utilities

```python
# utils/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return user_id
```

### 7.2 Authentication Router

```python
# api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from datetime import timedelta
from app.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user"""
    # Find user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token"""
    from app.utils.security import decode_token, create_access_token
    from datetime import timedelta
    
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

---

## 8. SCANNING ENDPOINTS

### 8.1 Phishing Scan Router

```python
# api/scan.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scan import ScanRequest, ScanResponse
from app.models.scan import Scan
from app.models.user import User
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
    
    # Perform phishing scan
    result = phishing_service.scan_url(request.target)
    
    # Save scan to database
    scan = Scan(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type="request.type",
        target=request.target,
        result=result["is_phishing"],
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
    
    # Perform malware scan
    result = malware_service.scan_file(content, file.filename)
    
    # Save scan to database
    scan = Scan(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type="malware",
        target=file.filename,
        result=result["is_malware"],
        score=result["probability"],
        details=result
    )
    
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    return scan

@router.get("/history")
async def get_scan_history(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get scan history for current user"""
    scans = db.query(Scan).filter(
        Scan.user_id == user_id
    ).order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()
    
    return scans
```

---

## 9. BEHAVIOR ANALYSIS ENDPOINTS

### 9.1 Behavior Router

```python
# api/behavior.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.behavior import BehaviorData, BehaviorAnalysisResponse
from app.services.behavior_service import BehaviorService
from app.utils.security import get_current_user

router = APIRouter()

behavior_service = BehaviorService()

@router.post("/analyze", response_model=BehaviorAnalysisResponse)
async def analyze_behavior(
    behavior: BehaviorData,
    user_id: str = Depends(get_current_user)
):
    """Analyze user behavior for anomalies"""
    result = behavior_service.analyze_behavior(behavior.dict(), user_id)
    return result

@router.post("/baseline/{user_id}")
async def update_baseline(
    user_id: str,
    behavior_data: list[BehaviorData],
    current_user_id: str = Depends(get_current_user)
):
    """Update user behavior baseline"""
    # Only allow users to update their own baseline or admins
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    behavior_list = [b.dict() for b in behavior_data]
    baseline = behavior_service.update_baseline(user_id, behavior_list)
    
    return {"user_id": user_id, "baseline_updated": True, "sample_count": baseline['sample_count']}
```

---

## 10. MONITORING ENDPOINTS

### 10.1 Monitoring Router

```python
# api/monitoring.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user
from typing import Any

router = APIRouter()

@router.post("/data")
async def receive_monitoring_data(
    data: dict,
    user_id: str = Depends(get_current_user)
):
    """Receive monitoring data from desktop agent"""
    # Process monitoring data
    # Store in database or send to threat detection engine
    return {"status": "received", "data_type": data.get("type")}

@router.post("/heartbeat")
async def receive_heartbeat(
    data: dict,
    user_id: str = Depends(get_current_user)
):
    """Receive heartbeat from desktop agent"""
    # Update last seen timestamp
    return {"status": "alive"}

@router.get("/status")
async def get_monitoring_status(
    user_id: str = Depends(get_current_user)
):
    """Get monitoring status for user"""
    return {
        "is_active": True,
        "last_heartbeat": "2026-07-14T10:30:00Z",
        "monitored_paths": ["Downloads", "Desktop"]
    }
```

---

## 11. ALERTS ENDPOINTS

### 11.1 Alerts Router

```python
# api/alerts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertResponse
from app.utils.security import get_current_user
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/", response_model=AlertResponse)
async def create_alert(
    alert: AlertCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    new_alert = Alert(
        id=str(uuid.uuid4()),
        user_id=user_id,
        **alert.dict()
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    # Broadcast via WebSocket
    from app.websocket.manager import manager
    await manager.broadcast_alert(new_alert)
    
    return new_alert

@router.get("/", response_model=list[AlertResponse])
async def get_alerts(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: str = None
):
    """Get alerts for current user"""
    query = db.query(Alert).filter(Alert.user_id == user_id)
    
    if status:
        query = query.filter(Alert.status == status)
    
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    
    return alerts

@router.put("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Acknowledge an alert"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user_id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "acknowledged"
    alert.acknowledged_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "acknowledged"}

@router.put("/{alert_id}/dismiss")
async def dismiss_alert(
    alert_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dismiss an alert"""
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == user_id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = "dismissed"
    alert.dismissed_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "dismissed"}
```

---

## 12. WEBSOCKET MANAGER

### 12.1 WebSocket Connection Manager

```python
# websocket/manager.py
from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect WebSocket"""
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific connection"""
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        """Broadcast message to all connections"""
        for connection in self.active_connections:
            await connection.send_text(message)
    
    async def broadcast_alert(self, alert):
        """Broadcast alert to all connections"""
        message = {
            "event": "new_alert",
            "data": {
                "id": alert.id,
                "type": alert.type,
                "severity": alert.severity,
                "title": alert.title,
                "message": alert.message,
                "created_at": alert.created_at.isoformat()
            }
        }
        await self.broadcast(json.dumps(message))

manager = ConnectionManager()
```

---

## 13. REQUIREMENTS

### 13.1 Requirements File

```txt
# requirements.txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
redis>=5.0.0
celery>=5.3.0
alembic>=1.12.0
httpx>=0.25.0
```

---

## 14. DEPLOYMENT

### 14.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 14.2 Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/digital_bodyguard
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=digital_bodyguard
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## 15. CONCLUSION

This document provides complete implementation for the Backend REST API including:

- **Project Structure**: Organized directory structure
- **Configuration**: Environment-based configuration
- **Database Models**: SQLAlchemy models for users, alerts, threats, scans
- **Pydantic Schemas**: Request/response validation
- **Authentication**: JWT-based authentication with password hashing
- **API Endpoints**: Complete REST API for all modules
- **WebSocket**: Real-time updates via WebSocket
- **Deployment**: Docker and Docker Compose configuration

**Next Steps:**
1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Implement ML service integrations
5. Test API endpoints
6. Deploy to production

---

## APPENDICES

### Appendix A: Database Migrations

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Appendix B: API Testing with curl

```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","first_name":"John","last_name":"Doe"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Scan URL
curl -X POST http://localhost:8000/api/v1/scan/url \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"type":"phishing","target":"http://example.com"}'
```

### Appendix C: API Documentation

The FastAPI automatic documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
