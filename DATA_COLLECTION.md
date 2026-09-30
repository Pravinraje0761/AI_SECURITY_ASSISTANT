# Data Collection Document
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. DATA COLLECTION OVERVIEW

This document provides comprehensive information about datasets required for training machine learning models for the AI-Powered Digital Bodyguard system. It includes dataset sources, descriptions, download instructions, and preprocessing steps for each type of cybersecurity data.

### 1.1 Data Requirements Summary

| Data Type | Purpose | Model | Sample Size | Format |
|-----------|---------|-------|-------------|--------|
| Phishing URLs | Phishing detection | Random Forest, XGBoost | 100,000+ | CSV |
| Malware Samples | Malware detection | Random Forest, Neural Network | 10,000+ | PE files |
| Network Intrusion | Network threat detection | SVM, Random Forest | 2M+ records | CSV, PCAP |
| User Behavior | Anomaly detection | Isolation Forest, Autoencoder | 50,000+ sessions | CSV |
| Ransomware Data | Ransomware detection | XGBoost, Neural Network | 5,000+ samples | PE files, logs |

---

## 2. PHISHING URLS DATASETS

### 2.1 PhishTank Dataset

**Source**: https://www.phishtank.com/developer_info.php

**Description**: Community-driven phishing URL database with verified phishing URLs

**Dataset Details**:
- **Size**: 50,000+ verified phishing URLs
- **Format**: CSV, JSON
- **Update Frequency**: Daily
- **License**: Creative Commons BY-SA
- **Features**: URL, submission date, verification status, target

**Download Instructions**:
```bash
# Register for API key at PhishTank
# Use API to download dataset
curl -X GET "https://data.phishtank.com/data/online-valid.csv" -o phishtank.csv
```

**API Access**:
```python
import requests

API_KEY = 'your-api-key'
response = requests.get(
    f'https://data.phishtank.com/data/{API_KEY}/online-valid.csv'
)
with open('phishtank.csv', 'wb') as f:
    f.write(response.content)
```

**Preprocessing Steps**:
1. **Data Cleaning**:
   - Remove duplicate URLs
   - Filter out invalid URLs
   - Remove URLs with missing fields

2. **Feature Extraction**:
   - Extract URL length
   - Count dots, digits, special characters
   - Extract domain and subdomain
   - Check for IP address in URL
   - Extract TLD (Top Level Domain)
   - Check HTTPS usage

3. **Label Encoding**:
   - Phishing: 1
   - Legitimate: 0 (need legitimate dataset)

4. **Data Balancing**:
   - Use SMOTE for oversampling if imbalanced
   - Or undersample majority class

**Sample Code**:
```python
import pandas as pd
from urllib.parse import urlparse
import tldextract

def extract_url_features(url):
    features = {}
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_special_chars'] = sum(not c.isalnum() for c in url)
    features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    features['has_https'] = 1 if parsed.scheme == 'https' else 0
    features['has_ip'] = 1 if parsed.hostname.replace('.', '').isdigit() else 0
    features['tld'] = ext.suffix
    features['domain'] = ext.domain
    
    return features

# Load dataset
df = pd.read_csv('phishtank.csv')
df['label'] = 1  # Phishing

# Extract features
features_df = df['url'].apply(extract_url_features).apply(pd.Series)
df = pd.concat([df, features_df], axis=1)
```

### 2.2 Kaggle Phishing Dataset

**Source**: https://www.kaggle.com/datasets

**Recommended Datasets**:

#### 2.2.1 Phishing Site URLs Dataset
- **URL**: https://www.kaggle.com/datasets/amananandrai/phishing-site-urls
- **Size**: 6,000+ URLs
- **Format**: CSV
- **Features**: URL, label (phishing/legitimate)

#### 2.2.2 Malicious URLs Dataset
- **URL**: https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset
- **Size**: 650,000+ URLs
- **Format**: CSV
- **Features**: URL, label, type (defacement, phishing, malware)

**Download Instructions**:
```bash
# Using Kaggle API
kaggle datasets download -d amananandrai/phishing-site-urls
unzip phishing-site-urls.zip
```

**Preprocessing Steps**:
1. Combine PhishTank with Kaggle datasets
2. Remove duplicates across datasets
3. Apply feature extraction to all URLs
4. Balance classes if needed
5. Split into train/validation/test sets (70/15/15)

### 2.3 Legitimate URL Dataset

**Source**: Alexa Top 1 Million (defunct) or Common Crawl

**Alternative Sources**:
- **Cisco Umbrella 1 Million**: https://umbrella.cisco.com/
- **Tranco List**: https://tranco-list.eu/
- **Common Crawl**: https://commoncrawl.org/

**Download Instructions**:
```bash
# Download Tranco list
wget https://tranco-list.eu/top-1m.csv.zip
unzip top-1m.csv.zip
```

**Preprocessing**:
1. Filter out domains that redirect
2. Add http:// or https:// prefix
3. Extract features same as phishing URLs
4. Label as 0 (legitimate)

### 2.4 Combined Phishing Dataset Structure

**Final Dataset Schema**:
```csv
url,label,url_length,num_dots,num_digits,num_special_chars,subdomain_count,has_https,has_ip,tld,domain
http://phishing.example.com,1,35,2,0,0,1,0,0,com,example
https://legitimate.com,0,22,1,0,0,0,1,0,com,legitimate
```

**Expected Final Size**: 100,000+ URLs (50,000 phishing, 50,000 legitimate)

---

## 3. MALWARE SAMPLES DATASETS

### 3.1 VirusShare

**Source**: https://virusshare.com/

**Description**: Large repository of malware samples

**Dataset Details**:
- **Size**: 40+ million malware samples
- **Format**: PE files, ELF, scripts
- **Access**: Registration required
- **License**: Research/educational use
- **Update Frequency**: Daily

**Download Instructions**:
```bash
# Register at virusshare.com
# Download samples using provided hashes
# Example using API (if available)
curl -X GET "https://virusshare.com/api/v4/file/{hash}" -H "Authorization: Bearer {api_key}"
```

**Sample Selection Strategy**:
1. Download recent samples (last 6 months)
2. Select diverse malware types:
   - Ransomware
   - Trojans
   - Worms
   - Spyware
   - Adware
3. Aim for 5,000-10,000 samples
4. Include both packed and unpacked samples

### 3.2 EURECOM Malicious Dataset

**Source**: https://www.eurecom.fr/en/publication/4898

**Description**: Labeled dataset of malicious and benign Android applications

**Dataset Details**:
- **Size**: 10,000+ APK files
- **Format**: APK files
- **Labels**: Malicious/Benign
- **License**: Research use

**Download Instructions**:
```bash
# Request access from EURECOM
# Download via provided link
wget http://www.eurecom.fr/~zimmermann/Dataset/Drebin.tar.gz
tar -xzf Drebin.tar.gz
```

### 3.3 Kaggle Malware Datasets

**Recommended Datasets**:

#### 3.3.1 Malware Analysis Dataset
- **URL**: https://www.kaggle.com/datasets/amauricio/malware-analysis-datasets
- **Size**: 10,000+ samples
- **Format**: PE files, CSV features
- **Features**: PE header, imports, exports, sections

#### 3.3.2 Microsoft Malware Classification
- **URL**: https://www.kaggle.com/c/malware-classification
- **Size**: 9TB of data
- **Format**: PE files, byte files, asm files
- **Labels**: 9 malware families

**Download Instructions**:
```bash
kaggle competitions download -c malware-classification
```

### 3.4 Benign Software Dataset

**Source**: System32, Program Files, or trusted software repositories

**Sources**:
- **Windows System Files**: C:\Windows\System32\
- **Common Software**: Notepad, Calculator, etc.
- **Open Source**: https://sourceforge.net/, https://github.com/

**Collection Strategy**:
1. Collect 5,000-10,000 benign executables
2. Include diverse software types:
   - System utilities
   - Office applications
   - Media players
   - Development tools
3. Ensure from trusted sources

### 3.5 Malware Feature Extraction

**PE File Features to Extract**:
```python
import pefile
import hashlib
import math

def extract_pe_features(file_path):
    pe = pefile.PE(file_path)
    features = {}
    
    # File hashes
    with open(file_path, 'rb') as f:
        data = f.read()
    features['md5'] = hashlib.md5(data).hexdigest()
    features['sha256'] = hashlib.sha256(data).hexdigest()
    
    # Basic file info
    features['file_size'] = len(data)
    features['compile_time'] = pe.FILE_HEADER.TimeDateStamp
    
    # Section information
    features['num_sections'] = len(pe.sections)
    sections_entropy = []
    for section in pe.sections:
        entropy = calculate_entropy(section.get_data())
        sections_entropy.append(entropy)
    features['avg_section_entropy'] = sum(sections_entropy) / len(sections_entropy)
    features['max_section_entropy'] = max(sections_entropy)
    
    # Import information
    try:
        features['num_imports'] = len(pe.DIRECTORY_ENTRY_IMPORT)
        imports = []
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            imports.append(entry.dll.decode())
        features['imports'] = imports
    except:
        features['num_imports'] = 0
        features['imports'] = []
    
    # Export information
    try:
        features['num_exports'] = len(pe.DIRECTORY_ENTRY_EXPORT.symbols)
    except:
        features['num_exports'] = 0
    
    # Header information
    features['entry_point'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    features['image_base'] = pe.OPTIONAL_HEADER.ImageBase
    
    # Resources
    try:
        features['has_resources'] = 1 if pe.DIRECTORY_ENTRY_RESOURCE else 0
    except:
        features['has_resources'] = 0
    
    # Debug information
    try:
        features['has_debug'] = 1 if pe.DIRECTORY_ENTRY_DEBUG else 0
    except:
        features['has_debug'] = 0
    
    # Packed detection
    features['is_packed'] = 1 if features['max_section_entropy'] > 7.0 else 0
    
    return features

def calculate_entropy(data):
    if not data:
        return 0.0
    counts = {}
    for byte in data:
        counts[byte] = counts.get(byte, 0) + 1
    entropy = 0.0
    for count in counts.values():
        p = count / len(data)
        entropy -= p * math.log2(p)
    return entropy
```

### 3.6 Preprocessing Steps

1. **File Validation**:
   - Verify PE file format
   - Remove corrupted files
   - Check file size limits (< 50MB)

2. **Feature Extraction**:
   - Extract PE header features
   - Calculate entropy
   - Extract import/export tables
   - Analyze sections

3. **Label Assignment**:
   - Malware：1
   - Benign：0

4. **Data Balancing**:
   - Balance malware and benign samples
   - Use SMOTE if needed

5. **Feature Scaling**:
   - Normalize numerical features
   - Encode categorical features

---

## 4. NETWORK INTRUSION DATASETS

### 4.1 CICIDS2017 Dataset

**Source**: https://www.unb.ca/cic/datasets/ids-2017.html

**Description**: Comprehensive intrusion detection dataset with various attack types

**Dataset Details**:
- **Size**: 2.8M records
- **Format**: PCAP files, CSV
- **Duration**: 5 days of traffic
- **Attack Types**: DoS, DDoS, PortScan, Botnet, Infiltration
- **Features**: 80+ network flow features
- **License**: Research use

**Download Instructions**:
```bash
# Download from official website
# Requires registration
wget http://205.174.165.80/CIC/CIC-IDS-2017/Dataset/CIC-IDS-2017.zip
unzip CIC-IDS-2017.zip
```

**Dataset Files**:
- Monday: Normal traffic (benign)
- Tuesday: DoS attacks
- Wednesday: Web attacks, infiltration
- Thursday: DoS, botnet
- Friday: DDoS, port scan

**Preprocessing Steps**:
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

def preprocess_cicids2017(file_path):
    # Load data
    df = pd.read_csv(file_path)
    
    # Handle missing values
    df = df.dropna()
    
    # Remove infinite values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    # Encode labels
    le = LabelEncoder()
    df['label'] = le.fit_transform(df['Label'])
    
    # Select features
    feature_cols = [col for col in df.columns if col not in ['Label', 'label', 'Timestamp']]
    X = df[feature_cols]
    y = df['label']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, le.classes_
```

### 4.2 UNSW-NB15 Dataset

**Source**: https://www.unsw.adfa.edu.au/unsw-canberra/cyber/cybersecurity/UNSW-NB15-dataset/

**Description**: Network intrusion dataset with 9 attack types

**Dataset Details**:
- **Size**: 2.5M records
- **Format**: CSV, PCAP
- **Attack Types**: Fuzzers, Analysis, Backdoors, DoS, Exploits, Generic, Reconnaissance, Shellcode, Worms
- **Features**: 49 features
- **License**: Research use

**Download Instructions**:
```bash
# Download from official website
wget https://www.unsw.adfa.edu.au/unsw-canberra/cyber/cybersecurity/UNSW-NB15-dataset/downloads/UNSW-NB15_1.csv
wget https://www.unsw.adfa.edu.au/unsw-canberra/cyber/cybersecurity/UNSW-NB15-dataset/downloads/UNSW-NB15_2.csv
wget https://www.unsw.adfa.edu.au/unsw-canberra/cyber/cybersecurity/UNSW-NB15-dataset/downloads/UNSW-NB15_3.csv
wget https://www.unsw.adfa.edu.au/unsw-canberra/cyber/cybersecurity/UNSW-NB15-dataset/downloads/UNSW-NB15_4.csv
```

**Preprocessing Steps**:
```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def preprocess_unsw_nb15(file_path):
    # Load data
    df = pd.read_csv(file_path)
    
    # Handle categorical features
    categorical_cols = ['proto', 'service', 'state']
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    # Encode attack labels
    attack_cat_encoder = LabelEncoder()
    df['attack_cat'] = attack_cat_encoder.fit_transform(df['attack_cat'].astype(str))
    
    # Binary classification (attack vs normal)
    df['label'] = df['label'].apply(lambda x: 1 if x == 1 else 0)
    
    # Select features
    feature_cols = [col for col in df.columns if col not in ['attack_cat', 'label']]
    X = df[feature_cols]
    y = df['label']
    
    return X, y
```

### 4.3 KDD Cup 1999 Dataset

**Source**: http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html

**Description**: Classic intrusion detection dataset

**Dataset Details**:
- **Size**: 5M records
- **Format**: CSV
- **Attack Types**: DoS, Probe, R2L, U2R
- **Features**: 41 features
- **License**: Public domain

**Download Instructions**:
```bash
wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data.gz
gunzip kddcup.data.gz
```

### 4.4 NSL-KDD Dataset

**Source**: https://www.unb.ca/cic/datasets/nsl.html

**Description**: Improved version of KDD Cup 1999

**Dataset Details**:
- **Size**: 125K training records, 22K test records
- **Format**: CSV
- **Attack Types**: Same as KDD Cup 1999
- **Features**: 41 features
- **License**: Research use

**Download Instructions**:
```bash
wget https://www.unb.ca/cic/datasets/nsl/kdd/KDDTrain+.txt
wget https://www.unb.ca/cic/datasets/nsl/kdd/KDDTest+.txt
```

### 4.5 Network Feature Extraction

**Key Network Features**:
```python
def extract_network_features(flow):
    features = {}
    
    # Basic flow features
    features['duration'] = flow['duration']
    features['protocol'] = flow['protocol']
    features['src_bytes'] = flow['src_bytes']
    features['dst_bytes'] = flow['dst_bytes']
    
    # Statistical features
    features['src_bytes_mean'] = flow['src_bytes_mean']
    features['src_bytes_std'] = flow['src_bytes_std']
    features['dst_bytes_mean'] = flow['dst_bytes_mean']
    features['dst_bytes_std'] = flow['dst_bytes_std']
    
    # Time-based features
    features['packet_count'] = flow['packet_count']
    features['packet_rate'] = flow['packet_count'] / flow['duration']
    
    # Flag features
    features['tcp_flags'] = flow['tcp_flags']
    
    # Connection features
    features['same_src_count'] = flow['same_src_count']
    features['same_dst_count'] = flow['same_dst_count']
    features['same_srv_count'] = flow['same_srv_count']
    
    return features
```

### 4.6 Preprocessing Pipeline

1. **Data Cleaning**:
   - Remove duplicate flows
   - Handle missing values
   - Remove infinite values

2. **Feature Encoding**:
   - Encode categorical features (protocol, service, flags)
   - Use LabelEncoder or OneHotEncoder

3. **Feature Scaling**:
   - Normalize numerical features
   - Use StandardScaler or MinMaxScaler

4. **Label Encoding**:
   - Binary: Normal (0) vs Attack (1)
   - Multi-class: Attack types

5. **Data Splitting**:
   - Train: 70%
   - Validation: 15%
   - Test: 15%

---

## 5. USER BEHAVIOR LOGS DATASETS

### 5.1 Synthetic User Behavior Dataset

**Source**: Generate synthetic data based on realistic patterns

**Description**: Simulated user behavior for anomaly detection

**Dataset Details**:
- **Size**: 50,000+ user sessions
- **Format**: CSV
- **Features**: Login times, user actions, file access, network activity
- **Labels**: Normal (0), Anomalous (1)

**Generation Strategy**:
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_user_behavior_data(num_users=100, days=30):
    data = []
    
    for user_id in range(num_users):
        # Generate normal behavior patterns
        for day in range(days):
            # Login time (normal: 8-10 AM, 6-8 PM)
            if random.random() < 0.7:
                login_hour = random.choice([8, 9, 18, 19])
            else:
                login_hour = random.randint(0, 23)
            
            login_time = datetime(2026, 1, 1) + timedelta(days=day, hours=login_hour)
            
            # Session duration (normal: 2-8 hours)
            session_duration = random.uniform(2, 8)
            
            # File access count (normal: 10-50 files)
            file_access_count = random.randint(10, 50)
            
            # Network activity (normal: 100-500 MB)
            network_activity = random.uniform(100, 500)
            
            # Browser activity (normal: 20-100 sites)
            browser_sites = random.randint(20, 100)
            
            data.append({
                'user_id': user_id,
                'timestamp': login_time,
                'login_hour': login_hour,
                'session_duration': session_duration,
                'file_access_count': file_access_count,
                'network_activity_mb': network_activity,
                'browser_sites_visited': browser_sites,
                'label': 0  # Normal
            })
    
    # Generate anomalous behavior (10% of data)
    num_anomalies = len(data) // 10
    for i in range(num_anomalies):
        idx = random.randint(0, len(data) - 1)
        
        # Anomalous patterns
        data[idx]['login_hour'] = random.randint(0, 5)  # Unusual time
        data[idx]['session_duration'] = random.uniform(10, 15)  # Unusually long
        data[idx]['file_access_count'] = random.randint(100, 200)  # Unusually high
        data[idx]['network_activity_mb'] = random.uniform(1000, 2000)  # Unusually high
        data[idx]['browser_sites_visited'] = random.randint(200, 300)  # Unusually high
        data[idx]['label'] = 1  # Anomalous
    
    return pd.DataFrame(data)

# Generate dataset
behavior_df = generate_user_behavior_data(num_users=100, days=30)
behavior_df.to_csv('user_behavior_dataset.csv', index=False)
```

### 5.2 Windows Event Logs

**Source**: Local system event logs or public datasets

**Description**: Windows security event logs for user behavior analysis

**Dataset Details**:
- **Size**: Variable
- **Format**: EVTX, CSV
- **Event IDs**: 4624 (logon), 4625 (failed logon), 5140 (network share access)
- **Features**: Event ID, timestamp, user, computer, logon type

**Collection Instructions**:
```python
import pandas as pd
from evtx import Evtx

def parse_windows_logs(log_path):
    with Evtx(log_path) as evtx:
        records = []
        for record in evtx.records():
            xml = record.xml()
            # Parse XML to extract relevant fields
            # Event ID, timestamp, user, etc.
            records.append(parse_event_xml(xml))
    return pd.DataFrame(records)
```

### 5.3 Kaggle User Behavior Datasets

**Recommended Datasets**:

#### 5.3.1 User Behavior Dataset
- **URL**: https://www.kaggle.com/datasets
- **Search**: "user behavior", "anomaly detection"
- **Features**: User actions, timestamps, session data

### 5.4 Behavior Feature Extraction

**Key Behavior Features**:
```python
def extract_behavior_features(session):
    features = {}
    
    # Temporal features
    features['login_hour'] = session['timestamp'].hour
    features['login_day_of_week'] = session['timestamp'].weekday()
    features['session_duration'] = session['session_duration']
    
    # Activity features
    features['file_access_count'] = session['file_access_count']
    features['network_activity_mb'] = session['network_activity_mb']
    features['browser_sites_visited'] = session['browser_sites_visited']
    
    # Derived features
    features['files_per_hour'] = session['file_access_count'] / session['session_duration']
    features['network_per_hour'] = session['network_activity_mb'] / session['session_duration']
    features['sites_per_hour'] = session['browser_sites_visited'] / session['session_duration']
    
    return features
```

### 5.5 Preprocessing Steps

1. **Data Cleaning**:
   - Remove incomplete sessions
   - Handle missing values
   - Remove outliers

2. **Feature Engineering**:
   - Extract temporal features
   - Calculate derived features
   - Create user-specific baselines

3. **Normalization**:
   - Normalize numerical features
   - Scale features to [0, 1]

4. **Label Assignment**:
   - Normal: 0
   - Anomalous: 1

5. **Train/Test Split**:
   - Use time-based split
   - Train on earlier data, test on recent data

---

## 6. RANSOMWARE DATASETS

### 6.1 Ransomware Samples

**Source**: VirusShare, MalwareBazaar, Hybrid Analysis

**Description**: Ransomware samples for detection and analysis

**Dataset Details**:
- **Size**: 5,000+ samples
- **Format**: PE files
- **Families**: WannaCry, Petya, Locky, Cerber, etc.
- **License**: Research use

**Download Instructions**:
```bash
# From VirusShare
# Search for ransomware samples
# Download using hash

# From MalwareBazaar
# API access
curl -X POST "https://mb-api.abuse.ch/api/v1/" \
  -d "query=get_siginfo" \
  -d "sha256_hash={hash}"
```

### 6.2 Ransomware Behavior Logs

**Source**: CIC ransomware datasets

**Description**: Ransomware behavior during execution

**Dataset Details**:
- **Size**: Variable
- **Format**: CSV, JSON
- **Features**: File operations, registry changes, network activity
- **Source**: https://www.unb.ca/cic/datasets/ransomware-dataset.html

**Download Instructions**:
```bash
# Download from CIC website
wget https://www.unb.ca/cic/datasets/ransomware-dataset.zip
unzip ransomware-dataset.zip
```

### 6.3 Ransomware Feature Extraction

**Key Ransomware Features**:
```python
def extract_ransomware_features(behavior_log):
    features = {}
    
    # File encryption behavior
    features['files_encrypted'] = behavior_log['files_encrypted']
    features['file_encryption_rate'] = behavior_log['files_encrypted'] / behavior_log['duration']
    
    # Ransom note behavior
    features['ransom_note_created'] = 1 if behavior_log['ransom_note'] else 0
    features['ransom_note_extensions'] = len(behavior_log['note_extensions'])
    
    # Network behavior
    features['c2_communication'] = 1 if behavior_log['c2_contact'] else 0
    features['unique_domains'] = len(behavior_log['domains_contacted'])
    
    # Registry behavior
    features['registry_changes'] = behavior_log['registry_changes']
    features['persistence_mechanism'] = 1 if behavior_log['persistence'] else 0
    
    # Process behavior
    features['process_injection'] = 1 if behavior_log['injection'] else 0
    features['privilege_escalation'] = 1 if behavior_log['escalation'] else 0
    
    return features
```

### 6.4 Preprocessing Steps

1. **Sample Validation**:
   - Verify ransomware family
   - Remove corrupted samples
   - Ensure behavior logs are complete

2. **Feature Extraction**:
   - Extract behavioral features
   - Extract PE features
   - Combine both feature sets

3. **Label Encoding**:
   - Ransomware: 1
   - Benign: 0

4. **Family Classification**:
   - Multi-class: Ransomware families
   - Binary: Ransomware vs non-ransomware malware

---

## 7. DATA PREPROCESSING PIPELINE

### 7.1 Common Preprocessing Steps

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.smote = SMOTE()
    
    def clean_data(self, df):
        """Remove duplicates, handle missing values"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.dropna()
        
        # Remove infinite values
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna()
        
        return df
    
    def encode_categorical(self, df, categorical_cols):
        """Encode categorical features"""
        for col in categorical_cols:
            if col in df.columns:
                df[col] = self.label_encoder.fit_transform(df[col].astype(str))
        return df
    
    def scale_features(self, X):
        """Scale numerical features"""
        return self.scaler.fit_transform(X)
    
    def balance_data(self, X, y):
        """Balance imbalanced dataset using SMOTE"""
        X_resampled, y_resampled = self.smote.fit_resample(X, y)
        return X_resampled, y_resampled
    
    def split_data(self, X, y, test_size=0.2, val_size=0.15):
        """Split data into train, validation, test sets"""
        # First split: train + val, test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Second split: train, val
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=42, stratify=y_temp
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test
```

### 7.2 Dataset-Specific Preprocessing

#### Phishing Dataset
```python
def preprocess_phishing_dataset(df):
    preprocessor = DataPreprocessor()
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Encode categorical features (TLD)
    categorical_cols = ['tld']
    df = preprocessor.encode_categorical(df, categorical_cols)
    
    # Select features
    feature_cols = ['url_length', 'num_dots', 'num_digits', 'num_special_chars',
                   'subdomain_count', 'has_https', 'has_ip', 'tld']
    X = df[feature_cols]
    y = df['label']
    
    # Scale features
    X = preprocessor.scale_features(X)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(X, y)
    
    return X_train, X_val, X_test, y_train, y_val, y_test
```

#### Malware Dataset
```python
def preprocess_malware_dataset(df):
    preprocessor = DataPreprocessor()
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Encode categorical features
    categorical_cols = ['tld']  # if applicable
    df = preprocessor.encode_categorical(df, categorical_cols)
    
    # Select features
    feature_cols = ['file_size', 'num_sections', 'num_imports', 'num_exports',
                   'avg_section_entropy', 'max_section_entropy', 'is_packed',
                   'has_resources', 'has_debug']
    X = df[feature_cols]
    y = df['label']
    
    # Scale features
    X = preprocessor.scale_features(X)
    
    # Balance data if needed
    X, y = preprocessor.balance_data(X, y)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(X, y)
    
    return X_train, X_val, X_test, y_train, y_val, y_test
```

#### Network Intrusion Dataset
```python
def preprocess_network_dataset(df):
    preprocessor = DataPreprocessor()
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Encode categorical features
    categorical_cols = ['protocol', 'service', 'state']
    df = preprocessor.encode_categorical(df, categorical_cols)
    
    # Select features
    feature_cols = [col for col in df.columns if col not in ['label', 'attack_cat']]
    X = df[feature_cols]
    y = df['label']
    
    # Scale features
    X = preprocessor.scale_features(X)
    
    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(X, y)
    
    return X_train, X_val, X_test, y_train, y_val, y_test
```

---

## 8. DATA STORAGE AND MANAGEMENT

### 8.1 Directory Structure

```
data/
├── phishing/
│   ├── raw/
│   │   ├── phishtank.csv
│   │   ├── kaggle_phishing.csv
│   │   └── legitimate_urls.csv
│   ├── processed/
│   │   ├── phishing_features.csv
│   │   └── phishing_labels.csv
│   └── models/
│       └── phishing_model.pkl
├── malware/
│   ├── raw/
│   │   ├── virusshare/
│   │   ├── kaggle_malware/
│   │   └── benign/
│   ├── processed/
│   │   ├── malware_features.csv
│   │   └── malware_labels.csv
│   └── models/
│       └── malware_model.pkl
├── network/
│   ├── raw/
│   │   ├── cicids2017/
│   │   └── unsw-nb15/
│   ├── processed/
│   │   ├── network_features.csv
│   │   └── network_labels.csv
│   └── models/
│       └── network_model.pkl
├── behavior/
│   ├── raw/
│   │   └── user_behavior.csv
│   ├── processed/
│   │   ├── behavior_features.csv
│   │   └── behavior_labels.csv
│   └── models/
│       └── behavior_model.pkl
└── ransomware/
    ├── raw/
    │   └── ransomware_samples/
    ├── processed/
    │   ├── ransomware_features.csv
    │   └── ransomware_labels.csv
    └── models/
        └── ransomware_model.pkl
```

### 8.2 Data Versioning

Use DVC (Data Version Control) for dataset versioning:

```bash
# Install DVC
pip install dvc

# Initialize DVC
dvc init

# Track datasets
dvc add data/phishing/raw/phishtank.csv
dvc add data/malware/raw/

# Commit changes
git add data/.gitignore data/phishing/raw/phishtank.csv.dvc .dvc
git commit -m "Add phishing dataset"
```

### 8.3 Data Augmentation

For small datasets, use data augmentation:

```python
def augment_phishing_urls(urls):
    """Generate augmented phishing URLs"""
    augmented = []
    
    for url in urls:
        # Add subdomains
        augmented.append(f"www.{url}")
        augmented.append(f"mail.{url}")
        
        # Add path variations
        augmented.append(f"{url}/login")
        augmented.append(f"{url}/account")
        
        # Add query parameters
        augmented.append(f"{url}?id=123")
        augmented.append(f"{url}?ref=spam")
    
    return augmented
```

---

## 9. DATA QUALITY CHECKS

### 9.1 Validation Functions

```python
def validate_phishing_dataset(df):
    """Validate phishing dataset quality"""
    issues = []
    
    # Check for missing values
    if df.isnull().any().any():
        issues.append("Missing values found")
    
    # Check for duplicates
    if df.duplicated().any():
        issues.append("Duplicate URLs found")
    
    # Check label balance
    label_counts = df['label'].value_counts()
    if abs(label_counts[0] - label_counts[1]) / len(df) > 0.3:
        issues.append("Imbalanced dataset")
    
    # Check URL validity
    invalid_urls = df[~df['url'].str.startswith('http')]
    if len(invalid_urls) > 0:
        issues.append(f"{len(invalid_urls)} invalid URLs")
    
    return issues

def validate_malware_dataset(df):
    """Validate malware dataset quality"""
    issues = []
    
    # Check for missing values
    if df.isnull().any().any():
        issues.append("Missing values found")
    
    # Check feature ranges
    if (df['file_size'] < 0).any():
        issues.append("Negative file sizes")
    
    if (df['num_sections'] < 0).any():
        issues.append("Negative section counts")
    
    # Check entropy range
    if (df['max_section_entropy'] < 0).any() or (df['max_section_entropy'] > 8).any():
        issues.append("Entropy values out of range")
    
    return issues
```

### 9.2 Data Statistics

```python
def generate_data_statistics(df, dataset_name):
    """Generate dataset statistics"""
    stats = {
        'dataset': dataset_name,
        'total_samples': len(df),
        'features': len(df.columns) - 1,  # Excluding label
        'missing_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'label_distribution': df['label'].value_counts().to_dict()
    }
    
    return stats
```

---

## 10. DATA COLLECTION SUMMARY

### 10.1 Dataset Requirements Matrix

| Dataset | Source | Size | Format | Preprocessing | Status |
|---------|--------|------|--------|---------------|--------|
| Phishing URLs | PhishTank, Kaggle | 100K+ | CSV | Feature extraction | Pending |
| Malware Samples | VirusShare, Kaggle | 10K+ | PE files | PE analysis | Pending |
| Network Intrusion | CICIDS2017, UNSW-NB15 | 2M+ | CSV, PCAP | Feature encoding | Pending |
| User Behavior | Synthetic, Logs | 50K+ | CSV | Feature engineering | Pending |
| Ransomware | VirusShare, CIC | 5K+ | PE files | Behavior analysis | Pending |

### 10.2 Data Collection Timeline

**Week 1-2**: Phishing URLs
- Download PhishTank dataset
- Download Kaggle datasets
- Collect legitimate URLs
- Extract features
- Preprocess and validate

**Week 3-4**: Malware Samples
- Download from VirusShare
- Download Kaggle malware datasets
- Collect benign samples
- Extract PE features
- Preprocess and validate

**Week 5-6**: Network Intrusion
- Download CICIDS2017
- Download UNSW-NB15
- Extract network features
- Preprocess and validate

**Week 7**: User Behavior
- Generate synthetic data
- Collect system logs
- Extract behavior features
- Preprocess and validate

**Week 8**: Ransomware
- Download ransomware samples
- Collect behavior logs
- Extract ransomware features
- Preprocess and validate

### 10.3 Storage Requirements

Estimated storage requirements:
- Phishing URLs: ~50 MB
- Malware Samples: ~10 GB
- Network Intrusion: ~50 GB
- User Behavior: ~100 MB
- Ransomware: ~5 GB

**Total**: ~65 GB

---

## 11. ETHICAL AND LEGAL CONSIDERATIONS

### 11.1 Data Usage Ethics

- **Research Purpose Only**: Use datasets only for research and educational purposes
- **No Distribution**: Do not redistribute malware samples
- **Safe Environment**: Handle malware in isolated environment
- **User Privacy**: Anonymize user behavior data
- **Attribution**: Cite dataset sources in publications

### 11.2 Legal Compliance

- **GDPR**: Ensure compliance for EU user data
- **CCPA**: Comply with California privacy laws
- **Terms of Use**: Follow dataset provider terms
- **Intellectual Property**: Respect software licenses

### 11.3 Security Measures

- **Isolated Environment**: Use virtual machines for malware analysis
- **Network Isolation**: Disconnect from network during analysis
- **Access Control**: Restrict access to sensitive datasets
- **Encryption**: Encrypt stored datasets
- **Backup**: Maintain secure backups

---

## 12. CONCLUSION

This document provides a comprehensive guide for collecting and preprocessing datasets for the AI-Powered Digital Bodyguard system. The datasets cover all required ML models:

- **Phishing Detection**: 100K+ URLs from PhishTank and Kaggle
- **Malware Detection**: 10K+ samples from VirusShare and Kaggle
- **Network Intrusion**: 2M+ records from CICIDS2017 and UNSW-NB15
- **Behavior Analysis**: 50K+ sessions from synthetic data and logs
- **Ransomware Detection**: 5K+ samples from VirusShare and CIC

**Next Steps:**
1. Begin data collection following the timeline
2. Implement preprocessing pipelines
3. Validate dataset quality
4. Proceed to Phase 6: Machine Learning Pipeline

---

## APPENDICES

### Appendix A: Dataset Download Scripts

```python
# download_datasets.py
import requests
import pandas as pd
import os

def download_phishtank():
    """Download PhishTank dataset"""
    url = "https://data.phishtank.com/data/online-valid.csv"
    response = requests.get(url)
    
    os.makedirs('data/phishing/raw', exist_ok=True)
    with open('data/phishing/raw/phishtank.csv', 'wb') as f:
        f.write(response.content)
    print("PhishTank dataset downloaded")

def download_kaggle_dataset(dataset_name):
    """Download Kaggle dataset"""
    import kaggle
    kaggle.api.dataset_download_files(dataset_name, path='data/', unzip=True)
    print(f"{dataset_name} downloaded")

if __name__ == "__main__":
    download_phishtank()
    # download_kaggle_dataset("amananandrai/phishing-site-urls")
```

### Appendix B: Feature Extraction Scripts

```python
# extract_features.py
import pandas as pd
from urllib.parse import urlparse
import tldextract

def extract_all_phishing_features(input_file, output_file):
    """Extract features from phishing dataset"""
    df = pd.read_csv(input_file)
    
    features = df['url'].apply(extract_url_features).apply(pd.Series)
    df = pd.concat([df, features], axis=1)
    
    df.to_csv(output_file, index=False)
    print(f"Features extracted to {output_file}")

if __name__ == "__main__":
    extract_all_phishing_features(
        'data/phishing/raw/phishtank.csv',
        'data/phishing/processed/phishing_features.csv'
    )
```

### Appendix C: Data Validation Script

```python
# validate_data.py
import pandas as pd

def validate_all_datasets():
    """Validate all datasets"""
    datasets = {
        'phishing': 'data/phishing/processed/phishing_features.csv',
        'malware': 'data/malware/processed/malware_features.csv',
        'network': 'data/network/processed/network_features.csv',
        'behavior': 'data/behavior/processed/behavior_features.csv'
    }
    
    for name, path in datasets.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            if name == 'phishing':
                issues = validate_phishing_dataset(df)
            elif name == 'malware':
                issues = validate_malware_dataset(df)
            
            print(f"{name}: {len(issues)} issues")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"{name}: File not found")

if __name__ == "__main__":
    validate_all_datasets()
```

### Appendix D: Dataset Sources Summary

| Dataset | URL | License | Access |
|---------|-----|---------|--------|
| PhishTank | https://www.phishtank.com/ | CC BY-SA | Free |
| Kaggle Phishing | https://www.kaggle.com/ | Various | Free |
| VirusShare | https://virusshare.com/ | Research | Registration |
| CICIDS2017 | https://www.unb.ca/cic/datasets/ids-2017.html | Research | Registration |
| UNSW-NB15 | https://www.unsw.adfa.edu.au/unsw-canberra/cyber/ | Research | Free |
| KDD Cup 1999 | http://kdd.ics.uci.edu/ | Public | Free |
| NSL-KDD | https://www.unb.ca/cic/datasets/nsl.html | Research | Free |
| MalwareBazaar | https://bazaar.abuse.ch/ | Research | Free |
