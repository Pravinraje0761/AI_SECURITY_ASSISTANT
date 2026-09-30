# Module Design Document
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. MODULE OVERVIEW

The AI-Powered Digital Bodyguard system is divided into 8 core modules, each responsible for specific functionality. This document provides detailed design for each module.

### Module Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MODULE ARCHITECTURE                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   MODULE 1       │
│  Authentication  │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 2       │
│  System Monitor  │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 3       │
│ Phishing Detect  │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 4       │
│ Malware Detect   │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 5       │
│ Behavior Analysis│
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 6       │
│ Threat Detection │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 7       │
│  Alert System    │
└────────┬─────────┘
         │
┌────────▼─────────┐
│   MODULE 8       │
│   Dashboard      │
└──────────────────┘
```

---

## 2. MODULE 1: USER AUTHENTICATION

### 2.1 Module Overview

**Purpose**: Manage user authentication, authorization, and session management

**Responsibilities**:
- User registration and login
- JWT token generation and validation
- Password hashing and verification
- Session management
- Password reset functionality

### 2.2 Features

#### 2.2.1 User Registration
- **Description**: Allow new users to create accounts
- **Input**: Email, password, first name, last name
- **Output**: User ID, JWT token
- **Validation**: Email format, password strength, email uniqueness

#### 2.2.2 User Login
- **Description**: Authenticate existing users
- **Input**: Email, password
- **Output**: JWT token, refresh token
- **Validation**: Credentials verification, account status

#### 2.2.3 JWT Authentication
- **Description**: Token-based authentication
- **Token Type**: Access token (15 min), Refresh token (7 days)
- **Algorithm**: RS256 (asymmetric) or HS256 (symmetric)

#### 2.2.4 Password Hashing
- **Description**: Secure password storage
- **Algorithm**: bcrypt with salt rounds = 12
- **Security**: Never store plain text passwords

#### 2.2.5 Session Management
- **Description**: Manage active user sessions
- **Features**: Session creation, validation, revocation
- **Storage**: Redis for fast access

#### 2.2.6 Password Reset
- **Description**: Allow users to reset forgotten passwords
- **Flow**: Email verification → Token generation → Password update

### 2.3 Components

#### 2.3.1 User Model
```python
class User:
    user_id: UUID
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime
    last_login: datetime
    is_active: bool
```

#### 2.3.2 Session Model
```python
class Session:
    session_id: UUID
    user_id: UUID
    token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime
```

#### 2.3.3 Authentication Service
```python
class AuthService:
    def register(self, email: str, password: str, first_name: str, last_name: str) -> dict
    def login(self, email: str, password: str) -> dict
    def logout(self, token: str) -> bool
    def refresh_token(self, refresh_token: str) -> dict
    def verify_token(self, token: str) -> dict
    def reset_password(self, email: str, new_password: str) -> bool
```

#### 2.3.4 Password Hasher
```python
class PasswordHasher:
    def hash_password(self, password: str) -> str
    def verify_password(self, password: str, hash: str) -> bool
```

#### 2.3.5 JWT Manager
```python
class JWTManager:
    def generate_access_token(self, user_id: UUID) -> str
    def generate_refresh_token(self, user_id: UUID) -> str
    def decode_token(self, token: str) -> dict
    def verify_token(self, token: str) -> bool
```

### 2.4 Data Flow

```
User Registration Flow:
1. User submits registration form
2. AuthService validates input
3. PasswordHasher hashes password
4. User created in database
5. JWTManager generates tokens
6. Session stored in Redis
7. Tokens returned to user

User Login Flow:
1. User submits login form
2. AuthService validates credentials
3. PasswordHasher verifies password
4. JWTManager generates tokens
5. Session stored in Redis
6. Last login updated
7. Tokens returned to user

Token Validation Flow:
1. API request with JWT token
2. JWTMiddleware extracts token
3. JWTManager verifies token
4. User ID extracted from token
5. Session validated in Redis
6. Request proceeds if valid
```

### 2.5 API Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/me
PUT    /api/v1/auth/profile
```

### 2.6 Dependencies

- **Database**: PostgreSQL (user storage)
- **Cache**: Redis (session storage)
- **Security**: bcrypt, python-jose
- **Email**: SendGrid/SMTP (password reset)

### 2.7 Implementation Details

**Password Strength Requirements**:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character

**JWT Token Payload**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "user",
  "iat": 1234567890,
  "exp": 1234568890
}
```

**Security Measures**:
- Rate limiting on login attempts (5 per minute)
- Account lockout after 10 failed attempts (15 minutes)
- Token expiration (access: 15 min, refresh: 7 days)
- HTTPS only for token transmission

---

## 3. MODULE 2: REAL-TIME SYSTEM MONITORING

### 3.1 Module Overview

**Purpose**: Monitor system activities in real-time for threat detection

**Responsibilities**:
- Process monitoring
- CPU and RAM usage tracking
- Network connection monitoring
- File system change detection
- Browser activity tracking
- Data collection and transmission

### 3.2 Features

#### 3.2.1 Process Monitoring
- **Description**: Monitor running processes
- **Data Collected**: PID, name, CPU usage, memory usage, start time, status
- **Frequency**: Every 5 seconds
- **Alert Threshold**: CPU > 80%, Memory > 90%

#### 3.2.2 CPU Usage Monitoring
- **Description**: Track CPU utilization
- **Metrics**: Overall CPU %, per-core usage
- **Frequency**: Every 2 seconds
- **Alert Threshold**: > 90% for 30 seconds

#### 3.2.3 RAM Usage Monitoring
- **Description**: Track memory utilization
- **Metrics**: Total RAM, used RAM, available RAM, swap usage
- **Frequency**: Every 2 seconds
- **Alert Threshold**: > 90%

#### 3.2.4 Network Connection Monitoring
- **Description**: Monitor active network connections
- **Data Collected**: Local IP/port, remote IP/port, protocol, status, process
- **Frequency**: Every 5 seconds
- **Alert**: Suspicious connections (unknown IPs, unusual ports)

#### 3.2.5 File System Monitoring
- **Description**: Detect file system changes
- **Events**: Create, modify, delete, move
- **Monitored Paths**: User directories, downloads, desktop
- **Frequency**: Real-time (inotify/watchdog)

#### 3.2.6 Browser Activity Monitoring
- **Description**: Track browser activities
- **Data Collected**: URLs visited, download history, extensions
- **Supported Browsers**: Chrome, Firefox, Edge
- **Privacy**: User consent required

### 3.3 Components

#### 3.3.1 Monitoring Service
```python
class MonitoringService:
    def start_monitoring(self) -> bool
    def stop_monitoring(self) -> bool
    def get_status(self) -> dict
    def collect_data(self) -> dict
    def send_data(self, data: dict) -> bool
```

#### 3.3.2 Process Monitor
```python
class ProcessMonitor:
    def get_processes(self) -> List[ProcessInfo]
    def get_process_details(self, pid: int) -> ProcessDetails
    def kill_process(self, pid: int) -> bool
    def detect_suspicious_process(self, process: ProcessInfo) -> bool
```

#### 3.3.3 Resource Monitor
```python
class ResourceMonitor:
    def get_cpu_usage(self) -> float
    def get_ram_usage(self) -> float
    def get_disk_usage(self) -> float
    def get_network_stats(self) -> NetworkStats
```

#### 3.3.4 Network Monitor
```python
class NetworkMonitor:
    def get_connections(self) -> List[Connection]
    def get_network_traffic(self) -> NetworkTraffic
    def detect_suspicious_connection(self, conn: Connection) -> bool
    def block_connection(self, conn: Connection) -> bool
```

#### 3.3.5 File Monitor
```python
class FileMonitor:
    def start_watching(self, path: str) -> bool
    def stop_watching(self) -> bool
    def get_changes(self) -> List[FileEvent]
    def detect_suspicious_file(self, event: FileEvent) -> bool
```

#### 3.3.6 Browser Monitor
```python
class BrowserMonitor:
    def get_browser_history(self) -> List[URLVisit]
    def get_downloads(self) -> List[Download]
    def get_extensions(self) -> List[Extension]
    def detect_suspicious_url(self, url: str) -> bool
```

### 3.4 Data Flow

```
Monitoring Data Collection Flow:
1. MonitoringService starts
2. ProcessMonitor collects process data every 5s
3. ResourceMonitor collects CPU/RAM every 2s
4. NetworkMonitor collects connections every 5s
5. FileMonitor watches for changes in real-time
6. BrowserMonitor tracks browser activities
7. All data aggregated
8. Data sent to backend API
9. Data stored in database
10. Threat Detection Engine analyzes data
```

### 3.5 API Endpoints

```
POST   /api/v1/monitoring/start
POST   /api/v1/monitoring/stop
GET    /api/v1/monitoring/status
GET    /api/v1/monitoring/processes
GET    /api/v1/monitoring/resources
GET    /api/v1/monitoring/network
GET    /api/v1/monitoring/files
GET    /api/v1/monitoring/browser
GET    /api/v1/monitoring/history
```

### 3.6 Dependencies

- **System Monitoring**: psutil
- **File Monitoring**: watchdog
- **Network Monitoring**: psutil, scapy
- **Browser Monitoring**: browser history APIs
- **Data Transmission**: HTTP requests to backend

### 3.7 Implementation Details

**Data Collection Intervals**:
- CPU/RAM: 2 seconds
- Processes: 5 seconds
- Network: 5 seconds
- Files: Real-time
- Browser: 10 seconds

**Suspicious Process Detection**:
- High CPU usage (>80%)
- High memory usage (>1GB)
- Unknown publisher
- Suspicious name patterns
- Running from temp directory

**Suspicious Connection Detection**:
- Connections to known malicious IPs
- Unusual ports (6666, 31337, etc.)
- Connections to non-HTTPS sites
- High data transfer rates
- Connections at unusual times

**File Monitoring Paths**:
- Windows: C:\Users\{username}\Downloads
- Windows: C:\Users\{username}\Desktop
- Windows: C:\Users\{username}\Documents
- Linux: /home/{username}/Downloads
- Linux: /home/{username}/Desktop

---

## 4. MODULE 3: PHISHING DETECTION SYSTEM

### 4.1 Module Overview

**Purpose**: Detect phishing URLs and fake websites

**Responsibilities**:
- URL feature extraction
- Domain age checking
- SSL certificate verification
- Machine learning classification
- VirusTotal integration
- Phishing report generation

### 4.2 Features

#### 4.2.1 URL Feature Extraction
- **Description**: Extract features from URL for ML model
- **Features**:
  - URL length
  - Number of dots
  - Number of digits
  - Number of special characters
  - Subdomain count
  - Path length
  - Query parameter count
  - HTTPS usage (binary)
  - IP address in URL (binary)
  - TLD (Top Level Domain)

#### 4.2.2 Domain Age Checking
- **Description**: Check domain registration age
- **Method**: WHOIS lookup
- **Threshold**: < 30 days = suspicious
- **API**: python-whois

#### 4.2.3 SSL Certificate Verification
- **Description**: Verify SSL certificate validity
- **Checks**:
  - Certificate validity period
  - Certificate authority
  - Certificate chain
  - Revocation status
- **Library**: pyOpenSSL

#### 4.2.4 Machine Learning Classification
- **Description**: Classify URL as phishing/legitimate
- **Algorithms**: Random Forest, XGBoost, LightGBM
- **Features**: 20+ URL features
- **Output**: Probability score (0-1)

#### 4.2.5 VirusTotal Integration
- **Description**: Cross-check with VirusTotal database
- **API**: VirusTotal API v3
- **Data**: Reputation score, detection ratio
- **Enhancement**: Combine with ML prediction

#### 4.2.6 Phishing Report Generation
- **Description**: Generate detailed phishing report
- **Contents**:
  - URL analysis
  - Feature breakdown
  - ML prediction
  - VirusTotal result
  - Risk level
  - Recommendations

### 4.3 Components

#### 4.3.1 Phishing Detector
```python
class PhishingDetector:
    def detect(self, url: str) -> str
    def analyze(self, url: str) -> PhishingReport
    def batch_detect(self, urls: List[str]) -> List[PhishingReport]
```

#### 4.3.2 URL Feature Extractor
```python
class URLFeatureExtractor:
    def extract_features(self, url: str) -> dict
    def get_url_length(self, url: str) -> int
    def count_dots(self, url: str) -> int
    def count_digits(self, url: str) -> int
    def count_special_chars(self, url: str) -> int
    def get_subdomain_count(self, url: str) -> int
    def has_https(self, url: str) -> bool
    def has_ip_address(self, url: str) -> bool
    def get_tld(self, url: str) -> str
```

#### 4.3.3 Domain Age Checker
```python
class DomainAgeChecker:
    def get_domain_age(self, domain: str) -> int
    def get_registration_date(self, domain: str) -> datetime
    def is_suspicious_age(self, age_days: int) -> bool
```

#### 4.3.4 SSL Verifier
```python
class SSLVerifier:
    def verify_ssl(self, url: str) -> SSLInfo
    def get_certificate(self, url: str) -> dict
    def is_valid_certificate(self, cert: dict) -> bool
    def check_revocation(self, url: str) -> bool
```

#### 4.3.5 Phishing ML Model
```python
class PhishingMLModel:
    def load_model(self) -> None
    def predict(self, features: dict) -> float
    def predict_proba(self, features: dict) -> dict
    def get_feature_importance(self) -> dict
```

#### 4.3.6 VirusTotal Checker
```python
class VirusTotalChecker:
    def scan_url(self, url: str) -> dict
    def get_url_report(self, url: str) -> dict
    def get_reputation_score(self, url: str) -> int
    def get_detection_ratio(self, url: str) -> dict
```

### 4.4 Data Flow

```
Phishing Detection Flow:
1. User submits URL for scanning
2. PhishingDetector receives URL
3. URLFeatureExtractor extracts features
4. DomainAgeChecker checks domain age
5. SSLVerifier verifies SSL certificate
6. PhishingMLModel predicts phishing probability
7. VirusTotalChecker cross-checks with VirusTotal
8. Results aggregated
9. Final score calculated (ML + VirusTotal)
10. PhishingReport generated
11. Report returned to user
12. Alert generated if phishing detected
```

### 4.5 API Endpoints

```
POST   /api/v1/scan/url
GET    /api/v1/scan/url/{scan_id}
POST   /api/v1/scan/url/batch
GET    /api/v1/phishing/stats
GET    /api/v1/phishing/history
```

### 4.6 Dependencies

- **Feature Extraction**: urllib, tldextract
- **Domain Age**: python-whois
- **SSL Verification**: pyOpenSSL, ssl
- **ML Model**: scikit-learn, joblib
- **VirusTotal**: requests, virustotal-api
- **Data Processing**: pandas, numpy

### 4.7 Implementation Details

**Feature Extraction Details**:
```python
features = {
    'url_length': len(url),
    'num_dots': url.count('.'),
    'num_digits': sum(c.isdigit() for c in url),
    'num_special_chars': sum(not c.isalnum() for c in url),
    'subdomain_count': len(domain.split('.')) - 2,
    'path_length': len(parsed_url.path),
    'query_params_count': len(parsed_url.query),
    'has_https': 1 if url.startswith('https') else 0,
    'has_ip': 1 if is_ip_address(domain) else 0,
    'tld': tld,
    'domain_age_days': domain_age,
    'ssl_valid': 1 if ssl_valid else 0
}
```

**Final Score Calculation**:
```python
ml_score = model.predict_proba(features)[1]  # Phishing probability
vt_score = virustotal_score / 100
final_score = (ml_score * 0.7) + (vt_score * 0.3)
```

**Risk Levels**:
- **Safe**: 0.0 - 0.3
- **Low Risk**: 0.3 - 0.5
- **Medium Risk**: 0.5 - 0.7
- **High Risk**: 0.7 - 0.9
- **Critical**: 0.9 - 1.0

---

## 5. MODULE 4: MALWARE DETECTION SYSTEM

### 5.1 Module Overview

**Purpose**: Detect malicious files and executables

**Responsibilities**:
- PE file feature extraction
- Entropy analysis
- API call pattern analysis
- YARA rule matching
- Process behavior monitoring
- Machine learning classification

### 5.2 Features

#### 5.2.1 PE File Feature Extraction
- **Description**: Extract features from Portable Executable files
- **Features**:
  - File size
  - Section counts
  - Import table entries
  - Export table entries
  - Resource counts
  - Header information
  - Compilation timestamp
  - Debug information

#### 5.2.2 Entropy Analysis
- **Description**: Calculate file entropy for packer detection
- **Method**: Shannon entropy calculation
- **Threshold**: > 7.0 = likely packed/obfuscated
- **Sections**: Analyze per-section entropy

#### 5.2.3 API Call Pattern Analysis
- **Description**: Analyze API calls made by executable
- **Suspicious APIs**:
  - CreateRemoteThread
  - WriteProcessMemory
  - VirtualAlloc
  - SetWindowsHookEx
  - InternetOpen
  - CryptEncrypt

#### 5.2.4 YARA Rule Matching
- **Description**: Apply YARA rules for signature-based detection
- **Rules**: Custom + community rules
- **Categories**: Ransomware, Trojan, Worm, Spyware
- **Library**: yara-python

#### 5.2.5 Process Behavior Monitoring
- **Description**: Monitor process behavior during execution
- **Behaviors**:
  - File creation/modification
  - Registry changes
  - Network connections
  - Process injection
  - Privilege escalation

#### 5.2.6 Machine Learning Classification
- **Description**: Classify file as malicious/benign
- **Algorithms**: Random Forest, XGBoost, Neural Network
- **Features**: 50+ PE and behavioral features
- **Output**: Malware probability (0-1)

### 5.3 Components

#### 5.3.1 Malware Detector
```python
class MalwareDetector:
    def detect(self, file_path: str) -> str
    def analyze(self, file_path: str) -> MalwareReport
    def scan_directory(self, directory: str) -> List[MalwareReport]
```

#### 5.3.2 PE Feature Extractor
```python
class PEFeatureExtractor:
    def extract_features(self, file_path: str) -> dict
    def get_file_hash(self, file_path: str) -> str
    def get_pe_header(self, file_path: str) -> dict
    def get_sections(self, file_path: str) -> List[Section]
    def get_imports(self, file_path: str) -> List[str]
    def get_exports(self, file_path: str) -> List[str]
```

#### 5.3.3 Entropy Analyzer
```python
class EntropyAnalyzer:
    def calculate_entropy(self, data: bytes) -> float
    def calculate_section_entropy(self, file_path: str) -> dict
    def is_packed(self, entropy: float) -> bool
    def get_entropy_distribution(self, data: bytes) -> List[float]
```

#### 5.3.4 API Call Analyzer
```python
class APICallAnalyzer:
    def monitor_api_calls(self, pid: int) -> List[APICall]
    def detect_suspicious_apis(self, api_calls: List[APICall]) -> bool
    def get_api_sequence(self, pid: int) -> List[str]
```

#### 5.3.5 YARA Scanner
```python
class YARAScanner:
    def load_rules(self, rule_path: str) -> None
    def scan_file(self, file_path: str) -> List[YARAMatch]
    def scan_memory(self, pid: int) -> List[YARAMatch]
    def update_rules(self) -> None
```

#### 5.3.6 Behavior Monitor
```python
class BehaviorMonitor:
    def start_monitoring(self, pid: int) -> None
    def stop_monitoring(self) -> None
    def get_behavior_report(self) -> BehaviorReport
    def detect_suspicious_behavior(self) -> bool
```

#### 5.3.7 Malware ML Model
```python
class MalwareMLModel:
    def load_model(self) -> None
    def predict(self, features: dict) -> float
    def predict_proba(self, features: dict) -> dict
    def get_feature_importance(self) -> dict
```

### 5.4 Data Flow

```
Malware Detection Flow:
1. User uploads file for scanning
2. MalwareDetector receives file
3. PEFeatureExtractor extracts PE features
4. EntropyAnalyzer calculates entropy
5. APICallAnalyzer monitors API calls (if executable)
6. YARAScanner applies YARA rules
7. BehaviorMonitor monitors process behavior
8. MalwareMLModel predicts malware probability
9. VirusTotalChecker cross-checks (optional)
10. Results aggregated
11. Final score calculated
12. MalwareReport generated
13. Report returned to user
14. File quarantined if malicious
```

### 5.5 API Endpoints

```
POST   /api/v1/scan/file
GET    /api/v1/scan/file/{scan_id}
POST   /api/v1/scan/directory
GET    /api/v1/malware/stats
GET    /api/v1/malware/history
POST   /api/v1/malware/quarantine
POST   /api/v1/malware/restore
```

### 5.6 Dependencies

- **PE Analysis**: pefile
- **Entropy**: numpy, scipy
- **YARA**: yara-python
- **API Monitoring**: apimonitor, frida
- **Behavior Monitoring**: psutil, watchdog
- **ML Model**: scikit-learn, tensorflow
- **File Hashing**: hashlib

### 5.7 Implementation Details

**PE Feature Extraction**:
```python
features = {
    'file_size': os.path.getsize(file_path),
    'md5': md5_hash,
    'sha256': sha256_hash,
    'num_sections': len(pe.sections),
    'num_imports': len(pe.imports),
    'num_exports': len(pe.exports),
    'has_debug': has_debug_info,
    'has_resources': has_resources,
    'entropy': overall_entropy,
    'max_section_entropy': max_section_entropy,
    'has_suspicious_section': has_suspicious_section,
    'compilation_timestamp': pe.FILE_HEADER.TimeDateStamp,
    'is_packed': is_packed
}
```

**Entropy Calculation**:
```python
def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = collections.Counter(data)
    entropy = 0.0
    for count in counts.values():
        p = count / len(data)
        entropy -= p * math.log2(p)
    return entropy
```

**YARA Rule Example**:
```yara
rule ransomware
{
    meta:
        description = "Generic ransomware detection"
    strings:
        $s1 = "encrypt" nocase
        $s2 = "decrypt" nocase
        $s3 = "bitcoin" nocase
        $s4 = "payment" nocase
    condition:
        2 of them
}
```

**Suspicious API Patterns**:
- Process injection APIs
- Registry modification APIs
- Network communication APIs
- File encryption APIs
- Privilege escalation APIs

---

## 6. MODULE 5: BEHAVIOR ANALYSIS ENGINE

### 6.1 Module Overview

**Purpose**: Detect anomalous user behavior patterns

**Responsibilities**:
- Login pattern analysis
- File access pattern monitoring
- Browser history analysis
- Network activity profiling
- Anomaly detection using ML
- Baseline establishment and updates

### 6.2 Features

#### 6.2.1 Login Pattern Analysis
- **Description**: Analyze user login patterns
- **Metrics**:
  - Typical login times
  - Login location
  - Device fingerprint
  - Login frequency
- **Anomalies**: Unusual time, location, device

#### 6.2.2 File Access Pattern Monitoring
- **Description**: Monitor file access patterns
- **Metrics**:
  - Frequently accessed files
  - File types accessed
  - Access frequency
  - Access duration
- **Anomalies**: Access to sensitive files, unusual file types

#### 6.2.3 Browser History Analysis
- **Description**: Analyze browsing patterns
- **Metrics**:
  - Frequently visited sites
  - Site categories
  - Browsing time distribution
  - Download patterns
- **Anomalies**: Visits to suspicious sites, unusual downloads

#### 6.2.4 Network Activity Profiling
- **Description**: Profile network activity patterns
- **Metrics**:
  - Data transfer volumes
  - Connection patterns
  - Protocol usage
  - Remote endpoints
- **Anomalies**: Unusual data transfers, connections to unknown endpoints

#### 6.2.5 Anomaly Detection
- **Description**: Detect anomalies using ML algorithms
- **Algorithms**:
  - Isolation Forest
  - One-Class SVM
  - Autoencoder
- **Output**: Anomaly score (0-1)

#### 6.2.6 Baseline Management
- **Description**: Establish and update user behavior baseline
- **Process**:
  - Collect behavior data for 30 days
  - Establish baseline patterns
  - Update baseline weekly
  - Adapt to normal behavior changes

### 6.3 Components

#### 6.3.1 Behavior Analyzer
```python
class BehaviorAnalyzer:
    def analyze(self, user_id: UUID) -> BehaviorReport
    def detect_anomaly(self, user_id: UUID, behavior_data: dict) -> bool
    def update_baseline(self, user_id: UUID) -> None
    def get_baseline(self, user_id: UUID) -> dict
```

#### 6.3.2 Login Pattern Analyzer
```python
class LoginPatternAnalyzer:
    def analyze_login_pattern(self, user_id: UUID) -> LoginPattern
    def detect_unusual_login(self, login_data: dict) -> bool
    def get_typical_login_times(self, user_id: UUID) -> List[datetime]
```

#### 6.3.3 File Access Analyzer
```python
class FileAccessAnalyzer:
    def analyze_file_access(self, user_id: UUID) -> FileAccessPattern
    def detect_unusual_access(self, file_access: dict) -> bool
    def get_frequently_accessed_files(self, user_id: UUID) -> List[str]
```

#### 6.3.4 Browser History Analyzer
```python
class BrowserHistoryAnalyzer:
    def analyze_browsing_pattern(self, user_id: UUID) -> BrowsingPattern
    def detect_suspicious_browsing(self, url: str) -> bool
    def get_frequently_visited_sites(self, user_id: UUID) -> List[str]
```

#### 6.3.5 Network Activity Analyzer
```python
class NetworkActivityAnalyzer:
    def analyze_network_pattern(self, user_id: UUID) -> NetworkPattern
    def detect_unusual_activity(self, network_data: dict) -> bool
    def get_typical_endpoints(self, user_id: UUID) -> List[str]
```

#### 6.3.6 Anomaly Detection Model
```python
class AnomalyDetectionModel:
    def train(self, normal_data: List[dict]) -> None
    def predict(self, behavior_data: dict) -> float
    def get_anomaly_score(self, behavior_data: dict) -> float
    def explain_anomaly(self, behavior_data: dict) -> dict
```

#### 6.3.7 Baseline Manager
```python
class BaselineManager:
    def establish_baseline(self, user_id: UUID) -> dict
    def update_baseline(self, user_id: UUID) -> dict
    def compare_to_baseline(self, user_id: UUID, current_data: dict) -> dict
    def get_baseline_drift(self, user_id: UUID) -> float
```

### 6.4 Data Flow

```
Behavior Analysis Flow:
1. Behavior data collected from monitoring
2. LoginPatternAnalyzer analyzes login patterns
3. FileAccessAnalyzer analyzes file access patterns
4. BrowserHistoryAnalyzer analyzes browsing patterns
5. NetworkActivityAnalyzer analyzes network patterns
6. Features extracted from all analyzers
7. AnomalyDetectionModel predicts anomaly score
8. BaselineManager compares to established baseline
9. Anomaly detected if score > threshold
10. Alert generated for anomalies
11. Baseline updated periodically
```

### 6.5 API Endpoints

```
GET    /api/v1/behavior/analysis
GET    /api/v1/behavior/baseline
PUT    /api/v1/behavior/baseline
GET    /api/v1/behavior/anomalies
GET    /api/v1/behavior/patterns
```

### 6.6 Dependencies

- **Data Processing**: pandas, numpy
- **ML Models**: scikit-learn, tensorflow
- **Anomaly Detection**: sklearn, pyod
- **Time Series**: statsmodels
- **Visualization**: matplotlib, seaborn

### 6.7 Implementation Details

**Feature Extraction for Anomaly Detection**:
```python
features = {
    'login_time_hour': login_time.hour,
    'login_day_of_week': login_time.weekday(),
    'login_location_changed': location_changed,
    'login_device_changed': device_changed,
    'file_access_count': len(file_accesses),
    'sensitive_file_accessed': accessed_sensitive_files,
    'unique_sites_visited': len(unique_sites),
    'suspicious_sites_visited': len(suspicious_sites),
    'data_transfer_mb': total_data_transfer,
    'unusual_endpoints': len(unusual_endpoints),
    'activity_duration_hours': activity_duration
}
```

**Isolation Forest Configuration**:
```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)
```

**One-Class SVM Configuration**:
```python
from sklearn.svm import OneClassSVM

model = OneClassSVM(
    kernel='rbf',
    gamma='scale',
    nu=0.1
)
```

**Autoencoder Architecture**:
```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(32, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(8, activation='relu'),  # Bottleneck
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(input_dim, activation='sigmoid')
])
```

**Baseline Establishment**:
- Collect data for 30 days
- Calculate statistical measures (mean, std, percentiles)
- Store baseline in database
- Update weekly with rolling window

**Anomaly Thresholds**:
- **Low Anomaly**: 0.5 - 0.7
- **Medium Anomaly**: 0.7 - 0.85
- **High Anomaly**: 0.85 - 0.95
- **Critical Anomaly**: 0.95 - 1.0

---

## 7. MODULE 6: THREAT DETECTION ENGINE

### 7.1 Module Overview

**Purpose**: Central threat detection and classification engine

**Responsibilities**:
- Collect system logs
- Extract features from logs
- Predict threats using ML models
- Generate threat scores
- Classify attack types
- Aggregate threat intelligence

### 7.2 Features

#### 7.2.1 System Log Collection
- **Description**: Collect logs from various sources
- **Sources**:
  - System event logs
  - Application logs
  - Security logs
  - Network logs
  - Monitoring data
- **Format**: Structured JSON

#### 7.2.2 Feature Extraction
- **Description**: Extract features from logs for ML models
- **Features**:
  - Temporal features (time of day, day of week)
  - Frequency features (event counts)
  - Sequence features (event patterns)
  - Contextual features (user, system state)
- **Method**: Feature engineering pipelines

#### 7.2.3 Threat Prediction
- **Description**: Predict threats using ensemble ML models
- **Models**:
  - Phishing detection model
  - Malware detection model
  - Behavior anomaly model
  - Network intrusion model
- **Method**: Ensemble voting

#### 7.2.4 Threat Score Generation
- **Description**: Generate comprehensive threat score
- **Components**:
  - ML prediction confidence
  - Severity classification
  - Risk factors
  - Historical context
- **Range**: 0-100

#### 7.2.5 Attack Type Classification
- **Description**: Classify attack type
- **Categories**:
  - Phishing
  - Malware
  - Ransomware
  - SQL Injection
  - XSS
  - DDoS
  - Insider Threat
  - Social Engineering

#### 7.2.6 Threat Intelligence Aggregation
- **Description**: Aggregate threat intelligence from external sources
- **Sources**:
  - VirusTotal
  - MITRE ATT&CK
  - CVE database
  - Threat feeds
- **Purpose**: Enhance detection accuracy

### 7.3 Components

#### 7.3.1 Threat Detection Engine
```python
class ThreatDetectionEngine:
    def detect_threat(self, log_data: dict) -> Threat
    def analyze_logs(self, logs: List[dict]) -> List[Threat]
    def generate_threat_score(self, threat_data: dict) -> int
    def classify_attack_type(self, threat_data: dict) -> str
```

#### 7.3.2 Log Collector
```python
class LogCollector:
    def collect_system_logs(self) -> List[dict]
    def collect_application_logs(self) -> List[dict]
    def collect_security_logs(self) -> List[dict]
    def collect_network_logs(self) -> List[dict]
    def aggregate_logs(self) -> List[dict]
```

#### 7.3.3 Feature Extractor
```python
class LogFeatureExtractor:
    def extract_temporal_features(self, log: dict) -> dict
    def extract_frequency_features(self, logs: List[dict]) -> dict
    def extract_sequence_features(self, logs: List[dict]) -> dict
    def extract_contextual_features(self, log: dict) -> dict
```

#### 7.3.4 Threat Predictor
```python
class ThreatPredictor:
    def load_models(self) -> None
    def predict_threat(self, features: dict) -> dict
    def ensemble_prediction(self, predictions: List[dict]) -> dict
    def get_prediction_confidence(self) -> float
```

#### 7.3.5 Threat Scorer
```python
class ThreatScorer:
    def calculate_score(self, threat_data: dict) -> int
    def get_severity_level(self, score: int) -> str
    def get_risk_factors(self, threat_data: dict) -> List[str]
```

#### 7.3.6 Attack Classifier
```python
class AttackClassifier:
    def classify(self, threat_data: dict) -> str
    def get_attack_description(self, attack_type: str) -> str
    def get_mitigation_steps(self, attack_type: str) -> List[str]
```

#### 7.3.7 Threat Intelligence Aggregator
```python
class ThreatIntelligenceAggregator:
    def get_virustotal_data(self, indicator: str) -> dict
    def get_mitre_attack_data(self, technique_id: str) -> dict
    def get_cve_data(self, cve_id: str) -> dict
    def aggregate_intelligence(self, threat_data: dict) -> dict
```

### 7.4 Data Flow

```
Threat Detection Flow:
1. LogCollector collects logs from various sources
2. Logs aggregated and normalized
3. LogFeatureExtractor extracts features
4. Features passed to ThreatPredictor
5. ThreatPredictor runs ensemble of ML models
6. Predictions aggregated
7. ThreatScorer calculates threat score
8. AttackClassifier classifies attack type
9. ThreatIntelligenceAggregator enriches with external data
10. Final threat object created
11. Threat stored in database
12. Alert generated if score > threshold
```

### 7.5 API Endpoints

```
POST   /api/v1/threats/detect
GET    /api/v1/threats
GET    /api/v1/threats/{threat_id}
PUT    /api/v1/threats/{threat_id}/status
GET    /api/v1/threats/stats
GET    /api/v1/threats/trends
GET    /api/v1/threats/intelligence
```

### 7.6 Dependencies

- **Log Processing**: logparser, python-json-logger
- **Feature Engineering**: sklearn, pandas
- **ML Models**: sklearn, xgboost, tensorflow
- **Threat Intelligence**: virustotal-api, mitreattack
- **Data Storage**: PostgreSQL, Redis

### 7.7 Implementation Details

**Log Collection Sources**:
```python
log_sources = {
    'system': '/var/log/syslog',
    'security': '/var/log/auth.log',
    'application': '/var/log/app.log',
    'network': '/var/log/network.log',
    'monitoring': 'monitoring_data_table'
}
```

**Feature Extraction**:
```python
features = {
    'timestamp_hour': log['timestamp'].hour,
    'timestamp_day': log['timestamp'].weekday(),
    'event_type': event_type_encoded,
    'user_id': user_id_encoded,
    'source_ip': source_ip_encoded,
    'destination_ip': dest_ip_encoded,
    'port_number': port_number,
    'protocol': protocol_encoded,
    'event_count_last_hour': event_count,
    'unique_sources_last_hour': unique_sources,
    'sequence_pattern': sequence_encoded
}
```

**Ensemble Prediction**:
```python
predictions = {
    'phishing_model': phishing_model.predict(features),
    'malware_model': malware_model.predict(features),
    'behavior_model': behavior_model.predict(features),
    'network_model': network_model.predict(features)
}

final_prediction = weighted_average(predictions, weights)
```

**Threat Score Calculation**:
```python
score = (
    ml_confidence * 0.4 +
    severity_weight * 0.3 +
    risk_factor_count * 0.2 +
    historical_frequency * 0.1
)
```

**Attack Type Classification**:
```python
attack_types = {
    'phishing': ['url_submission', 'email_link'],
    'malware': ['file_execution', 'process_injection'],
    'ransomware': ['file_encryption', 'ransom_note'],
    'sql_injection': ['sql_pattern', 'db_error'],
    'xss': ['script_injection', 'xss_pattern'],
    'ddos': ['high_request_rate', 'packet_flood'],
    'insider': ['unusual_access', 'data_exfiltration'],
    'social_engineering': ['phishing_email', 'impersonation']
}
```

---

## 8. MODULE 7: REAL-TIME ALERT SYSTEM

### 8.1 Module Overview

**Purpose**: Generate and manage real-time alerts for detected threats

**Responsibilities**:
- Alert generation based on threat detection
- Severity classification
- Multi-channel notification delivery
- Alert acknowledgment and dismissal
- Alert history and analytics
- User notification preferences

### 8.2 Features

#### 8.2.1 Alert Generation
- **Description**: Generate alerts when threats are detected
- **Triggers**:
  - Threat score > threshold
  - Anomaly detected
  - Suspicious activity
  - Policy violation
- **Content**: Threat details, severity, recommendations

#### 8.2.2 Severity Classification
- **Description**: Classify alert severity
- **Levels**:
  - **Low**: Informational, minimal risk
  - **Medium**: Requires attention, moderate risk
  - **High**: Immediate action required, high risk
  - **Critical**: Emergency, critical risk

#### 8.2.3 Desktop Notifications
- **Description**: Display desktop notifications
- **Features**:
  - Toast notifications
  - Sound alerts
  - Persistent notifications
  - Action buttons
- **Platform**: Windows, macOS, Linux

#### 8.2.4 Email Alerts
- **Description**: Send email notifications
- **Triggers**: High and Critical severity
- **Content**: Alert details, threat information, recommendations
- **Service**: SendGrid/SMTP

#### 8.2.5 Dashboard Alerts
- **Description**: Display alerts on dashboard
- **Features**:
  - Real-time alert feed
  - Alert filtering
  - Alert details panel
  - Alert history
- **Update**: WebSocket real-time updates

#### 8.2.6 Alert Acknowledgment
- **Description**: Allow users to acknowledge alerts
- **Purpose**: Track alert awareness
- **Metadata**: Acknowledgment time, user, notes

#### 8.2.7 Alert Dismissal
- **Description**: Allow users to dismiss alerts
- **Purpose**: Clear resolved alerts
- **Metadata**: Dismissal time, user, reason

### 8.3 Components

#### 8.3.1 Alert Manager
```python
class AlertManager:
    def generate_alert(self, threat: Threat) -> Alert
    def send_alert(self, alert: Alert) -> bool
    def acknowledge_alert(self, alert_id: UUID, user_id: UUID) -> bool
    def dismiss_alert(self, alert_id: UUID, user_id: UUID) -> bool
    def get_user_alerts(self, user_id: UUID) -> List[Alert]
```

#### 8.3.2 Severity Classifier
```python
class SeverityClassifier:
    def classify(self, threat_data: dict) -> str
    def get_severity_thresholds(self) -> dict
    def update_thresholds(self, thresholds: dict) -> None
```

#### 8.3.3 Desktop Notifier
```python
class DesktopNotifier:
    def show_notification(self, alert: Alert) -> bool
    def play_sound(self, severity: str) -> None
    def show_persistent_alert(self, alert: Alert) -> bool
```

#### 8.3.4 Email Sender
```python
class EmailSender:
    def send_alert_email(self, alert: Alert, recipient: str) -> bool
    def send_summary_email(self, user_id: UUID) -> bool
    def format_alert_email(self, alert: Alert) -> str
```

#### 8.3.5 WebSocket Broadcaster
```python
class WebSocketBroadcaster:
    def broadcast_alert(self, alert: Alert) -> None
    def broadcast_to_user(self, user_id: UUID, alert: Alert) -> None
    def subscribe_to_alerts(self, user_id: UUID) -> None
    def unsubscribe_from_alerts(self, user_id: UUID) -> None
```

#### 8.3.6 Alert History Manager
```python
class AlertHistoryManager:
    def get_alert_history(self, user_id: UUID, days: int) -> List[Alert]
    def get_alert_stats(self, user_id: UUID) -> dict
    def get_alert_trends(self, user_id: UUID) -> dict
```

#### 8.3.7 Notification Preferences Manager
```python
class NotificationPreferencesManager:
    def get_preferences(self, user_id: UUID) -> dict
    def update_preferences(self, user_id: UUID, prefs: dict) -> bool
    def should_notify(self, user_id: UUID, severity: str) -> bool
```

### 8.4 Data Flow

```
Alert Generation Flow:
1. Threat detected by Threat Detection Engine
2. AlertManager receives threat
3. SeverityClassifier classifies severity
4. Alert object created
5. Alert stored in database
6. WebSocketBroadcaster sends to dashboard
7. DesktopNotifier shows desktop notification
8. If severity >= High, EmailSender sends email
9. User acknowledges/dismisses alert
10. Alert status updated
11. Alert history updated
```

### 8.5 API Endpoints

```
GET    /api/v1/alerts
GET    /api/v1/alerts/{alert_id}
PUT    /api/v1/alerts/{alert_id}/acknowledge
PUT    /api/v1/alerts/{alert_id}/dismiss
GET    /api/v1/alerts/unread
GET    /api/v1/alerts/history
GET    /api/v1/alerts/stats
PUT    /api/v1/alerts/preferences
```

### 8.6 Dependencies

- **Desktop Notifications**: plyer, notify2
- **Email**: sendgrid, smtplib
- **WebSocket**: socketio
- **Task Queue**: celery
- **Database**: PostgreSQL

### 8.7 Implementation Details

**Severity Classification Rules**:
```python
def classify_severity(threat_data):
    score = threat_data['threat_score']
    attack_type = threat_data['attack_type']
    
    if score >= 90 or attack_type in ['ransomware', 'critical']:
        return 'critical'
    elif score >= 70 or attack_type in ['malware', 'ddos']:
        return 'high'
    elif score >= 50 or attack_type in ['phishing', 'xss']:
        return 'medium'
    else:
        return 'low'
```

**Desktop Notification Format**:
```python
notification = {
    'title': f'{severity} Alert: {threat_type}',
    'message': alert_message,
    'icon': 'warning_icon.png',
    'sound': f'{severity}_alert.mp3',
    'actions': ['View Details', 'Dismiss'],
    'persistent': severity in ['high', 'critical']
}
```

**Email Template**:
```html
<h2>{{ severity }} Security Alert</h2>
<p><strong>Threat Type:</strong> {{ threat_type }}</p>
<p><strong>Threat Score:</strong> {{ threat_score }}/100</p>
<p><strong>Description:</strong> {{ description }}</p>
<p><strong>Detected At:</strong> {{ timestamp }}</p>
<p><strong>Recommendations:</strong></p>
<ul>
  {% for rec in recommendations %}
    <li>{{ rec }}</li>
  {% endfor %}
</ul>
<p><a href="{{ dashboard_url }}">View in Dashboard</a></p>
```

**WebSocket Event Format**:
```javascript
{
  "event": "new_alert",
  "data": {
    "alert_id": "uuid",
    "severity": "high",
    "title": "Malware Detected",
    "message": "Suspicious file detected",
    "timestamp": "2026-07-14T10:30:00Z"
  }
}
```

**Notification Preferences**:
```python
preferences = {
    'desktop_notifications': {
        'enabled': True,
        'low': False,
        'medium': True,
        'high': True,
        'critical': True
    },
    'email_notifications': {
        'enabled': True,
        'low': False,
        'medium': False,
        'high': True,
        'critical': True
    },
    'sound_enabled': True,
    'quiet_hours': {
        'enabled': False,
        'start': '22:00',
        'end': '08:00'
    }
}
```

---

## 9. MODULE 8: THREAT INTELLIGENCE DASHBOARD

### 9.1 Module Overview

**Purpose**: Provide comprehensive dashboard for threat visualization and management

**Responsibilities**:
- Display current threats
- Show historical attack data
- Visualize threat trends
- Calculate and display security score
- Show risk level
- Provide security recommendations

### 9.2 Features

#### 9.2.1 Current Threats Display
- **Description**: Display currently active threats
- **Information**:
  - Threat type
  - Severity
  - Detection time
  - Status
  - Quick actions
- **Update**: Real-time via WebSocket

#### 9.2.2 Historical Attack Data
- **Description**: Show historical threat data
- **Views**:
  - Timeline view
  - Calendar view
  - List view
- **Filters**: Date range, threat type, severity

#### 9.2.3 Threat Trends Visualization
- **Description**: Visualize threat trends over time
- **Charts**:
  - Line chart: Threats over time
  - Bar chart: Threats by type
  - Pie chart: Threats by severity
  - Heatmap: Threats by time of day
- **Period**: Hourly, daily, weekly, monthly

#### 9.2.4 Security Score
- **Description**: Calculate and display overall security score
- **Range**: 0-100
- **Factors**:
  - Active threats count
  - Threat severity
  - System vulnerabilities
  - Security configuration
  - Historical performance

#### 9.2.5 Risk Level Display
- **Description**: Display current risk level
- **Levels**:
  - **Very Low**: 0-20
  - **Low**: 21-40
  - **Medium**: 41-60
  - **High**: 61-80
  - **Critical**: 81-100
- **Visual**: Color-coded indicator

#### 9.2.6 Security Recommendations
- **Description**: Provide actionable security recommendations
- **Categories**:
  - Immediate actions
  - Configuration improvements
  - Best practices
  - Training suggestions
- **Priority**: Based on risk level

### 9.3 Components

#### 9.3.1 Dashboard Service
```python
class DashboardService:
    def get_dashboard_data(self, user_id: UUID) -> DashboardData
    def get_current_threats(self, user_id: UUID) -> List[Threat]
    def get_historical_data(self, user_id: UUID, days: int) -> List[dict]
    def get_trends(self, user_id: UUID) -> dict
```

#### 9.3.2 Security Score Calculator
```python
class SecurityScoreCalculator:
    def calculate_score(self, user_id: UUID) -> int
    def get_score_breakdown(self, user_id: UUID) -> dict
    def get_score_history(self, user_id: UUID) -> List[dict]
```

#### 9.3.3 Risk Level Calculator
```python
class RiskLevelCalculator:
    def calculate_risk_level(self, user_id: UUID) -> str
    def get_risk_factors(self, user_id: UUID) -> List[str]
    def get_risk_trend(self, user_id: UUID) -> str
```

#### 9.3.4 Recommendation Engine
```python
class RecommendationEngine:
    def generate_recommendations(self, user_id: UUID) -> List[Recommendation]
    def prioritize_recommendations(self, recommendations: List[Recommendation]) -> List[Recommendation]
    def get_recommendation_history(self, user_id: UUID) -> List[dict]
```

#### 9.3.5 Chart Data Generator
```python
class ChartDataGenerator:
    def generate_trend_chart_data(self, user_id: UUID, period: str) -> dict
    def generate_type_chart_data(self, user_id: UUID) -> dict
    def generate_severity_chart_data(self, user_id: UUID) -> dict
    def generate_heatmap_data(self, user_id: UUID) -> dict
```

#### 9.3.6 Widget Manager
```python
class WidgetManager:
    def get_widgets(self, user_id: UUID) -> List[Widget]
    def update_widget(self, widget_id: UUID, config: dict) -> bool
    def add_widget(self, user_id: UUID, widget_type: str) -> Widget
    def remove_widget(self, widget_id: UUID) -> bool
```

### 9.4 Data Flow

```
Dashboard Data Flow:
1. User requests dashboard
2. DashboardService aggregates data from multiple sources
3. SecurityScoreCalculator calculates security score
4. RiskLevelCalculator determines risk level
5. RecommendationEngine generates recommendations
6. ChartDataGenerator prepares visualization data
7. Widget Manager configures dashboard widgets
8. Data formatted for frontend
9. Data sent to frontend via API
10. Frontend renders dashboard
11. WebSocket updates for real-time changes
12. User interacts with dashboard
13. Actions sent to backend
14. Dashboard updated accordingly
```

### 9.5 API Endpoints

```
GET    /api/v1/dashboard
GET    /api/v1/dashboard/security-score
GET    /api/v1/dashboard/risk-level
GET    /api/v1/dashboard/threats
GET    /api/v1/dashboard/trends
GET    /api/v1/dashboard/recommendations
GET    /api/v1/dashboard/widgets
PUT    /api/v1/dashboard/widgets/{widget_id}
```

### 9.6 Dependencies

- **Frontend**: React, Recharts, Material-UI
- **Backend**: FastAPI, SQLAlchemy
- **Data Processing**: pandas, numpy
- **Real-time**: WebSocket, Redis
- **Caching**: Redis

### 9.7 Implementation Details

**Security Score Calculation**:
```python
def calculate_security_score(user_id):
    factors = {
        'active_threats': get_active_threats_score(user_id),
        'threat_severity': get_severity_score(user_id),
        'vulnerabilities': get_vulnerability_score(user_id),
        'configuration': get_configuration_score(user_id),
        'history': get_history_score(user_id)
    }
    
    weights = {
        'active_threats': 0.3,
        'threat_severity': 0.25,
        'vulnerabilities': 0.2,
        'configuration': 0.15,
        'history': 0.1
    }
    
    total_score = sum(factors[k] * weights[k] for k in factors)
    return int(total_score)
```

**Dashboard Widgets**:
```python
widgets = [
    {
        'id': 'security-score',
        'type': 'gauge',
        'title': 'Security Score',
        'position': {'x': 0, 'y': 0, 'w': 3, 'h': 2}
    },
    {
        'id': 'threat-count',
        'type': 'stat-card',
        'title': 'Active Threats',
        'position': {'x': 3, 'y': 0, 'w': 3, 'h': 2}
    },
    {
        'id': 'threat-trends',
        'type': 'line-chart',
        'title': 'Threat Trends',
        'position': {'x': 0, 'y': 2, 'w': 6, 'h': 3}
    },
    {
        'id': 'threat-types',
        'type': 'pie-chart',
        'title': 'Threats by Type',
        'position': {'x': 6, 'y': 0, 'w': 3, 'h': 2}
    },
    {
        'id': 'recent-alerts',
        'type': 'list',
        'title': 'Recent Alerts',
        'position': {'x': 6, 'y': 2, 'w': 3, 'h': 3}
    }
]
```

**Chart Data Format**:
```javascript
{
  "type": "line",
  "data": {
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "datasets": [{
      "label": "Threats",
      "data": [12, 19, 3, 5, 2, 3, 10],
      "borderColor": "rgb(255, 99, 132)",
      "backgroundColor": "rgba(255, 99, 132, 0.2)"
    }]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "Threats Over Time"
      }
    }
  }
}
```

**Recommendation Generation**:
```python
recommendations = [
    {
        'id': 1,
        'priority': 'high',
        'category': 'immediate',
        'title': 'Update Antivirus Definitions',
        'description': 'Your antivirus definitions are 7 days old',
        'action': 'Update now',
        'estimated_time': '5 minutes'
    },
    {
        'id': 2,
        'priority': 'medium',
        'category': 'configuration',
        'title': 'Enable Two-Factor Authentication',
        'description': '2FA adds an extra layer of security',
        'action': 'Configure 2FA',
        'estimated_time': '10 minutes'
    }
]
```

**Real-time Updates**:
```javascript
// WebSocket connection
socket.on('dashboard_update', (data) => {
  updateDashboard(data);
});

socket.on('new_threat', (threat) => {
  addThreatToDashboard(threat);
});

socket.on('security_score_update', (score) => {
  updateSecurityScore(score);
});
```

---

## 10. MODULE INTEGRATION

### 10.1 Inter-Module Communication

```
Module Communication Flow:

Authentication Module → All Modules
  - Provides user authentication
  - Validates session tokens
  - Returns user context

Monitoring Module → Threat Detection Module
  - Sends monitoring data
  - Provides system state

Phishing Detection Module → Threat Detection Module
  - Sends phishing analysis results
  - Provides threat scores

Malware Detection Module → Threat Detection Module
  - Sends malware analysis results
  - Provides threat scores

Behavior Analysis Module → Threat Detection Module
  - Sends anomaly detection results
  - Provides behavior scores

Threat Detection Module → Alert Module
  - Sends detected threats
  - Triggers alert generation

Alert Module → Dashboard Module
  - Sends alert notifications
  - Provides alert history

All Modules → Database
  - Store module-specific data
  - Retrieve historical data
```

### 10.2 Shared Components

**Shared Models**:
- User model (used by all modules)
- Threat model (used by detection modules)
- Alert model (used by alert and dashboard modules)

**Shared Utilities**:
- Logger (used by all modules)
- Configuration manager (used by all modules)
- Database connection (used by all modules)
- Cache client (used by all modules)

**Shared Services**:
- Authentication service (used by all modules)
- Notification service (used by alert and dashboard modules)
- WebSocket service (used by dashboard and alert modules)

### 10.3 Data Flow Between Modules

```
Complete Data Flow:

1. User authenticates (Authentication Module)
2. Desktop agent starts (Monitoring Module)
3. Monitoring data collected (Monitoring Module)
4. URL scanned (Phishing Detection Module)
5. File scanned (Malware Detection Module)
6. Behavior analyzed (Behavior Analysis Module)
7. All data sent to Threat Detection Engine
8. Threat Detection Engine analyzes data
9. Threat detected
10. Alert generated (Alert Module)
11. Alert sent to user (Alert Module)
12. Dashboard updated (Dashboard Module)
13. User views dashboard (Dashboard Module)
14. User takes action
15. Action recorded (Database)
```

---

## 11. MODULE DEPENDENCIES SUMMARY

### 11.1 Module Dependency Matrix

| Module | Auth | Monitor | Phishing | Malware | Behavior | Threat | Alert | Dashboard |
|--------|------|---------|----------|---------|----------|--------|-------|-----------|
| Auth    | -    |         |          |         |          |        |       | X         |
| Monitor | X    | -       |          |         |          | X      |       |           |
| Phishing| X    |         | -        |         |          | X      |       |           |
| Malware | X    |         |          | -       |          | X      |       |           |
| Behavior| X    | X       |          |         | -        | X      |       |           |
| Threat  | X    | X       | X        | X       | X        | -      | X     | X         |
| Alert   | X    |         |          |         |          | X      | -     | X         |
| Dashboard| X  |         |          |         |          | X      | X     | -         |

### 11.2 Technology Dependencies by Module

**Module 1: Authentication**
- PostgreSQL, Redis, bcrypt, python-jose

**Module 2: Monitoring**
- psutil, watchdog, scapy, HTTP client

**Module 3: Phishing Detection**
- urllib, tldextract, python-whois, pyOpenSSL, scikit-learn

**Module 4: Malware Detection**
- pefile, yara-python, scikit-learn, tensorflow

**Module 5: Behavior Analysis**
- pandas, numpy, scikit-learn, pyod

**Module 6: Threat Detection**
- logparser, sklearn, xgboost, virustotal-api

**Module 7: Alert System**
- plyer, sendgrid, socketio, celery

**Module 8: Dashboard**
- React, Recharts, Material-UI, WebSocket

---

## 12. CONCLUSION

This Module Design document provides a comprehensive breakdown of the AI-Powered Digital Bodyguard system into 8 core modules. Each module is designed with:

- **Clear Purpose**: Well-defined responsibilities
- **Detailed Features**: Comprehensive feature sets
- **Component Design**: Modular component architecture
- **Data Flow**: Clear data flow diagrams
- **API Endpoints**: RESTful API design
- **Dependencies**: Technology dependencies identified
- **Implementation Details**: Specific implementation guidance

**Next Steps:**
1. Review and approve this Module Design
2. Proceed to Phase 5: Data Collection
3. Begin data collection for ML models

---

## APPENDICES

### Appendix A: Module Priority Matrix

| Module | Priority | Complexity | Dependencies |
|--------|----------|------------|--------------|
| Authentication | High | Low | None |
| Monitoring | High | Medium | Authentication |
| Phishing Detection | High | Medium | Authentication |
| Malware Detection | High | High | Authentication |
| Behavior Analysis | Medium | High | Monitoring, Authentication |
| Threat Detection | Critical | High | All detection modules |
| Alert System | High | Medium | Threat Detection |
| Dashboard | High | Medium | Threat Detection, Alert |

### Appendix B: Module Development Order

**Phase 1: Foundation**
1. Module 1: Authentication
2. Module 2: Monitoring

**Phase 2: Detection**
3. Module 3: Phishing Detection
4. Module 4: Malware Detection
5. Module 5: Behavior Analysis

**Phase 3: Integration**
6. Module 6: Threat Detection
7. Module 7: Alert System
8. Module 8: Dashboard

### Appendix C: Module Testing Strategy

**Unit Testing**: Test each component independently
**Integration Testing**: Test module interactions
**End-to-End Testing**: Test complete workflows
**Performance Testing**: Test module performance under load
**Security Testing**: Test module security vulnerabilities
