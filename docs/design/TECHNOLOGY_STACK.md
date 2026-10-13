# Technology Stack Document
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. FRONTEND TECHNOLOGIES

### 1.1 React.js

**Version:** 18.3.1

**Why React.js?**
- **Component-Based Architecture**: Promotes code reusability and maintainability
- **Virtual DOM**: Provides excellent performance by minimizing DOM manipulations
- **Large Ecosystem**: Extensive library support for any functionality needed
- **Strong Community**: Active community with abundant resources and support
- **One-Way Data Flow**: Predictable data flow makes debugging easier
- **JSX Syntax**: Combines JavaScript and HTML for intuitive development
- **Hooks**: Modern state management without class components
- **Excellent for Dashboards**: Perfect for real-time data visualization

**Use Cases in Project:**
- Main dashboard interface
- Real-time threat monitoring display
- Interactive charts and graphs
- User authentication forms
- Settings and configuration panels
- Alert notification system

**Key Libraries:**
- **React Router v6**: Client-side routing
- **Axios**: HTTP client for API calls
- **Socket.io-client**: WebSocket for real-time updates
- **Chart.js / Recharts**: Data visualization
- **Material-UI / Bootstrap**: UI component library
- **React Query**: Data fetching and caching
- **Zustand / Redux**: State management

**Installation:**
```bash
npm install react react-dom
npm install react-router-dom axios socket.io-client
npm install recharts chart.js
npm install @mui/material @emotion/react @emotion/styled
```

### 1.2 HTML5

**Version:** HTML5

**Why HTML5?**
- **Standard Web Technology**: Universal compatibility across browsers
- **Semantic Elements**: Better SEO and accessibility
- **Native APIs**: Built-in support for geolocation, storage, etc.
- **Multimedia Support**: Native audio and video without plugins
- **Form Validation**: Built-in form validation features
- **Offline Support**: Application Cache for offline functionality

**Use Cases in Project:**
- Page structure and layout
- Form elements for user input
- Semantic markup for accessibility
- Meta tags for SEO and security
- Canvas for custom visualizations

### 1.3 CSS3

**Version:** CSS3

**Why CSS3?**
- **Styling Power**: Advanced styling capabilities
- **Animations**: Smooth transitions and animations
- **Responsive Design**: Media queries for mobile responsiveness
- **Flexbox & Grid**: Modern layout systems
- **Custom Properties**: CSS variables for theming
- **Performance**: Hardware-accelerated animations

**Use Cases in Project:**
- Styling all UI components
- Responsive layouts for different screen sizes
- Dark/light theme implementation
- Animations for alerts and notifications
- Custom scrollbars and UI elements

### 1.4 Bootstrap

**Version:** Bootstrap 5.3

**Why Bootstrap?**
- **Pre-built Components**: Ready-to-use UI components
- **Responsive Grid System**: Easy responsive layouts
- **Cross-Browser Compatibility**: Consistent appearance across browsers
- **Customizable**: Easy to customize with SASS
- **Documentation**: Excellent documentation and examples
- **Rapid Development**: Faster development with pre-built styles
- **Accessibility**: Built-in accessibility features

**Use Cases in Project:**
- Navigation bar and menus
- Cards for threat displays
- Tables for data presentation
- Forms for user input
- Modals for alerts and confirmations
- Buttons and interactive elements
- Grid layouts for dashboard widgets

**Installation:**
```bash
npm install bootstrap
```

**Import in React:**
```javascript
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
```

---

## 2. BACKEND TECHNOLOGIES

### 2.1 Python FastAPI

**Version:** FastAPI 0.104.1

**Why FastAPI?**
- **Modern & Fast**: Built on Starlette and Pydantic for high performance
- **Automatic API Documentation**: Auto-generated Swagger UI and ReDoc
- **Type Hints**: Python type hints for better code quality
- **Async Support**: Native async/await for concurrent operations
- **Validation**: Automatic request validation with Pydantic
- **Dependency Injection**: Built-in dependency injection system
- **WebSocket Support**: Native WebSocket support for real-time features
- **Easy Testing**: Built-in testing support with TestClient

**Performance Comparison:**
- FastAPI: ~500 requests/second (comparable to Node.js)
- Flask: ~200 requests/second
- Django: ~100 requests/second

**Use Cases in Project:**
- REST API endpoints
- WebSocket server for real-time updates
- Request validation and serialization
- Authentication middleware
- Background task management
- API documentation

**Key Features Used:**
- **Pydantic Models**: Request/response validation
- **OAuth2PasswordBearer**: JWT authentication
- **WebSocket**: Real-time alert broadcasting
- **BackgroundTasks**: Asynchronous task execution
- **CORS**: Cross-origin resource sharing
- **Middleware**: Request logging and error handling

**Installation:**
```bash
pip install fastapi uvicorn
pip install pydantic python-multipart
pip install python-jose[cryptography] passlib[bcrypt]
pip install python-multipart
```

**Basic Structure:**
```python
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Digital Bodyguard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Digital Bodyguard API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
```

### 2.2 Flask (Alternative)

**Version:** Flask 3.0.0

**Why Flask?**
- **Mature Framework**: Battle-tested with large community
- **Flexible**: Minimalist design allows custom architecture
- **Extensible**: Large ecosystem of extensions
- **Easy to Learn**: Simple and intuitive API
- **Production Ready**: Used by many large companies

**When to Use Flask:**
- If you prefer a more traditional framework
- If you need extensive Flask extensions
- If your team has Flask experience

**Installation:**
```bash
pip install flask flask-cors flask-jwt-extended
pip install flask-socketio
```

---

## 3. DATABASE TECHNOLOGIES

### 3.1 PostgreSQL

**Version:** PostgreSQL 15

**Why PostgreSQL?**
- **ACID Compliant**: Ensures data integrity
- **Advanced Features**: JSONB support, full-text search, geospatial data
- **Scalability**: Handles large datasets efficiently
- **Extensibility**: Custom functions and data types
- **Performance**: Excellent query optimization
- **Open Source**: Free and community-driven
- **JSONB Support**: Perfect for storing ML model features
- **Full-Text Search**: Built-in search capabilities
- **Replication**: Built-in replication for high availability

**Comparison with MongoDB:**
- **PostgreSQL**: Better for structured data, complex queries, transactions
- **MongoDB**: Better for unstructured data, flexible schema

**Use Cases in Project:**
- User authentication data
- Threat logs and history
- Monitoring data storage
- Alert management
- Scan results
- ML model metadata
- Audit logs

**Key Features Used:**
- **JSONB**: Store flexible data like ML features
- **Indexes**: Optimize query performance
- **Foreign Keys**: Maintain data integrity
- **Transactions**: Ensure data consistency
- **Triggers**: Automated data updates
- **Views**: Simplify complex queries

**Installation:**
```bash
# Windows: Download installer from postgresql.org
# Linux: sudo apt-get install postgresql postgresql-contrib
# macOS: brew install postgresql
```

**Python Driver:**
```bash
pip install psycopg2-binary sqlalchemy alembic
```

**Connection Example:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 3.2 MongoDB (Alternative)

**Version:** MongoDB 7.0

**Why MongoDB?**
- **Flexible Schema**: No rigid schema requirements
- **Document-Based**: Natural JSON document storage
- **Horizontal Scaling**: Easy sharding for large datasets
- **Rich Queries**: Powerful query language
- **Aggregation Framework**: Complex data processing

**When to Use MongoDB:**
- If you need flexible schema
- If you have unstructured data
- If you need horizontal scaling

**Installation:**
```bash
pip install pymongo
```

### 3.3 Redis

**Version:** Redis 7.2

**Why Redis?**
- **In-Memory Storage**: Extremely fast data access
- **Data Structures**: Strings, Lists, Sets, Hashes, Sorted Sets
- **Pub/Sub**: Message broadcasting for real-time features
- **Caching**: Reduce database load
- **Session Storage**: Fast session management
- **Rate Limiting**: Implement API rate limits
- **Message Broker**: For Celery task queue

**Use Cases in Project:**
- Session storage for JWT tokens
- Caching frequently accessed data
- Real-time message broadcasting (Pub/Sub)
- Rate limiting for API endpoints
- Task queue for Celery
- Temporary data storage

**Key Features Used:**
- **Strings**: Cache simple key-value pairs
- **Hashes**: Store object-like data
- **Lists**: Queue for background tasks
- **Pub/Sub**: Real-time WebSocket updates
- **TTL**: Automatic key expiration

**Installation:**
```bash
# Windows: Download from redis.io
# Linux: sudo apt-get install redis-server
# macOS: brew install redis
```

**Python Driver:**
```bash
pip install redis
```

**Connection Example:**
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Set value
r.set('key', 'value')

# Get value
value = r.get('key')

# Set with expiration
r.setex('session:123', 3600, 'session_data')

# Publish message
r.publish('alerts', 'New threat detected')

# Subscribe to channel
pubsub = r.pubsub()
pubsub.subscribe('alerts')
```

---

## 4. MACHINE LEARNING TECHNOLOGIES

### 4.1 Python

**Version:** Python 3.11

**Why Python for ML?**
- **Rich ML Ecosystem**: Extensive libraries for ML/DL
- **Easy to Learn**: Readable and intuitive syntax
- **Large Community**: Active community and abundant resources
- **Integration**: Easy integration with other technologies
- **Performance**: Optimized libraries (NumPy, Pandas)
- **Prototyping**: Rapid prototyping capabilities

**Use Cases in Project:**
- ML model development
- Data preprocessing
- Feature engineering
- Model training and evaluation
- Model deployment
- Data analysis

### 4.2 Scikit-learn

**Version:** scikit-learn 1.3.2

**Why Scikit-learn?**
- **Comprehensive**: Wide range of ML algorithms
- **Easy to Use**: Consistent API across algorithms
- **Well Documented**: Excellent documentation and examples
- **Performance**: Optimized with NumPy and SciPy
- **Preprocessing**: Built-in data preprocessing tools
- **Model Evaluation**: Comprehensive evaluation metrics
- **Pipeline**: Easy pipeline construction

**Algorithms Used:**
- **Random Forest**: Phishing and malware detection
- **Support Vector Machines (SVM)**: Classification tasks
- **Isolation Forest**: Anomaly detection
- **One-Class SVM**: Anomaly detection
- **Logistic Regression**: Baseline classification
- **Gradient Boosting**: Advanced classification

**Use Cases in Project:**
- Phishing URL classification
- Malware file classification
- User behavior anomaly detection
- Feature selection
- Model evaluation
- Cross-validation

**Installation:**
```bash
pip install scikit-learn
```

**Example Usage:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
```

### 4.3 TensorFlow

**Version:** TensorFlow 2.15

**Why TensorFlow?**
- **Deep Learning**: State-of-the-art deep learning framework
- **Production Ready**: TensorFlow Serving for deployment
- **Flexible**: Supports multiple platforms (CPU, GPU, TPU)
- **Keras Integration**: High-level API for easy model building
- **TensorBoard**: Visualization and monitoring
- **Large Community**: Extensive resources and support

**Use Cases in Project:**
- Deep learning models for malware detection
- Neural networks for complex pattern recognition
- Autoencoders for anomaly detection
- Model deployment with TensorFlow Serving

**Installation:**
```bash
pip install tensorflow
```

**Example Usage:**
```python
import tensorflow as tf
from tensorflow import keras

# Build model
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
```

### 4.4 PyTorch

**Version:** PyTorch 2.1

**Why PyTorch?**
- **Research-Friendly**: Dynamic computation graph
- **Pythonic**: Natural Python integration
- **Debugging**: Easy debugging with Python debugger
- **Flexible**: Custom architectures and research
- **Growing Ecosystem**: Expanding library support

**When to Use PyTorch:**
- If you need custom model architectures
- If you're doing research
- If you prefer dynamic computation graphs

**Installation:**
```bash
pip install torch torchvision
```

### 4.5 Additional ML Libraries

**Pandas**
- **Why**: Data manipulation and analysis
- **Use Case**: Data preprocessing, feature engineering
- **Installation**: `pip install pandas`

**NumPy**
- **Why**: Numerical computing foundation
- **Use Case**: Array operations, mathematical functions
- **Installation**: `pip install numpy`

**Joblib**
- **Why**: Model serialization and parallel processing
- **Use Case**: Save/load trained models
- **Installation**: `pip install joblib`

**MLflow**
- **Why**: Experiment tracking and model management
- **Use Case**: Track experiments, manage models
- **Installation**: `pip install mlflow`

**Imbalanced-learn**
- **Why**: Handle imbalanced datasets
- **Use Case**: SMOTE for oversampling minority class
- **Installation**: `pip install imbalanced-learn`

**XGBoost**
- **Why**: High-performance gradient boosting
- **Use Case**: Advanced classification tasks
- **Installation**: `pip install xgboost`

**LightGBM**
- **Why**: Fast gradient boosting with lower memory usage
- **Use Case**: Large-scale classification
- **Installation**: `pip install lightgbm`

---

## 5. CYBERSECURITY LIBRARIES

### 5.1 Scapy

**Version:** Scapy 2.5.0

**Why Scapy?**
- **Packet Manipulation**: Create, send, and capture network packets
- **Protocol Support**: Support for numerous network protocols
- **Flexible**: Python-based for easy integration
- **Powerful**: Advanced packet analysis capabilities
- **No Dependencies**: Standalone library

**Use Cases in Project:**
- Network traffic monitoring
- Packet analysis
- Network scanning
- Protocol analysis
- Intrusion detection

**Installation:**
```bash
pip install scapy
```

**Example Usage:**
```python
from scapy.all import sniff, IP, TCP

# Packet capture
def packet_callback(packet):
    if packet.haslayer(IP):
        print(f"IP: {packet[IP].src} -> {packet[IP].dst}")

# Start sniffing
sniff(prn=packet_callback, count=100)
```

### 5.2 YARA

**Version:** YARA 4.3

**Why YARA?**
- **Pattern Matching**: Identify malware based on patterns
- **Rule-Based**: Define custom detection rules
- **Fast**: Efficient pattern matching
- **Flexible**: Complex rule definitions
- **Industry Standard**: Widely used in cybersecurity

**Use Cases in Project:**
- Signature-based malware detection
- Custom rule creation
- File classification
- Threat hunting

**Installation:**
```bash
pip install yara-python
```

**Example Usage:**
```python
import yara

# Define rule
rules = yara.compile(source='''
rule silent_banker {
    meta:
        description = "This is just an example"
    strings:
        $a = {6A 40 68 00 30 00 00 6A 14 8D 91}
        $b = {8D 64 24 30 85 C0 74 07}
    condition:
        $a or $b
}
''')

# Scan file
matches = rules.match(filepath='malicious.exe')
```

### 5.3 VirusTotal API

**Version**: VirusTotal API v3

**Why VirusTotal API?**
- **Comprehensive Database**: Access to vast malware database
- **Multiple Engines**: Results from 70+ antivirus engines
- **Reputation Scores**: Domain and file reputation
- **URL Analysis**: Phishing URL detection
- **File Analysis**: Malware file scanning

**Use Cases in Project:**
- Cross-check URLs for phishing
- Verify file hashes against malware database
- Get domain reputation scores
- Enhance ML model predictions

**Installation:**
```bash
pip install requests
```

**Example Usage:**
```python
import requests

API_KEY = 'your-virustotal-api-key'

# Scan URL
url = 'https://www.example.com'
headers = {'x-apikey': API_KEY}
response = requests.post(
    'https://www.virustotal.com/api/v3/urls',
    headers=headers,
    data={'url': url}
)

# Get analysis results
analysis_id = response.json()['data']['id']
response = requests.get(
    f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
    headers=headers
)
```

### 5.4 psutil

**Version**: psutil 5.9.6

**Why psutil?**
- **Cross-Platform**: Works on Windows, Linux, macOS
- **Comprehensive**: System and process utilities
- **Easy to Use**: Simple API
- **Efficient**: Low system overhead
- **Well Documented**: Excellent documentation

**Use Cases in Project:**
- Process monitoring
- CPU usage tracking
- Memory usage monitoring
- Disk usage monitoring
- Network connection monitoring
- Battery status monitoring

**Installation:**
```bash
pip install psutil
```

**Example Usage:**
```python
import psutil

# CPU usage
cpu_percent = psutil.cpu_percent(interval=1)

# Memory usage
memory = psutil.virtual_memory()
ram_percent = memory.percent

# Process list
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    print(proc.info)

# Network connections
connections = psutil.net_connections()
```

### 5.5 Requests

**Version**: requests 2.31.0

**Why Requests?**
- **Simple API**: Easy to use HTTP library
- **Feature Rich**: Sessions, cookies, authentication
- **JSON Support**: Built-in JSON handling
- **Standard**: De facto standard for HTTP in Python

**Use Cases in Project:**
- API calls to external services
- VirusTotal API integration
- Threat intelligence feeds
- Email service integration

**Installation:**
```bash
pip install requests
```

**Example Usage:**
```python
import requests

# GET request
response = requests.get('https://api.example.com/data')
data = response.json()

# POST request
response = requests.post(
    'https://api.example.com/submit',
    json={'key': 'value'},
    headers={'Authorization': 'Bearer token'}
)
```

### 5.6 Additional Cybersecurity Libraries

**pyOpenSSL**
- **Why**: SSL/TLS certificate verification
- **Use Case**: Check SSL certificate validity
- **Installation**: `pip install pyopenssl`

**whois**
- **Why**: Domain information lookup
- **Use Case**: Check domain age for phishing detection
- **Installation**: `pip install python-whois`

**python-nmap**
- **Why**: Network scanning
- **Use Case**: Network discovery and scanning
- **Installation**: `pip install python-nmap`

**cryptography**
- **Why**: Cryptographic operations
- **Use Case**: Encryption, hashing, digital signatures
- **Installation**: `pip install cryptography`

**hashlib**
- **Why**: Built-in Python library for hashing
- **Use Case**: Calculate file hashes for malware detection
- **Installation**: Built-in (no installation needed)

---

## 6. MONITORING TECHNOLOGIES

### 6.1 WebSockets

**Version**: WebSocket Protocol (RFC 6455)

**Why WebSockets?**
- **Real-Time Communication**: Bidirectional real-time data transfer
- **Low Latency**: Minimal overhead compared to HTTP polling
- **Efficient**: Single connection for multiple messages
- **Browser Support**: Native browser support
- **Scalable**: Can handle many concurrent connections

**Use Cases in Project:**
- Real-time threat alerts
- Live monitoring data updates
- Dashboard notifications
- System status updates
- User activity monitoring

**Implementation**:
- **Server**: Socket.IO with FastAPI
- **Client**: Socket.IO client in React

**Server Installation:**
```bash
pip install python-socketio
pip install aiohttp
```

**Client Installation:**
```bash
npm install socket.io-client
```

**Server Example:**
```python
import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app = socketio.ASGIApp(sio, app)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def alert(sid, data):
    await sio.emit('new_alert', data)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
```

**Client Example:**
```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:8000');

socket.on('connect', () => {
  console.log('Connected to server');
});

socket.on('new_alert', (data) => {
  console.log('New alert:', data);
});

socket.on('disconnect', () => {
  console.log('Disconnected from server');
});
```

### 6.2 Celery

**Version**: Celery 5.3.4

**Why Celery?**
- **Distributed Task Queue**: Process tasks asynchronously
- **Scalable**: Distribute tasks across multiple workers
- **Flexible**: Supports multiple message brokers
- **Reliable**: Task retries and error handling
- **Monitoring**: Built-in monitoring with Flower
- **Scheduling**: Periodic task scheduling

**Use Cases in Project:**
- Background file scanning
- Periodic system monitoring
- Email sending
- Data processing
- Model training
- Report generation

**Installation:**
```bash
pip install celery
pip install redis  # as message broker
```

**Example Usage:**
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def scan_file(file_path):
    # Scan file for malware
    result = perform_scan(file_path)
    return result

@app.task
def send_email_alert(user_email, alert_data):
    # Send email notification
    send_email(user_email, alert_data)

# Schedule periodic task
from celery.schedules import crontab

app.conf.beat_schedule = {
    'monitor-system-every-5-seconds': {
        'task': 'tasks.monitor_system',
        'schedule': 5.0,
    },
}
```

**Run Worker:**
```bash
celery -A tasks worker --loglevel=info
```

**Run Beat Scheduler:**
```bash
celery -A tasks beat --loglevel=info
```

### 6.3 Redis (as Message Broker)

**Version**: Redis 7.2

**Why Redis as Message Broker?**
- **Fast**: In-memory operations
- **Reliable**: Persistence options
- **Simple**: Easy to set up and use
- **Scalable**: Cluster support
- **Pub/Sub**: Native pub/sub support

**Use Cases in Project:**
- Celery message broker
- Real-time pub/sub for WebSockets
- Task queue management
- Result backend for Celery

**Configuration with Celery:**
```python
from celery import Celery

app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')
```

---

## 7. DEPLOYMENT TECHNOLOGIES

### 7.1 Docker

**Version**: Docker 24.0

**Why Docker?**
- **Containerization**: Package application with dependencies
- **Consistency**: Same environment across development and production
- **Isolation**: Isolated application environments
- **Scalability**: Easy to scale with containers
- **Portability**: Run anywhere Docker is installed
- **Version Control**: Version control for infrastructure

**Use Cases in Project:**
- Containerize backend API
- Containerize frontend
- Containerize database
- Containerize ML models
- Multi-container orchestration

**Installation:**
```bash
# Windows: Download Docker Desktop from docker.com
# Linux: sudo apt-get install docker.io
# macOS: Download Docker Desktop from docker.com
```

**Dockerfile for Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile for Frontend:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7.2
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 7.2 AWS (Amazon Web Services)

**Why AWS?**
- **Comprehensive Services**: Wide range of cloud services
- **Scalability**: Auto-scaling capabilities
- **Reliability**: 99.99% uptime SLA
- **Global Infrastructure**: Data centers worldwide
- **Security**: Enterprise-grade security
- **Cost-Effective**: Pay-as-you-go pricing

**Services Used:**

**EC2 (Elastic Compute Cloud)**
- **Why**: Virtual servers for application hosting
- **Use Case**: Host backend API and database
- **Instance Type**: t3.medium for development, m5.large for production

**RDS (Relational Database Service)**
- **Why**: Managed PostgreSQL database
- **Use Case**: Host PostgreSQL database
- **Features**: Automated backups, read replicas

**S3 (Simple Storage Service)**
- **Why**: Object storage for files and logs
- **Use Case**: Store ML models, uploaded files, logs
- **Features**: Versioning, lifecycle policies

**CloudWatch**
- **Why**: Monitoring and logging
- **Use Case**: Monitor application performance, set alarms
- **Features**: Metrics, logs, alarms

**Elastic Load Balancer (ELB)**
- **Why**: Distribute traffic across multiple instances
- **Use Case**: Load balancing for backend API
- **Features**: Health checks, SSL termination

**AWS Lambda**
- **Why**: Serverless compute
- **Use Case**: Run periodic tasks, data processing
- **Features**: Pay-per-use, automatic scaling

**IAM (Identity and Access Management)**
- **Why**: Access control and security
- **Use Case**: Manage user permissions
- **Features**: Role-based access control

**Deployment Steps:**
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Create EC2 instance
aws ec2 run-instances --image-id ami-xxx --instance-type t3.medium

# Create RDS instance
aws rds create-db-instance --db-instance-identifier mydb --db-instance-class db.t3.micro --engine postgres

# Deploy with Docker
docker build -t myapp .
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

### 7.3 Render (Alternative)

**Why Render?**
- **Simple PaaS**: Easy deployment without complex configuration
- **Free Tier**: Generous free tier for small projects
- **Auto-Deploy**: Automatic deployment from Git
- **SSL**: Free SSL certificates
- **Databases**: Managed PostgreSQL and Redis
- **Fast Setup**: Deploy in minutes

**When to Use Render:**
- For smaller projects
- For rapid prototyping
- If you prefer simplicity over control
- For student projects

**Services Used:**
- **Web Service**: Host backend API
- **Static Site**: Host frontend
- **PostgreSQL**: Managed database
- **Redis**: Managed Redis

**Deployment Steps:**
```bash
# Install Render CLI
npm install -g render

# Login
render login

# Initialize
render init

# Deploy
render deploy
```

**render.yaml Configuration:**
```yaml
services:
  - type: web
    name: backend-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: redis
          property: connectionString

databases:
  - name: postgres
    databaseName: digital_bodyguard
    user: admin

  - name: redis
```

---

## 8. DEVELOPMENT TOOLS

### 8.1 Version Control

**Git**
- **Why**: Distributed version control
- **Use Case**: Source code management
- **Platform**: GitHub/GitLab

### 8.2 IDE

**VS Code**
- **Why**: Lightweight, extensible, free
- **Extensions**: Python, React, Docker, Git

**PyCharm**
- **Why**: Python-specific IDE with excellent features
- **Use Case**: Backend development

### 8.3 API Testing

**Postman**
- **Why**: API testing and documentation
- **Use Case**: Test API endpoints during development

**Insomnia**
- **Why**: Lightweight REST client
- **Use Case**: Alternative to Postman

### 8.4 Database Management

**pgAdmin**
- **Why**: PostgreSQL management tool
- **Use Case**: Manage PostgreSQL database

**DBeaver**
- **Why**: Universal database tool
- **Use Case**: Manage multiple database types

### 8.5 Container Management

**Docker Desktop**
- **Why**: Easy Docker management
- **Use Case**: Run and manage containers locally

### 8.6 CI/CD

**GitHub Actions**
- **Why**: Integrated with GitHub, free for public repos
- **Use Case**: Automated testing and deployment

**GitLab CI**
- **Why**: Integrated with GitLab
- **Use Case**: Alternative to GitHub Actions

---

## 9. COMPLETE DEPENDENCIES

### 9.1 Backend Requirements (requirements.txt)

```txt
# FastAPI and Server
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Redis
redis==5.0.1

# WebSocket
python-socketio==5.10.0
aiohttp==3.9.1

# Task Queue
celery==5.3.4

# Machine Learning
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
joblib==1.3.2
xgboost==2.0.2
lightgbm==4.2.0
imbalanced-learn==0.11.0

# Deep Learning
tensorflow==2.15.0

# Cybersecurity
scapy==2.5.0
yara-python==4.3.1
psutil==5.9.6
requests==2.31.0
pyopenssl==23.3.0
python-whois==0.8.0
cryptography==41.0.7

# Utilities
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Monitoring
prometheus-client==0.19.0
```

### 9.2 Frontend Requirements (package.json)

```json
{
  "name": "ai-digital-bodyguard-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "socket.io-client": "^4.6.0",
    "recharts": "^2.10.3",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "bootstrap": "^5.3.2",
    "@mui/material": "^5.14.18",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.18",
    "zustand": "^4.4.7",
    "react-query": "^3.39.3",
    "date-fns": "^2.30.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "react-scripts": "5.0.1",
    "@types/react": "^18.2.42",
    "@types/react-dom": "^18.2.17",
    "typescript": "^5.3.2"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

---

## 10. TECHNOLOGY STACK SUMMARY

### 10.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                          │
│  React.js + HTML5 + CSS3 + Bootstrap + Material-UI         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND LAYER                           │
│  Python FastAPI + Celery + Socket.IO                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQL/NoSQL
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                              │
│  PostgreSQL + Redis + File Storage                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Model Inference
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 MACHINE LEARNING LAYER                       │
│  Scikit-learn + TensorFlow + XGBoost + LightGBM            │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ System Calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                CYBERSECURITY LAYER                           │
│  Scapy + YARA + VirusTotal API + psutil                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Deployment
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  DEPLOYMENT LAYER                           │
│  Docker + AWS/Render + Nginx + GitHub Actions              │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 Technology Selection Rationale

| Category | Technology | Primary Reason |
|----------|-----------|----------------|
| Frontend Framework | React.js | Component-based, large ecosystem, excellent performance |
| UI Library | Bootstrap | Pre-built components, rapid development |
| Backend Framework | FastAPI | Modern, fast, auto-documentation, async support |
| Database | PostgreSQL | ACID compliant, JSONB support, scalable |
| Cache | Redis | In-memory, fast, pub/sub support |
| ML Library | Scikit-learn | Comprehensive, easy to use, well documented |
| Deep Learning | TensorFlow | Production-ready, extensive features |
| Cybersecurity | YARA | Industry standard for malware detection |
| Monitoring | psutil | Cross-platform, comprehensive system monitoring |
| Network | Scapy | Powerful packet manipulation |
| Task Queue | Celery | Distributed, scalable, reliable |
| Real-time | WebSockets | Low latency, bidirectional |
| Containerization | Docker | Consistency, portability, scalability |
| Cloud | AWS | Comprehensive services, scalable, reliable |

### 10.3 Advantages of This Stack

**Performance:**
- FastAPI for high-performance API
- Redis for fast caching
- Optimized ML libraries

**Scalability:**
- Docker for containerization
- AWS for cloud scaling
- Celery for distributed tasks

**Development Speed:**
- React component reusability
- FastAPI auto-documentation
- Bootstrap pre-built components

**Maintainability:**
- Type hints in Python
- Modular architecture
- Comprehensive testing tools

**Security:**
- JWT authentication
- PostgreSQL security features
- Industry-standard cybersecurity libraries

**Cost-Effectiveness:**
- Open-source technologies
- Free tier options (Render)
- Pay-as-you-go (AWS)

---

## 11. CONCLUSION

This technology stack provides a robust, scalable, and modern foundation for the AI-Powered Digital Bodyguard system. The selected technologies offer:

- **Performance**: High-performance components for real-time threat detection
- **Scalability**: Cloud-native architecture for growth
- **Security**: Industry-standard security libraries and practices
- **Maintainability**: Modern, well-documented technologies
- **Cost-Effectiveness**: Open-source with flexible deployment options

**Next Steps:**
1. Review and approve this Technology Stack
2. Proceed to Phase 4: Module Design
3. Begin implementation with approved technologies

---

## APPENDICES

### Appendix A: Alternative Technology Options

**Frontend Alternatives:**
- Vue.js: Progressive framework, easier learning curve
- Angular: Full-featured framework, enterprise-grade
- Svelte: Compile-time framework, smaller bundle size

**Backend Alternatives:**
- Django: Full-featured framework, batteries included
- Node.js/Express: JavaScript backend, same language as frontend
- Go: High performance, compiled language

**Database Alternatives:**
- MySQL: Popular open-source relational database
- MongoDB: NoSQL document database
- Cassandra: Distributed NoSQL database

**ML Alternatives:**
- Keras: High-level deep learning API
- Theano: Older deep learning framework
- Caffe: Deep learning framework for vision

### Appendix B: Technology Resources

**Official Documentation:**
- React: https://react.dev
- FastAPI: https://fastapi.tiangolo.com
- PostgreSQL: https://www.postgresql.org/docs
- Scikit-learn: https://scikit-learn.org
- TensorFlow: https://www.tensorflow.org

**Learning Resources:**
- FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/
- React Tutorial: https://react.dev/learn
- ML Crash Course: https://developers.google.com/machine-learning/crash-course

**Community:**
- Stack Overflow: https://stackoverflow.com
- GitHub: https://github.com
- Reddit: r/Python, r/MachineLearning, r/cybersecurity
