# AI Digital Bodyguard - Folder Structure

## Complete Project Architecture

```
ai_digital_bodyguard/
├── README.md
├── ARCHITECTURE.md
├── FOLDER_STRUCTURE.md
├── requirements.txt
├── setup.py
├── config.yaml
├── .gitignore
│
├── desktop_app/                    # PyQt6 Desktop Application
│   ├── __init__.py
│   ├── main.py                     # Application entry point
│   ├── system_tray.py              # System tray icon and menu
│   ├── config_manager.py           # Configuration management
│   ├── notification_manager.py     # Desktop notifications
│   ├── auto_startup.py             # Windows auto-startup
│   ├── dashboard_launcher.py       # Dashboard window launcher
│   ├── resources/
│   │   ├── icons/
│   │   │   ├── tray_icon.ico
│   │   │   ├── safe.png
│   │   │   ├── suspicious.png
│   │   │   └── dangerous.png
│   │   └── sounds/
│   │       ├── alert.wav
│   │       └── safe.wav
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py
│       ├── settings_dialog.py
│       └── dashboard_window.py
│
├── backend/                        # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                     # FastAPI application
│   ├── config.py                   # Configuration
│   ├── database.py                 # Database setup
│   ├── models/                     # SQLAlchemy Models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── scan_history.py
│   │   ├── threat.py
│   │   └── whitelist.py
│   ├── schemas/                    # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── url.py
│   │   ├── file.py
│   │   └── alert.py
│   ├── api/                        # API Routes
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── url.py
│   │   ├── file.py
│   │   ├── system.py
│   │   └── dashboard.py
│   ├── services/                   # Business Logic
│   │   ├── __init__.py
│   │   ├── email_analyzer.py
│   │   ├── url_scanner.py
│   │   ├── file_scanner.py
│   │   ├── system_monitor.py
│   │   └── alert_manager.py
│   ├── utils/                      # Utilities
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── logger.py
│   │   └── validators.py
│   └── database/
│       └── digital_bodyguard.db
│
├── ai_engine/                      # AI/ML Models
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── phishing_detector.py
│   │   ├── malware_detector.py
│   │   ├── email_classifier.py
│   │   └── behavior_analyzer.py
│   ├── training/
│   │   ├── __init__.py
│   │   ├── train_phishing.py
│   │   ├── train_malware.py
│   │   └── train_email.py
│   ├── data/
│   │   ├── phishing_dataset.csv
│   │   ├── malware_dataset.csv
│   │   └── email_dataset.csv
│   ├── models_saved/
│   │   ├── phishing_model.pkl
│   │   ├── malware_model.pkl
│   │   └── email_model.pkl
│   └── features/
│       ├── __init__.py
│       ├── url_features.py
│       ├── email_features.py
│       └── file_features.py
│
├── browser_extensions/             # Browser Extensions
│   ├── chrome/
│   │   ├── manifest.json
│   │   ├── background.js
│   │   ├── content.js
│   │   ├── popup.html
│   │   ├── popup.js
│   │   ├── icons/
│   │   │   ├── icon16.png
│   │   │   ├── icon48.png
│   │   │   └── icon128.png
│   │   └── styles/
│   │       └── popup.css
│   ├── edge/
│   │   ├── manifest.json
│   │   ├── background.js
│   │   ├── content.js
│   │   ├── popup.html
│   │   ├── popup.js
│   │   ├── icons/
│   │   └── styles/
│   └── firefox/
│       ├── manifest.json
│       ├── background.js
│       ├── content.js
│       ├── popup.html
│       ├── popup.js
│       ├── icons/
│       └── styles/
│
├── file_monitor/                   # File System Monitor
│   ├── __init__.py
│   ├── monitor.py                  # File system watcher
│   ├── yara_rules/
│   │   ├── malware.yara
│   │   ├── suspicious.yara
│   │   └── custom.yara
│   └── scanners/
│       ├── __init__.py
│       ├── yara_scanner.py
│       ├── virustotal_scanner.py
│       └── ml_scanner.py
│
├── system_monitor/                 # System Monitoring
│   ├── __init__.py
│   ├── process_monitor.py
│   ├── network_monitor.py
│   ├── startup_monitor.py
│   └── registry_monitor.py
│
├── dashboard/                      # Web Dashboard
│   ├── index.html
│ ├── css/
│   │   ├── main.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── main.js
│   │   ├── charts.js
│   │   └── api.js
│   └── assets/
│       └── images/
│
├── tests/                          # Tests
│   ├── __init__.py
│   ├── test_api/
│   ├── test_models/
│   ├── test_services/
│   └── test_integration/
│
├── docs/                           # Documentation
│   ├── API.md
│   ├── INSTALLATION.md
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
│
└── scripts/                        # Utility Scripts
    ├── install.py
    ├── uninstall.py
    ├── update.py
    └── backup.py
```

## Key Components Explained

### desktop_app/
- Main PyQt6 application that runs in system tray
- Handles user interactions and notifications
- Manages configuration and auto-startup

### backend/
- FastAPI server running on localhost
- Provides REST API for all components
- Handles business logic and database operations

### ai_engine/
- Machine learning models for threat detection
- Training scripts and datasets
- Feature extraction utilities

### browser_extensions/
- Chrome, Edge, and Firefox extensions
- Content scripts for page analysis
- Background scripts for API communication

### file_monitor/
- Real-time file system monitoring
- YARA rules for malware detection
- Integration with VirusTotal API

### system_monitor/
- Process and network monitoring
- Startup program tracking
- Registry change detection

### dashboard/
- Web-based security dashboard
- Real-time threat visualization
- Historical data and reports

## Installation Structure

After installation, the application will be deployed to:

```
C:\Program Files\AI Digital Bodyguard\
├── ai_digital_bodyguard.exe
├── config.yaml
├── models/
├── database/
└── resources/
```

User data will be stored in:

```
C:\Users\<username>\AppData\Local\AI Digital Bodyguard\
├── digital_bodyguard.db
├── logs/
├── cache/
└── settings.yaml
```
