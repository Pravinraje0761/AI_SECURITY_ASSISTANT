# Testing Strategy
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. TESTING OVERVIEW

This document provides comprehensive testing strategy and implementation for the AI-Powered Digital Bodyguard system.

### 1.1 Testing Objectives

- Ensure system reliability and stability
- Validate ML model accuracy
- Verify API functionality
- Test integration between components
- Ensure security and performance
- Maintain code quality

### 1.2 Testing Levels

- **Unit Testing**: Individual component testing
- **Integration Testing**: Component interaction testing
- **End-to-End Testing**: Complete workflow testing
- **Performance Testing**: Load and stress testing
- **Security Testing**: Vulnerability assessment
- **ML Model Testing**: Model accuracy and validation

### 1.3 Testing Tools

- **Backend**: pytest, pytest-asyncio, pytest-cov
- **Frontend**: Jest, React Testing Library, Cypress
- **API Testing**: Postman, pytest-httpx
- **Performance**: locust, pytest-benchmark
- **Security**: bandit, safety
- **ML Testing**: scikit-learn validation metrics

---

## 2. BACKEND UNIT TESTING

### 2.1 Test Configuration

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create test client"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Create authenticated user and return headers"""
    # Register user
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "Test123!",
        "first_name": "Test",
        "last_name": "User"
    })
    
    # Login
    response = client.post("/api/v1/auth/login", data={
        "username": "test@example.com",
        "password": "Test123!"
    })
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### 2.2 Authentication Tests

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient

def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "first_name": "New",
        "last_name": "User"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["first_name"] == "New"
    assert "id" in data

def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    # First registration
    client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
        "first_name": "First",
        "last_name": "User"
    })
    
    # Duplicate registration
    response = client.post("/api/v1/auth/register", json={
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
        "first_name": "Second",
        "last_name": "User"
    })
    
    assert response.status_code == 400

def test_login_success(client):
    """Test successful login"""
    # Register user first
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "LoginPass123!",
        "first_name": "Login",
        "last_name": "User"
    })
    
    # Login
    response = client.post("/api/v1/auth/login", data={
        "username": "login@example.com",
        "password": "LoginPass123!"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post("/api/v1/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "WrongPass123!"
    })
    
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

def test_unauthorized_access(client):
    """Test access without authentication"""
    response = client.get("/api/v1/auth/me")
    
    assert response.status_code == 401
```

### 2.3 Phishing Detection Tests

```python
# tests/test_phishing.py
import pytest
from unittest.mock import Mock, patch

def test_scan_url_benign(client, auth_headers):
    """Test scanning benign URL"""
    with patch('app.services.phishing_service.PhishingService.scan_url') as mock_scan:
        mock_scan.return_value = {
            "is_phishing": False,
            "probability": 0.15,
            "model_predictions": {}
        }
        
        response = client.post(
            "/api/v1/scan/url",
            json={"type": "phishing", "target": "http://example.com"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "benign"
        assert data["score"] == 0.15

def test_scan_url_malicious(client, auth_headers):
    """Test scanning malicious URL"""
    with patch('app.services.phishing_service.PhishingService.scan_url') as mock_scan:
        mock_scan.return_value = {
            "is_phishing": True,
            "probability": 0.92,
            "model_predictions": {}
        }
        
        response = client.post(
            "/api/v1/scan/url",
            json={"type": "phishing", "target": "http://phishing-site.com"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "malicious"
        assert data["score"] == 0.92

def test_scan_url_invalid_type(client, auth_headers):
    """Test scanning with invalid type"""
    response = client.post(
        "/api/v1/scan/url",
        json={"type": "invalid", "target": "http://example.com"},
        headers=auth_headers
    )
    
    assert response.status_code == 400

def test_get_scan_history(client, auth_headers):
    """Test getting scan history"""
    response = client.get("/api/v1/scan/history", headers=auth_headers)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 2.4 Malware Detection Tests

```python
# tests/test_malware.py
import pytest
from io import BytesIO

def test_scan_file_benign(client, auth_headers):
    """Test scanning benign file"""
    with patch('app.services.malware_service.MalwareService.scan_file') as mock_scan:
        mock_scan.return_value = {
            "is_malware": False,
            "probability": 0.05,
            "model_predictions": {}
        }
        
        file_content = b"Benign file content"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}
        
        response = client.post(
            "/api/v1/scan/file",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "benign"

def test_scan_file_malicious(client, auth_headers):
    """Test scanning malicious file"""
    with patch('app.services.malware_service.MalwareService.scan_file') as mock_scan:
        mock_scan.return_value = {
            "is_malware": True,
            "probability": 0.95,
            "model_predictions": {}
        }
        
        file_content = b"Malicious file content"
        files = {"file": ("malware.exe", BytesIO(file_content), "application/x-msdownload")}
        
        response = client.post(
            "/api/v1/scan/file",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == "malicious"

def test_scan_file_too_large(client, auth_headers):
    """Test scanning file exceeding size limit"""
    # Create large file
    large_content = b"x" * (51 * 1024 * 1024)  # 51 MB
    files = {"file": ("large.txt", BytesIO(large_content), "text/plain")}
    
    response = client.post(
        "/api/v1/scan/file",
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 413  # Payload Too Large
```

### 2.5 Alert Tests

```python
# tests/test_alerts.py
import pytest

def test_create_alert(client, auth_headers):
    """Test creating an alert"""
    response = client.post(
        "/api/v1/alerts",
        json={
            "type": "phishing",
            "severity": "high",
            "title": "Test Alert",
            "message": "This is a test alert"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Alert"
    assert data["severity"] == "high"
    assert data["status"] == "new"

def test_get_alerts(client, auth_headers):
    """Test getting alerts"""
    # Create test alert first
    client.post(
        "/api/v1/alerts",
        json={
            "type": "malware",
            "severity": "critical",
            "title": "Critical Alert",
            "message": "This is critical"
        },
        headers=auth_headers
    )
    
    response = client.get("/api/v1/alerts", headers=auth_headers)
    
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) > 0

def test_acknowledge_alert(client, auth_headers):
    """Test acknowledging an alert"""
    # Create alert
    create_response = client.post(
        "/api/v1/alerts",
        json={
            "type": "network",
            "severity": "medium",
            "title": "Network Alert",
            "message": "Suspicious network activity"
        },
        headers=auth_headers
    )
    alert_id = create_response.json()["id"]
    
    # Acknowledge alert
    response = client.put(f"/api/v1/alerts/{alert_id}/acknowledge", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"

def test_dismiss_alert(client, auth_headers):
    """Test dismissing an alert"""
    # Create alert
    create_response = client.post(
        "/api/v1/alerts",
        json={
            "type": "behavior",
            "severity": "low",
            "title": "Behavior Alert",
            "message": "Anomalous behavior detected"
        },
        headers=auth_headers
    )
    alert_id = create_response.json()["id"]
    
    # Dismiss alert
    response = client.put(f"/api/v1/alerts/{alert_id}/dismiss", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["status"] == "dismissed"
```

### 2.6 Monitoring Tests

```python
# tests/test_monitoring.py
import pytest

def test_receive_monitoring_data(client, auth_headers):
    """Test receiving monitoring data"""
    response = client.post(
        "/api/v1/monitoring/data",
        json={
            "type": "process",
            "data": {"processes": []},
            "suspicious_count": 0
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "received"

def test_receive_heartbeat(client, auth_headers):
    """Test receiving heartbeat"""
    response = client.post(
        "/api/v1/monitoring/heartbeat",
        json={"timestamp": "2026-07-14T10:00:00Z"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

def test_get_monitoring_status(client, auth_headers):
    """Test getting monitoring status"""
    response = client.get("/api/v1/monitoring/status", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "is_active" in data
```

---

## 3. FRONTEND UNIT TESTING

### 3.1 Test Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/tests/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/tests/**',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
}
```

### 3.2 Test Setup

```typescript
// src/tests/setup.ts
import '@testing-library/jest-dom'
import { server } from './mocks/server'

// Start MSW server
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### 3.3 Component Tests

```typescript
// src/tests/components/SecurityScore.test.tsx
import React from 'react'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import SecurityScore from '../../components/dashboard/SecurityScore'
import { store } from '../../store'

const renderWithProvider = (component: React.ReactElement) => {
  return render(
    <Provider store={store}>
      {component}
    </Provider>
  )
}

describe('SecurityScore', () => {
  it('renders security score component', () => {
    renderWithProvider(<SecurityScore />)
    expect(screen.getByText('Security Score')).toBeInTheDocument()
  })

  it('displays score value', () => {
    renderWithProvider(<SecurityScore />)
    expect(screen.getByText('85')).toBeInTheDocument()
  })

  it('shows correct color for high score', () => {
    renderWithProvider(<SecurityScore score={90} />)
    const circularProgress = screen.getByRole('progressbar')
    expect(circularProgress).toHaveStyle({ color: 'rgb(34, 197, 94)' })
  })
})
```

### 3.4 Page Tests

```typescript
// src/tests/pages/Login.test.tsx
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../../pages/Login'

const renderWithRouter = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  )
}

describe('Login Page', () => {
  it('renders login form', () => {
    renderWithRouter(<Login />)
    expect(screen.getByText('Sign in to your account')).toBeInTheDocument()
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument()
  })

  it('shows validation error for invalid email', async () => {
    renderWithRouter(<Login />)
    
    const emailInput = screen.getByLabelText(/Email/i)
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } })
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid email/i)).toBeInTheDocument()
    })
  })

  it('shows validation error for short password', async () => {
    renderWithRouter(<Login />)
    
    const passwordInput = screen.getByLabelText(/Password/i)
    fireEvent.change(passwordInput, { target: { value: '123' } })
    
    await waitFor(() => {
      expect(screen.getByText(/at least 6 characters/i)).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    renderWithRouter(<Login />)
    
    const emailInput = screen.getByLabelText(/Email/i)
    const passwordInput = screen.getByLabelText(/Password/i)
    const submitButton = screen.getByRole('button', { name: /Sign In/i })
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(submitButton).toBeDisabled()
    })
  })
})
```

### 3.5 Service Tests

```typescript
// src/tests/services/authService.test.ts
import authService from '../../services/authService'
import api from '../../services/api'

jest.mock('../../services/api')

describe('AuthService', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('logs in user successfully', async () => {
    const mockResponse = {
      data: {
        access_token: 'test-token',
        refresh_token: 'test-refresh-token',
        token_type: 'bearer'
      }
    }
    
    (api.post as jest.Mock).mockResolvedValue(mockResponse)
    
    const result = await authService.login({
      email: 'test@example.com',
      password: 'password123'
    })
    
    expect(result).toEqual(mockResponse.data)
    expect(api.post).toHaveBeenCalledWith('/api/v1/auth/login', expect.any(FormData))
  })

  it('registers user successfully', async () => {
    const mockResponse = {
      data: {
        id: '123',
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User'
      }
    }
    
    (api.post as jest.Mock).mockResolvedValue(mockResponse)
    
    const result = await authService.register({
      email: 'test@example.com',
      password: 'password123',
      first_name: 'Test',
      last_name: 'User'
    })
    
    expect(result).toEqual(mockResponse.data)
    expect(api.post).toHaveBeenCalledWith('/api/v1/auth/register', expect.any(Object))
  })

  it('handles login error', async () => {
    (api.post as jest.Mock).mockRejectedValue(new Error('Login failed'))
    
    await expect(
      authService.login({
        email: 'test@example.com',
        password: 'wrong-password'
      })
    ).rejects.toThrow('Login failed')
  })
})
```

---

## 4. INTEGRATION TESTING

### 4.1 Backend Integration Tests

```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_full_scan_workflow(client, auth_headers, db):
    """Test complete scan workflow"""
    # 1. Scan URL
    with patch('app.services.phishing_service.PhishingService.scan_url') as mock_scan:
        mock_scan.return_value = {
            "is_phishing": False,
            "probability": 0.15,
            "model_predictions": {}
        }
        
        scan_response = client.post(
            "/api/v1/scan/url",
            json={"type": "phishing", "target": "http://example.com"},
            headers=auth_headers
        )
        assert scan_response.status_code == 200
        scan_id = scan_response.json()["id"]
    
    # 2. Get scan history
    history_response = client.get("/api/v1/scan/history", headers=auth_headers)
    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history) > 0
    
    # 3. Verify scan in history
    scan_ids = [scan["id"] for scan in history]
    assert scan_id in scan_ids

def test_alert_workflow(client, auth_headers, db):
    """Test alert creation and acknowledgment workflow"""
    # 1. Create alert
    create_response = client.post(
        "/api/v1/alerts",
        json={
            "type": "phishing",
            "severity": "high",
            "title": "Test Alert",
            "message": "Test message"
        },
        headers=auth_headers
    )
    assert create_response.status_code == 200
    alert_id = create_response.json()["id"]
    
    # 2. Get alerts
    get_response = client.get("/api/v1/alerts", headers=auth_headers)
    assert get_response.status_code == 200
    alerts = get_response.json()
    assert any(alert["id"] == alert_id for alert in alerts)
    
    # 3. Acknowledge alert
    ack_response = client.put(
        f"/api/v1/alerts/{alert_id}/acknowledge",
        headers=auth_headers
    )
    assert ack_response.status_code == 200
    
    # 4. Verify acknowledged
    get_response = client.get("/api/v1/alerts", headers=auth_headers)
    alerts = get_response.json()
    alert = next((a for a in alerts if a["id"] == alert_id), None)
    assert alert["status"] == "acknowledged"

def test_monitoring_workflow(client, auth_headers, db):
    """Test monitoring data workflow"""
    # 1. Send monitoring data
    data_response = client.post(
        "/api/v1/monitoring/data",
        json={
            "type": "process",
            "data": {"processes": []},
            "suspicious_count": 0
        },
        headers=auth_headers
    )
    assert data_response.status_code == 200
    
    # 2. Send heartbeat
    heartbeat_response = client.post(
        "/api/v1/monitoring/heartbeat",
        json={"timestamp": "2026-07-14T10:00:00Z"},
        headers=auth_headers
    )
    assert heartbeat_response.status_code == 200
    
    # 3. Get monitoring status
    status_response = client.get("/api/v1/monitoring/status", headers=auth_headers)
    assert status_response.status_code == 200
```

### 4.2 Frontend Integration Tests

```typescript
// src/tests/integration/Scan.integration.test.tsx
import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Provider } from 'react-redux'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import Scan from '../../pages/Scan'
import { store } from '../../store'

const queryClient = new QueryClient()

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          {component}
        </BrowserRouter>
      </QueryClientProvider>
    </Provider>
  )
}

describe('Scan Integration', () => {
  it('completes URL scan workflow', async () => {
    renderWithProviders(<Scan />)
    
    // Find URL scanner tab
    const urlTab = screen.getByText(/URL Scanner/i)
    fireEvent.click(urlTab)
    
    // Enter URL
    const urlInput = screen.getByLabelText(/Enter URL to scan/i)
    fireEvent.change(urlInput, { target: { value: 'http://example.com' } })
    
    // Click scan
    const scanButton = screen.getByRole('button', { name: /Scan/i })
    fireEvent.click(scanButton)
    
    // Wait for result
    await waitFor(() => {
      expect(screen.getByText(/URL is safe/i)).toBeInTheDocument()
    })
  })

  it('handles scan error', async () => {
    renderWithProviders(<Scan />)
    
    const urlTab = screen.getByText(/URL Scanner/i)
    fireEvent.click(urlTab)
    
    const scanButton = screen.getByRole('button', { name: /Scan/i })
    fireEvent.click(scanButton)
    
    await waitFor(() => {
      expect(screen.getByText(/Please enter a URL/i)).toBeInTheDocument()
    })
  })
})
```

---

## 5. ML MODEL TESTING

### 5.1 Phishing Model Tests

```python
# tests/ml/test_phishing_model.py
import pytest
import pandas as pd
import numpy as np
from app.ml.phishing_model import PhishingDetector

@pytest.fixture
def phishing_detector():
    """Create phishing detector instance"""
    detector = PhishingDetector("models/phishing")
    return detector

def test_url_feature_extraction(phishing_detector):
    """Test URL feature extraction"""
    url = "http://example.com/login"
    features = phishing_detector.extractor.extract_features(url)
    
    assert features['url_length'] == len(url)
    assert features['has_https'] == 0
    assert features['num_dots'] >= 1

def test_phishing_prediction(phishing_detector):
    """Test phishing prediction"""
    # This test requires trained models
    if not phishing_detector.models:
        pytest.skip("Models not trained")
    
    url = "http://phishing-site.com/login"
    result = phishing_detector.predict_url(url)
    
    assert 'ensemble' in result
    assert 'prediction' in result['ensemble']
    assert 'probability' in result['ensemble']

def test_phishing_model_evaluation(phishing_detector):
    """Test phishing model evaluation"""
    if not phishing_detector.models:
        pytest.skip("Models not trained")
    
    # Create test data
    test_data = pd.DataFrame({
        'url': ['http://example.com', 'http://phishing.com'],
        'label': [0, 1]
    })
    
    results = phishing_detector.evaluate_on_test_set(test_data)
    
    assert 'random_forest' in results
    assert 'xgboost' in results
    assert 'lightgbm' in results
```

### 5.2 Malware Model Tests

```python
# tests/ml/test_malware_model.py
import pytest
import tempfile
import os
from app.ml.malware_model import MalwareDetector

@pytest.fixture
def malware_detector():
    """Create malware detector instance"""
    detector = MalwareDetector("models/malware")
    return detector

def test_pe_feature_extraction(malware_detector):
    """Test PE file feature extraction"""
    # Create a dummy PE file
    with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as f:
        f.write(b'MZ')  # PE header
        temp_path = f.name
    
    try:
        features = malware_detector.extractor.extract_features(temp_path)
        assert 'file_size' in features
        assert 'md5' in features
    finally:
        os.unlink(temp_path)

def test_malware_prediction(malware_detector):
    """Test malware prediction"""
    if not malware_detector.models:
        pytest.skip("Models not trained")
    
    # Create test file
    with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as f:
        f.write(b'MZ')
        temp_path = f.name
    
    try:
        result = malware_detector.predict_file(temp_path)
        assert 'ensemble' in result
        assert 'prediction' in result['ensemble']
    finally:
        os.unlink(temp_path)
```

### 5.3 Behavior Model Tests

```python
# tests/ml/test_behavior_model.py
import pytest
from datetime import datetime
from app.ml.behavior_model import BehaviorAnalyzer

@pytest.fixture
def behavior_analyzer():
    """Create behavior analyzer instance"""
    analyzer = BehaviorAnalyzer("models/behavior")
    return analyzer

def test_behavior_feature_extraction(behavior_analyzer):
    """Test behavior feature extraction"""
    behavior_data = {
        'timestamp': datetime.now().isoformat(),
        'login_attempts': 1,
        'failed_login_attempts': 0,
        'file_access_count': 10,
        'sites_visited': 5,
        'network_activity_mb': 100.0,
        'session_duration': 2.5
    }
    
    features = behavior_analyzer.extractor.extract_features(behavior_data)
    
    assert 'login_hour' in features
    assert 'file_access_count' in features
    assert 'session_duration' in features

def test_behavior_prediction(behavior_analyzer):
    """Test behavior anomaly prediction"""
    if not behavior_analyzer.models:
        pytest.skip("Models not trained")
    
    behavior_data = {
        'timestamp': datetime.now().isoformat(),
        'login_attempts': 10,
        'failed_login_attempts': 8,
        'file_access_count': 500,
        'sites_visited': 200,
        'network_activity_mb': 5000.0,
        'session_duration': 15.0
    }
    
    result = behavior_analyzer.predict_behavior(behavior_data)
    assert 'ensemble' in result
    assert 'prediction' in result['ensemble']
    assert 'anomaly_score' in result['ensemble']
```

---

## 6. END-TO-END TESTING

### 6.1 Cypress Tests

```javascript
// cypress/e2e/login.cy.js
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('successfully logs in with valid credentials', () => {
    cy.get('input[name="email"]').type('test@example.com')
    cy.get('input[name="password"]').type('Test123!')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/dashboard')
    cy.contains('Dashboard').should('be.visible')
  })

  it('shows error with invalid credentials', () => {
    cy.get('input[name="email"]').type('test@example.com')
    cy.get('input[name="password"]').type('wrongpassword')
    cy.get('button[type="submit"]').click()
    
    cy.contains('Incorrect email or password').should('be.visible')
  })

  it('validates email format', () => {
    cy.get('input[name="email"]').type('invalid-email')
    cy.get('input[name="password"]').type('Test123!')
    cy.get('button[type="submit"]').click()
    
    cy.contains('Invalid email').should('be.visible')
  })
})
```

### 6.2 Dashboard E2E Tests

```javascript
// cypress/e2e/dashboard.cy.js
describe('Dashboard Flow', () => {
  beforeEach(() => {
    // Login before each test
    cy.session('login', () => {
      cy.visit('/login')
      cy.get('input[name="email"]').type('test@example.com')
      cy.get('input[name="password"]').type('Test123!')
      cy.get('button[type="submit"]').click()
    })
    
    cy.visit('/dashboard')
  })

  it('displays security score', () => {
    cy.contains('Security Score').should('be.visible')
    cy.contains('85').should('be.visible')
  })

  it('displays threat chart', () => {
    cy.contains('Threat Trends').should('be.visible')
    cy.get('.recharts-wrapper').should('be.visible')
  })

  it('displays alert feed', () => {
    cy.contains('Alert Feed').should('be.visible')
  })

  it('navigates to scan page', () => {
    cy.get('button').contains('Scan').click()
    cy.url().should('include', '/scan')
  })
})
```

### 6.3 Scan E2E Tests

```javascript
// cypress/e2e/scan.cy.js
describe('Scan Flow', () => {
  beforeEach(() => {
    cy.session('login', () => {
      cy.visit('/login')
      cy.get('input[name="email"]').type('test@example.com')
      cy.get('input[name="password"]').type('Test123!')
      cy.get('button[type="submit"]').click()
    })
    
    cy.visit('/scan')
  })

  it('scans URL successfully', () => {
    cy.contains('URL Scanner').click()
    cy.get('input[placeholder*="Enter URL"]').type('http://example.com')
    cy.get('button').contains('Scan').click()
    
    cy.contains('URL is safe', { timeout: 10000 }).should('be.visible')
  })

  it('scans file successfully', () => {
    cy.contains('File Scanner').click()
    cy.get('input[type="file"]').selectFile('cypress/fixtures/test.txt')
    cy.get('button').contains('Scan').click()
    
    cy.contains('File is safe', { timeout: 10000 }).should('be.visible')
  })
})
```

---

## 7. PERFORMANCE TESTING

### 7.1 Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", data={
            "username": "test@example.com",
            "password": "Test123!"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def scan_url(self):
        """Scan URL"""
        self.client.post(
            "/api/v1/scan/url",
            json={"type": "phishing", "target": "http://example.com"},
            headers=self.headers
        )
    
    @task(2)
    def get_alerts(self):
        """Get alerts"""
        self.client.get("/api/v1/alerts", headers=self.headers)
    
    @task(1)
    def get_dashboard(self):
        """Get dashboard data"""
        self.client.get("/api/v1/dashboard/stats", headers=self.headers)
```

### 7.2 Performance Tests with pytest-benchmark

```python
# tests/test_performance.py
import pytest
from app.services.phishing_service import PhishingService

@pytest.mark.benchmark(group="phishing_scan")
def test_phishing_scan_performance(benchmark):
    """Benchmark phishing scan performance"""
    service = PhishingService()
    
    def scan_url():
        return service.scan_url("http://example.com")
    
    result = benchmark(scan_url)
    assert result is not None

@pytest.mark.benchmark(group="malware_scan")
def test_malware_scan_performance(benchmark):
    """Benchmark malware scan performance"""
    from app.services.malware_service import MalwareService
    service = MalwareService()
    
    def scan_file():
        return service.scan_file(b"test content", "test.txt")
    
    result = benchmark(scan_file)
    assert result is not None
```

---

## 8. SECURITY TESTING

### 8.1 Security Tests with Bandit

```bash
# Run bandit security scanner
bandit -r backend/app -f json -o security_report.json
```

### 8.2 Security Tests

```python
# tests/test_security.py
import pytest

def test_sql_injection_protection(client):
    """Test SQL injection protection"""
    response = client.post("/api/v1/auth/login", data={
        "username": "admin' OR '1'='1",
        "password": "password"
    })
    
    assert response.status_code == 401

def test_xss_protection(client, auth_headers):
    """Test XSS protection"""
    response = client.post(
        "/api/v1/alerts",
        json={
            "type": "test",
            "severity": "low",
            "title": "<script>alert('xss')</script>",
            "message": "Test"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    # Verify script tag is escaped in response
    assert "<script>" not in response.text

def test_rate_limiting(client):
    """Test rate limiting"""
    # Make multiple requests quickly
    for _ in range(100):
        response = client.get("/api/v1/health")
        if response.status_code == 429:
            break
    
    # Should be rate limited
    assert response.status_code == 429

def test_csrf_protection(client):
    """Test CSRF protection"""
    # CSRF tokens should be required for state-changing operations
    response = client.post("/api/v1/auth/logout")
    # Should fail without CSRF token
    assert response.status_code in [401, 403]
```

---

## 9. TEST COVERAGE

### 9.1 Coverage Configuration

```ini
# .coveragerc
[run]
source = backend/app
omit = 
    backend/app/tests/*
    backend/app/__init__.py
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

### 9.2 Running Coverage

```bash
# Backend coverage
pytest backend/tests/ --cov=backend/app --cov-report=html --cov-report=term

# Frontend coverage
npm test -- --coverage --watchAll=false
```

### 9.3 Coverage Targets

- **Backend**: 80% coverage minimum
- **Frontend**: 75% coverage minimum
- **Critical Paths**: 90% coverage minimum

---

## 10. TEST AUTOMATION

### 10.1 GitHub Actions CI/CD

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          npm install -D cypress
      
      - name: Run E2E tests
        run: |
          cd frontend
          npx cypress run
      
      - name: Upload screenshots
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: cypress-screenshots
          path: frontend/cypress/screenshots
```

### 10.2 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 11. TEST DATA MANAGEMENT

### 11.1 Test Data Fixtures

```python
# tests/fixtures/test_data.py
import pytest
from datetime import datetime
from app.models.user import User
from app.models.alert import Alert
from app.models.scan import Scan
from app.utils.security import get_password_hash

@pytest.fixture
def test_user(db):
    """Create test user"""
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("Test123!"),
        first_name="Test",
        last_name="User",
        role="user",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_alert(db, test_user):
    """Create test alert"""
    alert = Alert(
        user_id=test_user.id,
        type="phishing",
        severity="high",
        title="Test Alert",
        message="This is a test alert",
        status="new"
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@pytest.fixture
def test_scan(db, test_user):
    """Create test scan"""
    scan = Scan(
        user_id=test_user.id,
        type="phishing",
        target="http://example.com",
        result="benign",
        score=0.15
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan
```

---

## 12. CONCLUSION

This document provides comprehensive testing strategy for the AI-Powered Digital Bodyguard system including:

- **Backend Unit Tests**: pytest-based tests for API endpoints
- **Frontend Unit Tests**: Jest and React Testing Library tests
- **Integration Tests**: Component interaction testing
- **ML Model Tests**: Model accuracy and validation tests
- **E2E Tests**: Cypress end-to-end workflow tests
- **Performance Tests**: Load testing with Locust
- **Security Tests**: Vulnerability assessment
- **Test Coverage**: Coverage targets and reporting
- **CI/CD**: Automated testing with GitHub Actions
- **Test Automation**: Pre-commit hooks and continuous integration

**Next Steps:**
1. Set up test environment
2. Write unit tests for all components
3. Implement integration tests
4. Set up E2E tests
5. Configure CI/CD pipeline
6. Monitor test coverage
7. Run tests regularly
8. Maintain test suite

---

## APPENDICES

### Appendix A: Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html

# Frontend tests
cd frontend
npm test
npm test -- --coverage

# E2E tests
cd frontend
npx cypress open
npx cypress run

# Performance tests
locust -f locustfile.py --host=http://localhost:8000
```

### Appendix B: Test Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Generate XML coverage report for CI
pytest --cov=app --cov-report=xml

# Generate JUnit XML report
pytest --junitxml=test-results.xml
```

### Appendix C: Test Database

```python
# Create test database
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Drop test database
python -c "from app.database import engine, Base; Base.metadata.drop_all(bind=engine)"
```
