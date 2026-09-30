# AI Digital Bodyguard - System Architecture

## Overview
AI Digital Bodyguard is a desktop security assistant that runs on Windows, similar to Grammarly, providing real-time protection against phishing, malware, and other cyber threats.

## System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Desktop Application                       │
│                    (PyQt6 System Tray)                       │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│  Local Backend  │   │  Browser       │
│   (FastAPI)     │   │  Extensions    │
└───────┬────────┘   └───────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   AI Engine         │
        │  (ML Models)         │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   Database          │
        │   (SQLite)          │
        └─────────────────────┘
```

### Component Descriptions

#### 1. Desktop Application (PyQt6)
- System tray icon
- Background service
- Configuration management
- Notification system
- Dashboard launcher

#### 2. Local Backend (FastAPI)
- REST API for local communication
- Email analysis service
- URL scanning service
- File scanning service
- System monitoring service
- Alert management

#### 3. Browser Extensions
- Content scripts for page analysis
- Background scripts for API communication
- Popup warnings
- URL interception

#### 4. AI Engine
- Phishing detection model
- Malware detection model
- Email classification model
- Behavior anomaly detection

#### 5. Database (SQLite)
- User settings
- Scan history
- Threat database
- Whitelist/Blacklist

## Technology Stack

### Desktop Application
- **Language**: Python 3.11+
- **GUI Framework**: PyQt6
- **System Integration**: pywin32, psutil
- **System Tray**: QSystemTrayIcon

### Backend
- **Framework**: FastAPI
- **Database**: SQLite
- **Async**: asyncio, aiohttp
- **Process Monitoring**: psutil

### AI/ML
- **Framework**: scikit-learn, XGBoost, TensorFlow
- **NLP**: transformers, spaCy
- **Feature Extraction**: pandas, numpy

### Browser Extensions
- **Language**: JavaScript (ES6+)
- **Manifest**: V3
- **Communication**: WebSocket, HTTP

### Security
- **File Scanning**: YARA rules
- **API Integration**: VirusTotal API
- **Encryption**: cryptography

## Data Flow

### Email Analysis Flow
```
Browser Extension → Read Email Content → Send to Backend → 
AI Analysis → Return Result → Display Warning
```

### Website Monitoring Flow
```
Browser Extension → Capture URL → Send to Backend → 
Phishing Check → Return Result → Show Popup Warning
```

### File Scanning Flow
```
File System Monitor → Detect New File → YARA Scan → 
VirusTotal API → ML Analysis → Return Result → Alert User
```

### System Monitoring Flow
```
System Monitor → Collect Metrics → Anomaly Detection → 
Alert Generation → Dashboard Update
```

## Security Considerations

### Privacy
- All analysis happens locally
- No data sent to external servers (except VirusTotal)
- User consent for all monitoring
- Encrypted local storage

### Performance
- Minimal CPU usage (<5%)
- Memory footprint (<100MB)
- Asynchronous processing
- Background task queuing

### Reliability
- Automatic restart on crash
- Log rotation
- Health checks
- Graceful degradation

## Communication Protocols

### Internal Communication
- Desktop App ↔ Backend: HTTP (localhost)
- Browser Extensions ↔ Backend: HTTP (localhost)
- Backend ↔ AI Engine: Direct function calls
- Backend ↔ Database: SQLite

### External Communication
- Backend ↔ VirusTotal: HTTPS API
- Backend ↔ Threat Intelligence: HTTPS API (optional)

## Deployment Architecture

### Installation
- Windows Installer (MSI/EXE)
- Auto-startup registration
- Browser extension installation
- Database initialization

### Updates
- Auto-update mechanism
- Signature verification
- Rollback capability

## Scalability Considerations

### Single User
- SQLite database sufficient
- Local ML models
- No external dependencies

### Multi-User (Future)
- PostgreSQL database
- Centralized threat intelligence
- Shared ML models
