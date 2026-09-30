# System Design Document
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 13, 2026  

---

## 1. HIGH-LEVEL ARCHITECTURE DIAGRAM

### 1.1 System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   Web Dashboard  │  │  Desktop Agent   │  │   Mobile App     │         │
│  │   (React.js)     │  │  (Python)        │  │   (React Native) │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│           │                     │                     │                    │
│           └─────────────────────┴─────────────────────┘                    │
│                                 │                                          │
│                         HTTPS/WebSocket                                     │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   Nginx Reverse  │  │   FastAPI REST   │  │   WebSocket      │         │
│  │      Proxy       │  │      API         │  │   Server         │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   JWT Auth       │  │   Rate Limiter   │  │   Request        │         │
│  │   Middleware     │  │   Middleware     │  │   Logger         │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                             │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    AUTHENTICATION SERVICE                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Register │  │  Login   │  │  JWT     │  │ Session  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   MONITORING SERVICE                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Process  │  │ Network  │  │   File   │  │ Resource │            │   │
│  │  │ Monitor  │  │ Monitor  │  │ Monitor  │  │ Monitor  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   THREAT DETECTION SERVICES                          │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │  Phishing    │  │   Malware    │  │   Behavior   │             │   │
│  │  │  Detector    │  │   Detector   │  │   Analyzer   │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   ALERT MANAGEMENT SERVICE                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │ Alert    │  │ Email    │  │ Desktop  │  │ Severity │            │   │
│  │  │ Generator│  │ Sender   │  │ Notifier │  │ Classifier│            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MACHINE LEARNING LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    ML MODEL INFERENCE ENGINE                         │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │  Phishing    │  │   Malware    │  │   Behavior   │             │   │
│  │  │  Model (RF)  │  │  Model (XGB) │  │  Model (IF)  │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │  Feature     │  │   Model      │  │  Result      │             │   │
│  │  │  Extractor   │  │  Loader      │  │  Formatter   │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   PostgreSQL     │  │      Redis       │  │   File Storage   │         │
│  │   (Primary DB)   │  │    (Cache)       │  │   (Logs/Models)  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                             │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │   VirusTotal     │  │   Threat Intel   │  │   Email Service  │         │
│  │      API         │  │      Feeds       │  │   (SMTP/SendGrid)│         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Explanation

**Client Layer:**
- **Web Dashboard**: React-based interface for users to view threats, configure settings, and manage security
- **Desktop Agent**: Python service running in background for real-time system monitoring
- **Mobile App**: Optional mobile interface for on-the-go security monitoring

**API Gateway Layer:**
- **Nginx**: Reverse proxy for load balancing and SSL termination
- **FastAPI**: High-performance REST API framework
- **WebSocket**: Real-time bidirectional communication for live updates
- **JWT Auth**: Token-based authentication middleware
- **Rate Limiter**: Prevent API abuse
- **Request Logger**: Log all API requests for audit trails

**Business Logic Layer:**
- **Authentication Service**: User registration, login, session management
- **Monitoring Service**: Process, network, file, and resource monitoring
- **Threat Detection Services**: Phishing, malware, and behavior analysis
- **Alert Management**: Alert generation, email sending, desktop notifications

**Machine Learning Layer:**
- **ML Model Inference Engine**: Load and run trained models
- **Feature Extractor**: Extract features from raw data
- **Model Loader**: Load serialized models from disk
- **Result Formatter**: Format ML predictions for API responses

**Data Layer:**
- **PostgreSQL**: Primary relational database for structured data
- **Redis**: In-memory cache for frequently accessed data and session storage
- **File Storage**: Storage for logs, ML models, and uploaded files

**External Services Layer:**
- **VirusTotal API**: Third-party malware scanning
- **Threat Intel Feeds**: External threat intelligence data
- **Email Service**: Email delivery for alerts

---

## 2. DATA FLOW DIAGRAMS (DFD)

### 2.1 DFD Level 0 (Context Diagram)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER                                           │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    │ 1. Login/Register        │
                    │ 2. View Dashboard        │
                    │ 3. Scan URL/File         │
                    │ 4. Configure Settings    │
                    │ 5. Receive Alerts        │
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI-POWERED DIGITAL BODYGUARD                              │
│                                                                             │
│                    0.0: Main System Process                                 │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │              CYBER THREAT DETECTION & PREVENTION SYSTEM             │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    │ 1. Monitoring Data        │
                    │ 2. Threat Alerts         │
                    │ 3. Security Reports      │
                    │ 4. System Status         │
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   EXTERNAL SERVICES      │    │   SYSTEM RESOURCES      │
│                          │    │                          │
│ - VirusTotal API         │    │ - Processes              │
│ - Threat Intel Feeds     │    │ - Network Connections    │
│ - Email Service          │    │ - File System            │
│                          │    │ - Browser Activities     │
└──────────────────────────┘    └──────────────────────────┘
```

**Explanation:**
- **User**: Interacts with the system through web dashboard or desktop agent
- **Main System Process**: Core system that processes user requests and monitors system resources
- **External Services**: Third-party APIs for enhanced detection capabilities
- **System Resources**: Local system resources being monitored

### 2.2 DFD Level 1

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER                                           │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │ 1. Authentication Request │
                    │ 2. Monitoring Data        │
                    │ 3. Scan Request           │
                    │ 4. Dashboard Request      │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           1.0 AUTHENTICATION SERVICE                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Validate Credentials                                               │   │
│  │  - Generate JWT Token                                                 │   │
│  │  - Manage Sessions                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           2.0 MONITORING SERVICE                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Process Monitor                                                    │   │
│  │  - Network Monitor                                                     │   │
│  │  - File Monitor                                                        │   │
│  │  - Resource Monitor                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         3.0 THREAT DETECTION ENGINE                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Phishing Detector                                                  │   │
│  │  - Malware Detector                                                   │   │
│  │  - Behavior Analyzer                                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          4.0 ALERT MANAGER                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Generate Alerts                                                    │   │
│  │  - Classify Severity                                                   │   │
│  │  - Send Notifications                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          5.0 DASHBOARD SERVICE                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Display Security Score                                             │   │
│  │  - Show Threat History                                                 │   │
│  │  - Visualize Trends                                                    │   │
│  │  - Provide Recommendations                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           6.0 DATABASE MANAGER                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Store User Data                                                    │   │
│  │  - Store Threat Logs                                                   │   │
│  │  - Store Alerts                                                        │   │
│  │  - Store Monitoring Data                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         7.0 ML INFERENCE ENGINE                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Load Models                                                        │   │
│  │  - Extract Features                                                   │   │
│  │  - Run Predictions                                                     │   │
│  │  - Return Results                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Explanation:**
- **1.0 Authentication Service**: Handles user authentication and session management
- **2.0 Monitoring Service**: Collects system monitoring data
- **3.0 Threat Detection Engine**: Analyzes data for threats using ML models
- **4.0 Alert Manager**: Generates and manages alerts based on threat detection
- **5.0 Dashboard Service**: Provides data for the user dashboard
- **6.0 Database Manager**: Manages all data persistence operations
- **7.0 ML Inference Engine**: Runs machine learning models for threat detection

### 2.3 DFD Level 2 (Phishing Detection Detail)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER                                           │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │  1. Submit URL for Scan   │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1 PHISHING DETECTOR                                  │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   3.1.1 URL Validator    │    │   3.1.2 Feature Extractor│
│                          │    │                          │
│ - Check URL Format       │    │ - URL Length             │
│ - Validate Protocol     │    │ - Number of Dots         │
│ - Check Domain           │    │ - Number of Digits       │
│                          │    │ - Special Characters     │
└──────────────────────────┘    │ - HTTPS Usage            │
                    │           │ - Subdomain Count        │
                    └───────────┴──────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1.3 SSL VERIFIER                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Check SSL Certificate Validity                                     │   │
│  │  - Verify Certificate Authority                                       │   │
│  │  - Check Certificate Expiration                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1.4 DOMAIN AGE CHECKER                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Query WHOIS Database                                               │   │
│  │  - Calculate Domain Age                                               │   │
│  │  - Flag Suspicious New Domains                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1.5 ML CLASSIFIER                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Load Phishing Detection Model                                      │   │
│  │  - Run Prediction on Features                                         │   │
│  │  - Generate Probability Score                               │   │
│  │  - Classify as Phishing/Legitimate                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1.6 VIRUS TOTAL CHECKER                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Query VirusTotal API                                               │   │
│  │  - Get VirusTotal Reputation Score                                    │   │
│  │  - Check Against Known Malicious URLs                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3.1.7 RESULT AGGREGATOR                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  - Combine ML Prediction with VirusTotal Result                       │   │
│  │  - Calculate Final Threat Score                                       │   │
│  │  - Generate Detailed Report                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼─────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER                                           │
│                    ┌─────────────┴─────────────┐                            │
│                    │  2. Receive Scan Result  │                            │
│                    └───────────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Explanation:**
- **3.1.1 URL Validator**: Validates URL format and structure
- **3.1.2 Feature Extractor**: Extracts numerical features from URL for ML model
- **3.1.3 SSL Verifier**: Checks SSL certificate validity
- **3.1.4 Domain Age Checker**: Determines domain age using WHOIS
- **3.1.5 ML Classifier**: Uses trained ML model to classify URL
- **3.1.6 VirusTotal Checker**: Cross-checks with VirusTotal database
- **3.1.7 Result Aggregator**: Combines all results into final threat assessment

---

## 3. USE CASE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ACTORS                                         │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │    USER      │  │   ADMIN      │  │   SYSTEM     │  │  EXTERNAL    │   │
│  │              │  │              │  │              │  │   SERVICES   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USE CASES                                         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        AUTHENTICATION                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-001     │  │   UC-002     │  │   UC-003     │             │   │
│  │  │   Register   │  │    Login     │  │   Logout    │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐                              │   │
│  │  │   UC-004     │  │   UC-005     │                              │   │
│  │  │ Reset Password│  │  Manage Profile│                            │   │
│  │  └──────────────┘  └──────────────┘                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      DASHBOARD MANAGEMENT                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-006     │  │   UC-007     │  │   UC-008     │             │   │
│  │  │View Dashboard│  │View Threat   │  │View Security│             │   │
│  │  │              │  │  History     │  │   Score     │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐                              │   │
│  │  │   UC-009     │  │   UC-010     │                              │   │
│  │  │View Threat   │  │View System   │                              │   │
│  │  │   Trends     │  │   Status     │                              │   │
│  │  └──────────────┘  └──────────────┘                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      THREAT SCANNING                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-011     │  │   UC-012     │  │   UC-013     │             │   │
│  │  │  Scan URL    │  │  Scan File   │  │  Scan Email  │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐                              │   │
│  │  │   UC-014     │  │   UC-015     │                              │   │
│  │  │View Scan     │  │Download Scan│                              │   │
│  │  │  Report      │  │   Report     │                              │   │
│  │  └──────────────┘  └──────────────┘                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      MONITORING CONTROL                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-016     │  │   UC-017     │  │   UC-018     │             │   │
│  │  │Start Monitor │  │ Stop Monitor │  │Configure    │             │   │
│  │  │              │  │              │  │  Monitor    │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐                              │   │
│  │  │   UC-019     │  │   UC-020     │                              │   │
│  │  │View Monitor  │  │View Process  │                              │   │
│  │  │  Logs        │  │  Activity    │                              │   │
│  │  └──────────────┘  └──────────────┘                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      ALERT MANAGEMENT                                │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-021     │  │   UC-022     │  │   UC-023     │             │   │
│  │  │View Alerts   │  │Configure     │  │Acknowledge  │             │   │
│  │  │              │  │Alert Settings│  │  Alert      │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐                                                │   │
│  │  │   UC-024     │                                                │   │
│  │  │Dismiss Alert │                                                │   │
│  │  └──────────────┘                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      SETTINGS & CONFIGURATION                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-025     │  │   UC-026     │  │   UC-027     │             │   │
│  │  │Manage Scan   │  │Configure    │  │Set Alert    │             │   │
│  │  │  Settings    │  │  Thresholds │  │ Preferences │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐                                                │   │
│  │  │   UC-028     │                                                │   │
│  │  │Export Data   │                                                │   │
│  │  └──────────────┘                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      ADMIN FUNCTIONS                                 │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │   │
│  │  │   UC-029     │  │   UC-030     │  │   UC-031     │             │   │
│  │  │Manage Users  │  │View System   │  │Configure    │             │   │
│  │  │              │  │   Logs       │  │  System     │             │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘             │   │
│  │  ┌──────────────┐  ┌──────────────┐                              │   │
│  │  │   UC-032     │  │   UC-033     │                              │   │
│  │  │Train ML      │  │Update Threat  │                              │   │
│  │  │  Models      │  │  Intelligence │                              │   │
│  │  └──────────────┘  └──────────────┘                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Use Case Descriptions

**UC-001: Register**
- **Actor**: User
- **Description**: New user creates account with email and password
- **Preconditions**: None
- **Postconditions**: User account created, authentication token generated

**UC-002: Login**
- **Actor**: User
- **Description**: Existing user authenticates with credentials
- **Preconditions**: User account exists
- **Postconditions**: JWT token issued, session established

**UC-011: Scan URL**
- **Actor**: User
- **Description**: User submits URL for phishing analysis
- **Preconditions**: User authenticated
- **Postconditions**: URL analyzed, threat score returned

**UC-012: Scan File**
- **Actor**: User
- **Description**: User uploads file for malware analysis
- **Preconditions**: User authenticated
- **Postconditions**: File analyzed, threat score returned

**UC-016: Start Monitor**
- **Actor**: User
- **Description**: User starts real-time system monitoring
- **Preconditions**: User authenticated, desktop agent installed
- **Postconditions**: Monitoring service activated

**UC-029: Manage Users**
- **Actor**: Admin
- **Description**: Admin manages user accounts
- **Preconditions**: Admin authenticated
- **Postconditions**: User accounts updated

---

## 4. CLASS DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLASS DIAGRAM                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┐
│         User                 │
├──────────────────────────────┤
│ - userId: UUID               │
│ - email: String              │
│ - passwordHash: String       │
│ - firstName: String          │
│ - lastName: String           │
│ - createdAt: DateTime        │
│ - lastLogin: DateTime        │
│ - role: UserRole             │
├──────────────────────────────┤
│ + register()                 │
│ + login()                    │
│ + logout()                   │
│ + updateProfile()            │
│ + changePassword()           │
└──────────────────────────────┘
              │
              │ 1
              │
              ▼
┌──────────────────────────────┐
│         Session              │
├──────────────────────────────┤
│ - sessionId: UUID            │
│ - userId: UUID               │
│ - token: String              │
│ - expiresAt: DateTime        │
│ - createdAt: DateTime        │
├──────────────────────────────┤
│ + validate()                 │
│ + refresh()                  │
│ + revoke()                   │
└──────────────────────────────┘

┌──────────────────────────────┐
│      MonitoringData          │
├──────────────────────────────┤
│ - monitoringId: UUID         │
│ - userId: UUID               │
│ - timestamp: DateTime        │
│ - cpuUsage: Float            │
│ - ramUsage: Float            │
│ - processCount: Integer      │
│ - networkConnections: Integer│
├──────────────────────────────┤
│ + collect()                  │
│ + save()                     │
│ + analyze()                  │
└──────────────────────────────┘

┌──────────────────────────────┐
│      ProcessMonitor          │
├──────────────────────────────┤
│ - processId: UUID            │
│ - processName: String        │
│ - pid: Integer               │
│ - cpuUsage: Float            │
│ - memoryUsage: Float         │
│ - startTime: DateTime        │
│ - status: ProcessStatus      │
├──────────────────────────────┤
│ + monitor()                  │
│ + killProcess()              │
│ + getDetails()               │
└──────────────────────────────┘

┌──────────────────────────────┐
│      NetworkMonitor          │
├──────────────────────────────┤
│ - connectionId: UUID         │
│ - localIP: String            │
│ - localPort: Integer         │
│ - remoteIP: String           │
│ - remotePort: Integer        │
│ - protocol: String           │
│ - status: ConnectionStatus   │
├──────────────────────────────┤
│ + monitor()                  │
│ + blockConnection()          │
│ + getDetails()               │
└──────────────────────────────┘

┌──────────────────────────────┐
│      Threat                 │
├──────────────────────────────┤
│ - threatId: UUID             │
│ - userId: UUID               │
│ - threatType: ThreatType     │
│ - severity: Severity         │
│ - description: String        │
│ - source: String             │
│ - timestamp: DateTime        │
│ - status: ThreatStatus       │
│ - threatScore: Float         │
├──────────────────────────────┤
│ + detect()                   │
│ + classify()                 │
│ + updateStatus()             │
└──────────────────────────────┘
              │
              │ 1
              │
              ▼
┌──────────────────────────────┐      ┌──────────────────────────────┐
│     PhishingThreat           │      │      MalwareThreat          │
├──────────────────────────────┤      ├──────────────────────────────┤
│ - url: String                │      │ - filePath: String           │
│ - domain: String             │      │ - fileName: String           │
│ - sslValid: Boolean          │      │ - fileSize: Long            │
│ - domainAge: Integer         │      │ - fileHash: String           │
│ - features: JSON             │      │ - entropy: Float             │
├──────────────────────────────┤      │ - yaraMatches: List<String>  │
│ + extractFeatures()          │      ├──────────────────────────────┤
│ + checkSSL()                 │      │ + extractPEFeatures()        │
│ + checkDomainAge()           │      │ + calculateEntropy()         │
│ + classify()                 │      │ + applyYARARules()           │
└──────────────────────────────┘      │ + classify()                 │
                                       └──────────────────────────────┘

┌──────────────────────────────┐
│      BehaviorThreat          │
├──────────────────────────────┤
│ - behaviorType: String       │
│ - anomalyScore: Float        │
│ - baseline: JSON             │
│ - currentPattern: JSON       │
├──────────────────────────────┤
│ + analyzePattern()           │
│ + detectAnomaly()            │
│ + updateBaseline()           │
└──────────────────────────────┘

┌──────────────────────────────┐
│         Alert                │
├──────────────────────────────┤
│ - alertId: UUID              │
│ - userId: UUID               │
│ - threatId: UUID             │
│ - severity: Severity         │
│ - message: String             │
│ - timestamp: DateTime        │
│ - acknowledged: Boolean       │
│ - dismissed: Boolean          │
├──────────────────────────────┤
│ + send()                     │
│ + acknowledge()               │
│ + dismiss()                  │
└──────────────────────────────┘

┌──────────────────────────────┐
│      ScanResult              │
├──────────────────────────────┤
│ - scanId: UUID               │
│ - userId: UUID               │
│ - scanType: ScanType         │
│ - target: String             │
│ - result: ScanResultType     │
│ - score: Float               │
│ - details: JSON              │
│ - timestamp: DateTime        │
├──────────────────────────────┤
│ + performScan()              │
│ + generateReport()           │
│ + export()                   │
└──────────────────────────────┘

┌──────────────────────────────┐
│      MLModel                 │
├──────────────────────────────┤
│ - modelId: UUID              │
│ - modelName: String          │
│ - modelType: ModelType       │
│ - version: String            │
│ - accuracy: Float            │
│ - trainedAt: DateTime        │
│ - modelPath: String          │
├──────────────────────────────┤
│ + load()                     │
│ + predict()                  │
│ + train()                    │
│ + evaluate()                 │
└──────────────────────────────┘
              │
              │ 1
              │
              ▼
┌──────────────────────────────┐      ┌──────────────────────────────┐
│    PhishingModel            │      │     MalwareModel            │
├──────────────────────────────┤      ├──────────────────────────────┤
│ - algorithm: String         │      │ - algorithm: String         │
│ - featureCount: Integer      │      │ - featureCount: Integer      │
├──────────────────────────────┤      ├──────────────────────────────┤
│ + extractURLFeatures()       │      │ + extractPEFeatures()        │
│ + predictPhishing()          │      │ + predictMalware()           │
└──────────────────────────────┘      └──────────────────────────────┘

┌──────────────────────────────┐
│    BehaviorModel            │
├──────────────────────────────┤
│ - algorithm: String         │
│ - featureCount: Integer      │
├──────────────────────────────┤
│ + extractBehaviorFeatures()  │
│ + detectAnomaly()            │
└──────────────────────────────┘

┌──────────────────────────────┐
│      DashboardData           │
├──────────────────────────────┤
│ - dashboardId: UUID          │
│ - userId: UUID               │
│ - securityScore: Integer      │
│ - threatCount: Integer       │
│ - activeAlerts: Integer      │
│ - lastUpdated: DateTime      │
├──────────────────────────────┤
│ + calculateSecurityScore()   │
│ + getThreatTrends()          │
│ + getRecommendations()       │
└──────────────────────────────┘
```

### Class Relationships

**Inheritance:**
- `PhishingThreat`, `MalwareThreat`, `BehaviorThreat` inherit from `Threat`
- `PhishingModel`, `MalwareModel`, `BehaviorModel` inherit from `MLModel`

**Association:**
- `User` has one or more `Session`
- `User` has many `MonitoringData`
- `User` has many `Threat`
- `User` has many `Alert`
- `User` has many `ScanResult`
- `Threat` has one `Alert`
- `MLModel` used by `Threat` detection

**Composition:**
- `MonitoringData` contains `ProcessMonitor` and `NetworkMonitor`

---

## 5. SEQUENCE DIAGRAM

### 5.1 URL Scanning Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         URL SCANNING SEQUENCE                               │
└─────────────────────────────────────────────────────────────────────────────┘

User          Web Dashboard    API Gateway    Phishing Detector    ML Model    VirusTotal
 │                 │                │                  │               │            │
 │──Scan URL──────>│                │                  │               │            │
 │                 │──POST /scan/url>│                  │               │            │
 │                 │                │──Validate URL───>│               │            │
 │                 │                │<──Valid──────────│               │            │
 │                 │                │──Extract Features>│               │            │
 │                 │                │<──Features───────│               │            │
 │                 │                │──Predict────────>│               │            │
 │                 │                │                  │──Inference──>│            │
 │                 │                │                  │<──Score──────│            │
 │                 │                │<──ML Result──────│               │            │
 │                 │                │──Check VirusTotal>│               │            │
 │                 │                │                  │──────────────>│            │
 │                 │                │                  │<──VT Result───│            │
 │                 │                │<──VT Result──────│               │            │
 │                 │                │──Aggregate Results──────────────────────────>│
 │                 │                │<──Final Result───────────────────────────────│
 │                 │<──Scan Result──│                  │               │            │
 │<──Display Result│                │                  │               │            │
 │                 │                │                  │               │            │
```

**Explanation:**
1. User submits URL through web dashboard
2. Dashboard sends POST request to API Gateway
3. API Gateway validates URL format
4. Phishing Detector extracts features from URL
5. ML Model performs inference on features
6. System cross-checks with VirusTotal API
7. Results are aggregated into final threat score
8. Result returned to user via dashboard

### 5.2 Real-Time Monitoring Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME MONITORING SEQUENCE                            │
└─────────────────────────────────────────────────────────────────────────────┘

Desktop Agent    Monitoring Service    Threat Engine    Alert Manager    User
      │                   │                  │               │           │
      │──Start Monitor───>│                  │               │           │
      │<──Started─────────│                  │               │           │
      │                   │                  │               │           │
      │──Process Data────>│                  │               │           │
      │                   │──Analyze────────>│               │           │
      │                   │<──Normal────────│               │           │
      │                   │                  │               │           │
      │──Network Data────>│                  │               │           │
      │                   │──Analyze────────>│               │           │
      │                   │<──Suspicious─────│               │           │
      │                   │                  │──Generate Alert>│           │
      │                   │                  │               │──Notify──>│
      │                   │                  │               │           │
      │──File Data────────>│                  │               │           │
      │                   │──Analyze────────>│               │           │
      │                   │<──Threat Detected│               │           │
      │                   │                  │──Generate Alert>│           │
      │                   │                  │               │──Notify──>│
      │                   │                  │               │           │
      │──Stop Monitor────>│                  │               │           │
      │<──Stopped─────────│                  │               │           │
```

**Explanation:**
1. Desktop Agent starts monitoring service
2. Agent continuously sends process, network, and file data
3. Monitoring Service analyzes data using Threat Engine
4. Threat Engine detects anomalies and generates alerts
5. Alert Manager notifies user of threats
6. User can stop monitoring at any time

---

## 6. ACTIVITY DIAGRAM

### 6.1 User Registration Activity

``┌─────────────────────────────────────────────────────────────────────────────┐
│                       USER REGISTRATION ACTIVITY                              │
└─────────────────────────────────────────────────────────────────────────────┘

                    [Start]
                       │
                       ▼
              ┌───────────────┐
              │ Enter Email   │
              │ & Password    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Validate Email │
              │ Format         │
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            │                   │
         [Valid]            [Invalid]
            │                   │
            ▼                   ▼
  ┌───────────────┐    ┌───────────────┐
  │ Validate      │    │ Show Error    │
  │ Password      │    │ Message       │
  │ Strength      │    └───────┬───────┘
  └───────┬───────┘            │
          │                    │
    ┌─────┴─────┐              │
    │           │              │
 [Strong]   [Weak]             │
    │           │              │
    ▼           ▼              │
┌─────────┐ ┌─────────┐       │
│ Check   │ │ Show    │       │
│ Email   │ │ Error   │       │
│ Exists  │ │ Message │       │
└────┬────┘ └────┬────┘       │
     │          │             │
  ┌──┴──┐   ┌───┴───┐         │
  │     │   │       │         │
[No] [Yes] │       │         │
  │     │   │       │         │
  ▼     ▼   │       │         │
┌─────┐ ┌─────┐ │       │         │
│Hash │ │Show │ │       │         │
│Pass │ │Error │ │       │         │
└──┬──┘ └──┬──┘ │       │         │
   │       │   │       │         │
   └───────┴───┴───────┴─────────┘
           │
           ▼
  ┌───────────────┐
  │ Create User   │
  │ in Database   │
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ Generate JWT  │
  │ Token         │
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │ Send Welcome  │
  │ Email         │
  └───────┬───────┘
          │
          ▼
         [End]
```

### 6.2 Threat Detection Activity

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      THREAT DETECTION ACTIVITY                              │
└─────────────────────────────────────────────────────────────────────────────┘

                    [Start]
                       │
                       ▼
              ┌───────────────┐
              │ Receive Data  │
              │ (URL/File)    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Validate Input│
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            │                   │
         [Valid]            [Invalid]
            │                   │
            ▼                   ▼
  ┌───────────────┐    ┌───────────────┐
  │ Extract       │    │ Return Error  │
  │ Features      │    └───────┬───────┘
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Load ML Model │            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Run Prediction│            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Get ML Score  │            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Check External│            │
  │ Services      │            │
  │ (VirusTotal)  │            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Aggregate     │            │
  │ Results       │            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
  ┌───────────────┐            │
  │ Calculate     │            │
  │ Final Score   │            │
  └───────┬───────┘            │
          │                    │
          ▼                    │
    ┌─────┴─────┐              │
    │           │              │
 [Threat]  [Safe]              │
    │           │              │
    ▼           ▼              │
┌─────────┐ ┌─────────┐       │
│Generate │ │ Return  │       │
│ Alert   │ │ Safe    │       │
└────┬────┘ │ Result   │       │
     │       └────┬────┘       │
     │            │            │
     └──────┬─────┴────────────┘
            │
            ▼
  ┌───────────────┐
  │ Save to DB    │
  └───────┬───────┘
          │
          ▼
         [End]
```

---

## 7. DATABASE DESIGN

### 7.1 Database Schema

```sql
-- Users Table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email)
);

-- Sessions Table
CREATE TABLE sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token)
);

-- Monitoring Data Table
CREATE TABLE monitoring_data (
    monitoring_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_usage FLOAT,
    ram_usage FLOAT,
    disk_usage FLOAT,
    process_count INTEGER,
    network_connections INTEGER,
    active_window VARCHAR(255),
    INDEX idx_user_id (user_id),
    INDEX idx_timestamp (timestamp)
);

-- Process Monitor Table
CREATE TABLE process_monitor (
    process_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    process_name VARCHAR(255) NOT NULL,
    pid INTEGER NOT NULL,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    start_time TIMESTAMP,
    status VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_process_name (process_name)
);

-- Network Monitor Table
CREATE TABLE network_monitor (
    connection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    local_ip VARCHAR(50),
    local_port INTEGER,
    remote_ip VARCHAR(50),
    remote_port INTEGER,
    protocol VARCHAR(10),
    status VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_remote_ip (remote_ip)
);

-- Threats Table
CREATE TABLE threats (
    threat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    threat_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description TEXT,
    source VARCHAR(255),
    threat_score FLOAT,
    status VARCHAR(50) DEFAULT 'active',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_threat_type (threat_type),
    INDEX idx_severity (severity),
    INDEX idx_timestamp (timestamp)
);

-- Phishing Threats Table
CREATE TABLE phishing_threats (
    phishing_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_id UUID NOT NULL REFERENCES threats(threat_id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    domain VARCHAR(255),
    ssl_valid BOOLEAN,
    domain_age INTEGER,
    features JSONB,
    ml_score FLOAT,
    virustotal_score FLOAT,
    final_score FLOAT
);

-- Malware Threats Table
CREATE TABLE malware_threats (
    malware_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_id UUID NOT NULL REFERENCES threats(threat_id) ON DELETE CASCADE,
    file_path TEXT,
    file_name VARCHAR(255),
    file_size BIGINT,
    file_hash VARCHAR(100),
    entropy FLOAT,
    yara_matches JSONB,
    ml_score FLOAT,
    virustotal_score FLOAT
);

-- Behavior Threats Table
CREATE TABLE behavior_threats (
    behavior_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_id UUID NOT NULL REFERENCES threats(threat_id) ON DELETE CASCADE,
    behavior_type VARCHAR(100),
    anomaly_score FLOAT,
    baseline JSONB,
    current_pattern JSONB,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts Table
CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    threat_id UUID REFERENCES threats(threat_id) ON DELETE SET NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    acknowledged BOOLEAN DEFAULT FALSE,
    dismissed BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    dismissed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_severity (severity),
    INDEX idx_acknowledged (acknowledged)
);

-- Scan Results Table
CREATE TABLE scan_results (
    scan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    scan_type VARCHAR(50) NOT NULL,
    target TEXT NOT NULL,
    result VARCHAR(50) NOT NULL,
    score FLOAT,
    details JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_scan_type (scan_type),
    INDEX idx_timestamp (timestamp)
);

-- ML Models Table
CREATE TABLE ml_models (
    model_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    algorithm VARCHAR(100),
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    trained_at TIMESTAMP,
    model_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_model_type (model_type),
    INDEX idx_is_active (is_active)
);

-- Dashboard Data Table
CREATE TABLE dashboard_data (
    dashboard_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    security_score INTEGER,
    threat_count INTEGER DEFAULT 0,
    active_alerts INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trends JSONB,
    recommendations JSONB,
    INDEX idx_user_id (user_id)
);

-- Settings Table
CREATE TABLE settings (
    setting_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, key),
    INDEX idx_user_id (user_id)
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    details JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_timestamp (timestamp)
);
```

### 7.2 Database Relationships

**Primary Keys:**
- All tables use UUID as primary key for distributed system compatibility

**Foreign Keys:**
- `sessions.user_id` → `users.user_id`
- `monitoring_data.user_id` → `users.user_id`
- `process_monitor.user_id` → `users.user_id`
- `network_monitor.user_id` → `users.user_id`
- `threats.user_id` → `users.user_id`
- `phishing_threats.threat_id` → `threats.threat_id`
- `malware_threats.threat_id` → `threats.threat_id`
- `behavior_threats.threat_id` → `threats.threat_id`
- `alerts.user_id` → `users.user_id`
- `alerts.threat_id` → `threats.threat_id`
- `scan_results.user_id` → `users.user_id`
- `dashboard_data.user_id` → `users.user_id`
- `settings.user_id` → `users.user_id`
- `audit_logs.user_id` → `users.user_id`

**Indexes:**
- Foreign key columns indexed for join performance
- Timestamp columns indexed for time-based queries
- Status/severity columns indexed for filtering

---

## 8. ER DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIP DIAGRAM                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     USERS        │
├──────────────────┤
│ PK user_id       │
│    email         │
│    password_hash │
│    first_name    │
│    last_name     │
│    role          │
│    created_at    │
│    last_login    │
└────────┬─────────┘
         │
         │ 1
         │
         │ N
    ┌────┴──────────────────────────────────────────────────────────────┐
    │                                                                   │
    │                                                                   │
┌───┴────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│SESSIONS│  │MONITORING    │  │   THREATS    │  │SCAN_RESULTS  │     │
├────────┤  │    DATA      │  ├──────────────┤  ├──────────────┤     │
│PK sess │  │PK mon_id     │  │PK threat_id │  │PK scan_id    │     │
│FK user │  │FK user_id    │  │FK user_id    │  │FK user_id    │     │
│    token│  │    timestamp │  │    type     │  │    type      │     │
│    exp  │  │    cpu_usage │  │    severity │  │    target    │     │
└────────┘  │    ram_usage  │  │    score    │  │    result    │     │
           └──────────────┘  └──────┬───────┘  └──────────────┘     │
                                   │ 1                               │
                                   │                                 │
                                   │ N                               │
                          ┌────────┴──────────────────────────────┐ │
                          │                                         │ │
                          │                                         │ │
                   ┌──────┴──────┐  ┌──────────────┐  ┌──────────┴──┴──┐
                   │PHISHING    │  │  MALWARE     │  │   BEHAVIOR     │
                   │THREATS     │  │  THREATS     │  │   THREATS      │
                   ├─────────────┤  ├──────────────┤  ├────────────────┤
                   │PK phish_id │  │PK malware_id │  │PK behavior_id  │
                   │FK threat_id│  │FK threat_id  │  │FK threat_id    │
                   │    url      │  │    file_path │  │    behavior    │
                   │    domain   │  │    file_hash │  │    anomaly     │
                   │    ssl      │  │    entropy   │  │    baseline    │
                   └─────────────┘  └──────────────┘  └────────────────┘
                                                                   │
                                                                   │
    ┌──────────────────────────────────────────────────────────────┘
    │
    │ N
    │
    │ 1
┌───┴────────┐
│   ALERTS   │
├────────────┤
│PK alert_id│
│FK user_id │
│FK threat_id│
│   severity│
│   message │
│   ack     │
│   dismiss │
└───────────┘

┌──────────────────┐
│ PROCESS_MONITOR  │
├──────────────────┤
│PK process_id     │
│FK user_id         │
│   process_name    │
│   pid             │
│   cpu_usage       │
│   memory_usage    │
└──────────────────┘

┌──────────────────┐
│ NETWORK_MONITOR  │
├──────────────────┤
│PK connection_id  │
│FK user_id         │
│   local_ip        │
│   remote_ip       │
│   protocol        │
│   status          │
└──────────────────┘

┌──────────────────┐
│   ML_MODELS      │
├──────────────────┤
│PK model_id        │
│   model_name      │
│   model_type      │
│   version         │
│   accuracy        │
│   model_path      │
└──────────────────┘

┌──────────────────┐
│ DASHBOARD_DATA   │
├──────────────────┤
│PK dashboard_id   │
│FK user_id         │
│   security_score │
│   threat_count   │
│   active_alerts  │
│   trends         │
└──────────────────┘

┌──────────────────┐
│    SETTINGS      │
├──────────────────┤
│PK setting_id     │
│FK user_id         │
│   key            │
│   value          │
└──────────────────┘

┌──────────────────┐
│   AUDIT_LOGS     │
├──────────────────┤
│PK log_id         │
│FK user_id         │
│   action         │
│   entity_type    │
│   details        │
│   timestamp      │
└──────────────────┘
```

### ER Diagram Explanation

**Entities:**
- **USERS**: Central entity representing system users
- **SESSIONS**: User authentication sessions
- **MONITORING_DATA**: System monitoring metrics
- **THREATS**: Detected threats (parent table)
- **PHISHING_THREATS**: Specific phishing threat details
- **MALWARE_THREATS**: Specific malware threat details
- **BEHAVIOR_THREATS**: Specific behavior threat details
- **ALERTS**: Generated alerts for threats
- **SCAN_RESULTS**: Results of URL/file scans
- **PROCESS_MONITOR**: Process monitoring data
- **NETWORK_MONITOR**: Network connection monitoring
- **ML_MODELS**: Machine learning model metadata
- **DASHBOARD_DATA**: Dashboard aggregation data
- **SETTINGS**: User configuration settings
- **AUDIT_LOGS**: System audit trail

**Relationships:**
- **One-to-Many**: User to Sessions, Monitoring Data, Threats, Alerts, Scan Results
- **One-to-One**: Threat to Phishing/Malware/Behavior Threats (inheritance)
- **Many-to-One**: Alerts to Threats

**Cardinality:**
- 1:N relationships marked with "1" and "N"
- PK = Primary Key
- FK = Foreign Key

---

## 9. API ARCHITECTURE

### 9.1 API Endpoint Design

#### Authentication Endpoints
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
```

#### User Management Endpoints
```
GET    /api/v1/users/profile
PUT    /api/v1/users/profile
DELETE /api/v1/users/account
```

#### Monitoring Endpoints
```
GET    /api/v1/monitoring/status
POST   /api/v1/monitoring/start
POST   /api/v1/monitoring/stop
GET    /api/v1/monitoring/processes
GET    /api/v1/monitoring/network
GET    /api/v1/monitoring/history
```

#### Scanning Endpoints
```
POST   /api/v1/scan/url
POST   /api/v1/scan/file
POST   /api/v1/scan/email
GET    /api/v1/scan/results/{scan_id}
GET    /api/v1/scan/history
```

#### Threat Endpoints
```
GET    /api/v1/threats
GET    /api/v1/threats/{threat_id}
PUT    /api/v1/threats/{threat_id}/status
GET    /api/v1/threats/stats
GET    /api/v1/threats/trends
```

#### Alert Endpoints
```
GET    /api/v1/alerts
GET    /api/v1/alerts/{alert_id}
PUT    /api/v1/alerts/{alert_id}/acknowledge
PUT    /api/v1/alerts/{alert_id}/dismiss
GET    /api/v1/alerts/unread
```

#### Dashboard Endpoints
```
GET    /api/v1/dashboard
GET    /api/v1/dashboard/security-score
GET    /api/v1/dashboard/threats
GET    /api/v1/dashboard/trends
GET    /api/v1/dashboard/recommendations
```

#### Settings Endpoints
```
GET    /api/v1/settings
PUT    /api/v1/settings
GET    /api/v1/settings/{key}
PUT    /api/v1/settings/{key}
```

#### Admin Endpoints
```
GET    /api/v1/admin/users
PUT    /api/v1/admin/users/{user_id}
DELETE /api/v1/admin/users/{user_id}
GET    /api/v1/admin/logs
GET    /api/v1/admin/system-status
POST   /api/v1/admin/models/train
GET    /api/v1/admin/models
```

### 9.2 API Request/Response Format

#### Standard Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2026-07-13T10:30:00Z"
}
```

#### Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {}
  },
  "timestamp": "2026-07-13T10:30:00Z"
}
```

### 9.3 Authentication Flow

```
1. User Registration:
   POST /api/v1/auth/register
   Body: { email, password, first_name, last_name }
   Response: { user_id, email, token }

2. User Login:
   POST /api/v1/auth/login
   Body: { email, password }
   Response: { token, refresh_token, expires_at }

3. Token Refresh:
   POST /api/v1/auth/refresh
   Headers: { Authorization: Bearer <refresh_token> }
   Response: { token, expires_at }

4. Authenticated Request:
   GET /api/v1/dashboard
   Headers: { Authorization: Bearer <token> }
```

### 9.4 WebSocket Events

#### Client → Server Events
```javascript
{
  "event": "subscribe",
  "data": {
    "channels": ["alerts", "monitoring"]
  }
}

{
  "event": "unsubscribe",
  "data": {
    "channels": ["alerts"]
  }
}
```

#### Server → Client Events
```javascript
{
  "event": "alert",
  "data": {
    "alert_id": "uuid",
    "severity": "high",
    "message": "Threat detected",
    "timestamp": "2026-07-13T10:30:00Z"
  }
}

{
  "event": "monitoring_update",
  "data": {
    "cpu_usage": 45.2,
    "ram_usage": 62.1,
    "process_count": 45,
    "timestamp": "2026-07-13T10:30:00Z"
  }
}
```

---

## 10. CONCLUSION

This System Design document provides a comprehensive blueprint for the AI-Powered Digital Bodyguard system. The design includes:

- **High-Level Architecture**: 6-layer architecture from client to external services
- **Data Flow Diagrams**: Context, Level 1, and Level 2 DFDs showing data movement
- **Use Case Diagram**: 33 use cases covering all system functionality
- **Class Diagram**: Object-oriented design with inheritance and relationships
- **Sequence Diagrams**: Interaction flows for URL scanning and real-time monitoring
- **Activity Diagrams**: Process flows for user registration and threat detection
- **Database Design**: Complete schema with 14 tables and relationships
- **ER Diagram**: Visual representation of entities and relationships
- **API Architecture**: RESTful API design with authentication, WebSocket support

**Next Steps:**
1. Review and approve this System Design
2. Proceed to Phase 3: Technology Stack
3. Begin implementation based on approved design

---

## APPENDICES

### Appendix A: Design Patterns Used

1. **Repository Pattern**: For data access layer
2. **Service Layer Pattern**: For business logic separation
3. **Factory Pattern**: For creating different threat detectors
4. **Observer Pattern**: For alert notifications
5. **Strategy Pattern**: For different ML algorithms
6. **Singleton Pattern**: For configuration management

### Appendix B: Security Considerations

1. **Authentication**: JWT-based stateless authentication
2. **Authorization**: Role-based access control (RBAC)
3. **Data Encryption**: AES-256 for sensitive data at rest
4. **Communication**: TLS 1.3 for all API communications
5. **Input Validation**: Comprehensive input sanitization
6. **Rate Limiting**: API rate limiting to prevent abuse
7. **Audit Logging**: Complete audit trail for compliance

### Appendix C: Scalability Considerations

1. **Horizontal Scaling**: Stateless API design enables horizontal scaling
2. **Database Sharding**: User data can be sharded by user_id
3. **Caching**: Redis caching for frequently accessed data
4. **Load Balancing**: Nginx load balancer for API distribution
5. **Asynchronous Processing**: Celery for background tasks
6. **CDN**: Static assets served via CDN
