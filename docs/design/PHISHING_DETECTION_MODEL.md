# Phishing Detection Model
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. MODEL OVERVIEW

This document provides complete implementation details for the Phishing Detection Model, including training code, testing code, and API integration.

### 1.1 Model Purpose

Detect phishing URLs using machine learning algorithms with the following approach:
- Extract features from URLs
- Train ML models on labeled phishing/legitimate URLs
- Predict phishing probability for new URLs
- Integrate with VirusTotal for enhanced detection

### 1.2 Algorithms Used

- **Random Forest**: Ensemble method with decision trees
- **XGBoost**: Gradient boosting framework
- **LightGBM**: Light gradient boosting machine

### 1.3 Performance Targets

- **Accuracy**: > 95%
- **Precision**: > 93%
- **Recall**: > 92%
- **F1 Score**: > 92%
- **ROC-AUC**: > 0.98

---

## 2. FEATURE EXTRACTION

### 2.1 URL Feature Extractor

```python
import re
from urllib.parse import urlparse
import tldextract
import whois
import ssl
import socket
from datetime import datetime
import numpy as np

class URLFeatureExtractor:
    """Extract features from URLs for phishing detection"""
    
    def __init__(self):
        self.suspicious_tlds = ['.xyz', '.top', '.zip', '.tk', '.ml', '.ga', '.cf']
        self.suspicious_keywords = ['login', 'signin', 'account', 'verify', 'bank', 'secure', 'update']
    
    def extract_features(self, url):
        """Extract all features from a URL"""
        features = {}
        
        try:
            parsed = urlparse(url)
            ext = tldextract.extract(url)
            
            # Basic URL features
            features['url_length'] = len(url)
            features['domain_length'] = len(ext.domain)
            features['path_length'] = len(parsed.path)
            features['query_length'] = len(parsed.query)
            
            # Character counts
            features['num_dots'] = url.count('.')
            features['num_hyphens'] = url.count('-')
            features['num_underscores'] = url.count('_')
            features['num_digits'] = sum(c.isdigit() for c in url)
            features['num_special_chars'] = sum(not c.isalnum() and c not in '.-_' for c in url)
            
            # Subdomain features
            subdomains = ext.subdomain.split('.') if ext.subdomain else []
            features['subdomain_count'] = len(subdomains)
            features['has_subdomain'] = 1 if ext.subdomain else 0
            features['subdomain_length'] = len(ext.subdomain) if ext.subdomain else 0
            
            # Protocol features
            features['has_https'] = 1 if parsed.scheme == 'https' else 0
            features['has_http'] = 1 if parsed.scheme == 'http' else 0
            
            # IP address in URL
            features['has_ip_address'] = 1 if self._is_ip_address(parsed.netloc) else 0
            
            # TLD features
            features['tld'] = ext.suffix
            features['tld_length'] = len(ext.suffix)
            features['is_suspicious_tld'] = 1 if ext.suffix in self.suspicious_tlds else 0
            
            # Domain features
            features['domain'] = ext.domain
            features['domain_digit_count'] = sum(c.isdigit() for c in ext.domain)
            features['domain_hyphen_count'] = ext.domain.count('-')
            
            # Path features
            features['path_depth'] = parsed.path.count('/')
            features['has_at_symbol'] = 1 if '@' in url else 0
            
            # Query features
            features['has_query'] = 1 if parsed.query else 0
            features['query_param_count'] = parsed.query.count('&') + 1 if parsed.query else 0
            
            # Suspicious keywords
            features['suspicious_keyword_count'] = sum(
                1 for keyword in self.suspicious_keywords 
                if keyword in url.lower()
            )
            
            # Port
            features['has_port'] = 1 if ':' in parsed.netloc else 0
            
            # Redirection
            features['has_redirect'] = 1 if '//' in url[8:] else 0
            
        except Exception as e:
            print(f"Error extracting features from {url}: {e}")
            # Return default features if extraction fails
            features = self._get_default_features()
        
        return features
    
    def _is_ip_address(self, hostname):
        """Check if hostname is an IP address"""
        try:
            socket.inet_aton(hostname)
            return True
        except:
            return False
    
    def _get_default_features(self):
        """Return default features for failed extraction"""
        return {
            'url_length': 0,
            'domain_length': 0,
            'path_length': 0,
            'query_length': 0,
            'num_dots': 0,
            'num_hyphens': 0,
            'num_underscores': 0,
            'num_digits': 0,
            'num_special_chars': 0,
            'subdomain_count': 0,
            'has_subdomain': 0,
            'subdomain_length': 0,
            'has_https': 0,
            'has_http': 0,
            'has_ip_address': 0,
            'tld': 'com',
            'tld_length': 3,
            'is_suspicious_tld': 0,
            'domain': '',
            'domain_digit_count': 0,
            'domain_hyphen_count': 0,
            'path_depth': 0,
            'has_at_symbol': 0,
            'has_query': 0,
            'query_param_count': 0,
            'suspicious_keyword_count': 0,
            'has_port': 0,
            'has_redirect': 0
        }
```

### 2.2 Domain Age Checker

```python
class DomainAgeChecker:
    """Check domain age using WHOIS"""
    
    def get_domain_age(self, domain):
        """Get domain age in days"""
        try:
            domain_info = whois.whois(domain)
            
            if domain_info.creation_date:
                if isinstance(domain_info.creation_date, list):
                    creation_date = domain_info.creation_date[0]
                else:
                    creation_date = domain_info.creation_date
                
                age_days = (datetime.now() - creation_date).days
                return max(0, age_days)
            else:
                return -1  # Unknown
        except Exception as e:
            print(f"Error getting domain age for {domain}: {e}")
            return -1
    
    def is_suspicious_age(self, age_days):
        """Check if domain age is suspicious (too young)"""
        return 0 <= age_days < 30  # Less than 30 days is suspicious
```

### 2.3 SSL Verifier

```python
class SSLVerifier:
    """Verify SSL certificate of a URL"""
    
    def verify_ssl(self, url):
        """Verify SSL certificate and return SSL info"""
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc.split(':')[0]
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    ssl_info = {
                        'ssl_valid': 1,
                        'issuer': cert['issuer'],
                        'subject': cert['subject'],
                        'version': cert['version'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'serial_number': cert['serialNumber']
                    }
                    
                    # Check if certificate is expired
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    ssl_info['is_expired'] = 1 if datetime.now() > not_after else 0
                    
                    return ssl_info
        except Exception as e:
            print(f"SSL verification failed for {url}: {e}")
            return {
                'ssl_valid': 0,
                'is_expired': 1,
                'issuer': None,
                'subject': None,
                'version': None,
                'not_before': None,
                'not_after': None,
                'serial_number': None
            }
```

---

## 3. MODEL TRAINING

### 3.1 Training Pipeline

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import joblib
import os
from imblearn.over_sampling import SMOTE

class PhishingModelTrainer:
    """Train phishing detection models"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.extractor = URLFeatureExtractor()
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = None
        
    def load_data(self):
        """Load phishing dataset"""
        df = pd.read_csv(self.data_path)
        print(f"Loaded {len(df)} samples")
        return df
    
    def prepare_features(self, df):
        """Extract features from URLs"""
        print("Extracting features...")
        
        # Extract features for all URLs
        features_list = []
        for url in df['url']:
            features = self.extractor.extract_features(url)
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        
        # Combine with labels
        df = pd.concat([df.reset_index(drop=True), features_df], axis=1)
        
        # Encode categorical features
        le = LabelEncoder()
        if 'tld' in df.columns:
            df['tld_encoded'] = le.fit_transform(df['tld'].astype(str))
        
        # Select numerical features
        numerical_features = [
            'url_length', 'domain_length', 'path_length', 'query_length',
            'num_dots', 'num_hyphens', 'num_underscores', 'num_digits',
            'num_special_chars', 'subdomain_count', 'has_subdomain',
            'subdomain_length', 'has_https', 'has_http', 'has_ip_address',
            'tld_length', 'is_suspicious_tld', 'domain_digit_count',
            'domain_hyphen_count', 'path_depth', 'has_at_symbol',
            'has_query', 'query_param_count', 'suspicious_keyword_count',
            'has_port', 'has_redirect', 'tld_encoded'
        ]
        
        # Ensure all features exist
        for feature in numerical_features:
            if feature not in df.columns:
                df[feature] = 0
        
        X = df[numerical_features]
        y = df['label']
        
        self.feature_names = numerical_features
        
        return X, y
    
    def balance_data(self, X, y):
        """Balance dataset using SMOTE"""
        print("Balancing dataset...")
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        print(f"Original: {len(y)} samples, Balanced: {len(y_resampled)} samples")
        return X_resampled, y_resampled
    
    def split_data(self, X, y):
        """Split data into train, validation, test sets"""
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )
        
        print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def scale_features(self, X_train, X_val, X_test):
        """Scale features"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_val_scaled, X_test_scaled
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest model"""
        print("Training Random Forest...")
        
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        rf.fit(X_train, y_train)
        self.models['random_forest'] = rf
        print("Random Forest trained")
        return rf
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost model"""
        print("Training XGBoost...")
        
        xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
        
        xgb_model.fit(X_train, y_train)
        self.models['xgboost'] = xgb_model
        print("XGBoost trained")
        return xgb_model
    
    def train_lightgbm(self, X_train, y_train):
        """Train LightGBM model"""
        print("Training LightGBM...")
        
        lgb_model = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        
        lgb_model.fit(X_train, y_train)
        self.models['lightgbm'] = lgb_model
        print("LightGBM trained")
        return lgb_model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        print(f"\n{model_name} Metrics:")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1_score']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return metrics
    
    def save_models(self, output_dir):
        """Save trained models and scaler"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            joblib.dump(model, f"{output_dir}/{model_name}.pkl")
        
        # Save scaler
        joblib.dump(self.scaler, f"{output_dir}/scaler.pkl")
        
        # Save feature names
        joblib.dump(self.feature_names, f"{output_dir}/feature_names.pkl")
        
        print(f"Models saved to {output_dir}")
    
    def train_pipeline(self):
        """Complete training pipeline"""
        # Load data
        df = self.load_data()
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Balance data
        X, y = self.balance_data(X, y)
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(X, y)
        
        # Scale features
        X_train_scaled, X_val_scaled, X_test_scaled = self.scale_features(X_train, X_val, X_test)
        
        # Train models
        self.train_random_forest(X_train_scaled, y_train)
        self.train_xgboost(X_train_scaled, y_train)
        self.train_lightgbm(X_train_scaled, y_train)
        
        # Evaluate models
        results = {}
        for model_name, model in self.models.items():
            results[model_name] = self.evaluate_model(model, X_test_scaled, y_test, model_name)
        
        # Save models
        self.save_models('models/phishing')
        
        return results
```

### 3.2 Training Script

```python
# train_phishing_model.py
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phishing_model_trainer import PhishingModelTrainer

if __name__ == "__main__":
    # Initialize trainer
    trainer = PhishingModelTrainer('data/phishing/processed/phishing_features.csv')
    
    # Run training pipeline
    results = trainer.train_pipeline()
    
    print("\nTraining completed!")
    print("Results:", results)
```

---

## 4. MODEL TESTING

### 4.1 Testing Pipeline

```python
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class PhishingModelTester:
    """Test phishing detection models"""
    
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.models = {}
        self.scaler = None
        self.feature_names = None
        self.extractor = URLFeatureExtractor()
        
    def load_models(self):
        """Load trained models"""
        print("Loading models...")
        
        # Load models
        self.models['random_forest'] = joblib.load(f"{self.model_dir}/random_forest.pkl")
        self.models['xgboost'] = joblib.load(f"{self.model_dir}/xgboost.pkl")
        self.models['lightgbm'] = joblib.load(f"{self.model_dir}/lightgbm.pkl")
        
        # Load scaler
        self.scaler = joblib.load(f"{self.model_dir}/scaler.pkl")
        
        # Load feature names
        self.feature_names = joblib.load(f"{self.model_dir}/feature_names.pkl")
        
        print("Models loaded")
    
    def prepare_test_url(self, url):
        """Prepare URL for prediction"""
        # Extract features
        features = self.extractor.extract_features(url)
        
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Encode TLD
        if 'tld' in df.columns:
            le = LabelEncoder()
            df['tld_encoded'] = le.fit_transform(df['tld'].astype(str))
        
        # Select features
        X = df[self.feature_names]
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def predict_url(self, url):
        """Predict if URL is phishing"""
        X = self.prepare_test_url(url)
        
        predictions = {}
        for model_name, model in self.models.items():
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]
            predictions[model_name] = {
                'prediction': int(pred),
                'probability': float(proba[1])
            }
        
        # Ensemble prediction (majority vote)
        preds = [v['prediction'] for v in predictions.values()]
        ensemble_pred = 1 if sum(preds) >= 2 else 0
        
        # Average probability
        avg_proba = np.mean([v['probability'] for v in predictions.values()])
        
        predictions['ensemble'] = {
            'prediction': ensemble_pred,
            'probability': avg_proba
        }
        
        return predictions
    
    def evaluate_on_test_set(self, test_data_path):
        """Evaluate models on test dataset"""
        print("Evaluating on test set...")
        
        # Load test data
        df = pd.read_csv(test_data_path)
        
        # Prepare features
        X_list = []
        for url in df['url']:
            features = self.extractor.extract_features(url)
            X_list.append(features)
        
        X_df = pd.DataFrame(X_list)
        
        # Encode TLD
        if 'tld' in X_df.columns:
            le = LabelEncoder()
            X_df['tld_encoded'] = le.fit_transform(X_df['tld'].astype(str))
        
        # Select features
        X = X_df[self.feature_names]
        y = df['label']
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Evaluate each model
        results = {}
        for model_name, model in self.models.items():
            y_pred = model.predict(X_scaled)
            y_pred_proba = model.predict_proba(X_scaled)[:, 1]
            
            metrics = {
                'accuracy': accuracy_score(y, y_pred),
                'precision': precision_score(y, y_pred),
                'recall': recall_score(y, y_pred),
                'f1_score': f1_score(y, y_pred),
                'roc_auc': roc_auc_score(y, y_pred_proba)
            }
            
            results[model_name] = metrics
            print(f"\n{model_name}:")
            print(f"Accuracy: {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall: {metrics['recall']:.4f}")
            print(f"F1 Score: {metrics['f1_score']:.4f}")
            print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        
        return results
    
    def plot_confusion_matrix(self, y_true, y_pred, model_name):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'results/{model_name}_confusion_matrix.png')
        plt.close()
    
    def plot_feature_importance(self, model, model_name):
        """Plot feature importance"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(12, 8))
            plt.title(f'Feature Importance - {model_name}')
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), [self.feature_names[i] for i in indices], rotation=90)
            plt.tight_layout()
            plt.savefig(f'results/{model_name}_feature_importance.png')
            plt.close()
```

### 4.2 Testing Script

```python
# test_phishing_model.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phishing_model_tester import PhishingModelTester

if __name__ == "__main__":
    # Initialize tester
    tester = PhishingModelTester('models/phishing')
    
    # Load models
    tester.load_models()
    
    # Test on single URL
    test_url = "http://phishing-example.com/login"
    predictions = tester.predict_url(test_url)
    
    print(f"\nPredictions for {test_url}:")
    for model_name, pred in predictions.items():
        print(f"{model_name}: {'Phishing' if pred['prediction'] == 1 else 'Legitimate'} ({pred['probability']:.4f})")
    
    # Evaluate on test set
    results = tester.evaluate_on_test_set('data/phishing/processed/test_data.csv')
    
    print("\nTesting completed!")
```

---

## 5. API INTEGRATION

### 5.1 FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import joblib
import pandas as pd
import numpy as np
from phishing_model_tester import PhishingModelTester

app = FastAPI(title="Phishing Detection API")

# Initialize model
model_tester = PhishingModelTester('models/phishing')
model_tester.load_models()

class URLRequest(BaseModel):
    url: str

class PhishingResponse(BaseModel):
    url: str
    is_phishing: bool
    probability: float
    model_predictions: dict
    features: dict

@app.post("/api/v1/scan/url", response_model=PhishingResponse)
async def scan_url(request: URLRequest):
    """Scan URL for phishing"""
    try:
        # Get predictions
        predictions = model_tester.predict_url(request.url)
        
        # Extract features
        features = model_tester.extractor.extract_features(request.url)
        
        # Get ensemble result
        ensemble = predictions['ensemble']
        
        return PhishingResponse(
            url=request.url,
            is_phishing=ensemble['prediction'] == 1,
            probability=ensemble['probability'],
            model_predictions=predictions,
            features=features
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/scan/url/batch")
async def scan_urls_batch(requests: list[URLRequest]):
    """Scan multiple URLs for phishing"""
    results = []
    for req in requests:
        try:
            predictions = model_tester.predict_url(req.url)
            ensemble = predictions['ensemble']
            results.append({
                'url': req.url,
                'is_phishing': ensemble['prediction'] == 1,
                'probability': ensemble['probability']
            })
        except Exception as e:
            results.append({
                'url': req.url,
                'error': str(e)
            })
    
    return {"results": results}

@app.get("/api/v1/phishing/stats")
async def get_phishing_stats():
    """Get phishing detection statistics"""
    return {
        "model_count": len(model_tester.models),
        "models": list(model_tester.models.keys()),
        "feature_count": len(model_tester.feature_names)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5.2 VirusTotal Integration

```python
import requests
import hashlib

class VirusTotalChecker:
    """Check URLs against VirusTotal database"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"
    
    def scan_url(self, url):
        """Submit URL for scanning"""
        headers = {
            "x-apikey": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"url": url}
        
        response = requests.post(
            f"{self.base_url}/urls",
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            analysis_id = response.json()['data']['id']
            return analysis_id
        else:
            return None
    
    def get_scan_report(self, analysis_id):
        """Get scan report"""
        headers = {"x-apikey": self.api_key}
        
        response = requests.get(
            f"{self.base_url}/analyses/{analysis_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_url_report(self, url):
        """Get existing URL report"""
        url_id = hashlib.sha256(url.encode()).hexdigest()
        headers = {"x-apikey": self.api_key}
        
        response = requests.get(
            f"{self.base_url}/urls/{url_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_reputation_score(self, url):
        """Get reputation score from VirusTotal"""
        report = self.get_url_report(url)
        
        if report and 'data' in report:
            attributes = report['data']['attributes']
            last_analysis_stats = attributes.get('last_analysis_stats', {})
            
            malicious = last_analysis_stats.get('malicious', 0)
            suspicious = last_analysis_stats.get('suspicious', 0)
            total = sum(last_analysis_stats.values())
            
            if total > 0:
                reputation_score = 1 - (malicious + suspicious) / total
            else:
                reputation_score = 0.5  # Unknown
            
            return {
                'reputation_score': reputation_score,
                'malicious_count': malicious,
                'suspicious_count': suspicious,
                'total_engines': total
            }
        
        return None
```

### 5.3 Combined Detection (ML + VirusTotal)

```python
class CombinedPhishingDetector:
    """Combine ML prediction with VirusTotal"""
    
    def __init__(self, model_dir, virustotal_api_key):
        self.ml_detector = PhishingModelTester(model_dir)
        self.ml_detector.load_models()
        self.vt_checker = VirusTotalChecker(virustotal_api_key)
    
    def detect(self, url):
        """Detect phishing using both ML and VirusTotal"""
        # Get ML prediction
        ml_predictions = self.ml_detector.predict_url(url)
        ml_score = ml_predictions['ensemble']['probability']
        
        # Get VirusTotal reputation
        vt_result = self.vt_checker.get_reputation_score(url)
        
        if vt_result:
            vt_score = vt_result['reputation_score']
            
            # Combine scores (70% ML, 30% VirusTotal)
            final_score = (ml_score * 0.7) + ((1 - vt_score) * 0.3)
            
            return {
                'url': url,
                'is_phishing': final_score > 0.5,
                'final_score': final_score,
                'ml_score': ml_score,
                'vt_score': vt_score,
                'vt_details': vt_result
            }
        else:
            # If VirusTotal fails, use only ML
            return {
                'url': url,
                'is_phishing': ml_score > 0.5,
                'final_score': ml_score,
                'ml_score': ml_score,
                'vt_score': None,
                'vt_details': None
            }
```

---

## 6. COMPLETE IMPLEMENTATION

### 6.1 Main Application

```python
# phishing_detector.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phishing_model_trainer import PhishingModelTrainer
from phishing_model_tester import PhishingModelTester
from combined_phishing_detector import CombinedPhishingDetector

def main():
    print("AI-Powered Digital Bodyguard - Phishing Detection")
    print("=" * 60)
    
    # Check if models exist
    model_dir = 'models/phishing'
    if not os.path.exists(model_dir):
        print("Models not found. Training new models...")
        trainer = PhishingModelTrainer('data/phishing/processed/phishing_features.csv')
        results = trainer.train_pipeline()
        print("Training completed!")
    else:
        print("Loading existing models...")
    
    # Initialize detector
    detector = CombinedPhishingDetector(
        model_dir=model_dir,
        virustotal_api_key='your-virustotal-api-key'
    )
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Scan a URL")
        print("2. Batch scan URLs")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            url = input("Enter URL to scan: ")
            result = detector.detect(url)
            
            print(f"\nURL: {result['url']}")
            print(f"Is Phishing: {result['is_phishing']}")
            print(f"Final Score: {result['final_score']:.4f}")
            print(f"ML Score: {result['ml_score']:.4f}")
            if result['vt_score']:
                print(f"VirusTotal Score: {result['vt_score']:.4f}")
        
        elif choice == '2':
            urls = input("Enter URLs (comma-separated): ").split(',')
            urls = [url.strip() for url in urls]
            
            for url in urls:
                result = detector.detect(url)
                print(f"{url}: {'PHISHING' if result['is_phishing'] else 'LEGITIMATE'} ({result['final_score']:.4f})")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
```

### 6.2 Requirements File

```txt
# requirements_phishing.txt
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=2.0.0
lightgbm>=4.0.0
joblib>=1.3.0
urllib3>=2.0.0
tldextract>=3.4.0
python-whois>=0.8.0
pyopenssl>=23.0.0
requests>=2.31.0
imbalanced-learn>=0.11.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
```

---

## 7. DEPLOYMENT

### 7.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_phishing.txt .
RUN pip install --no-cache-dir -r requirements_phishing.txt

# Copy application code
COPY phishing_detector.py .
COPY phishing_model_trainer.py .
COPY phishing_model_tester.py .
COPY combined_phishing_detector.py .

# Copy models
COPY models/phishing/ ./models/phishing/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "phishing_detector:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.2 Docker Compose

```yaml
version: '3.8'

services:
  phishing-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - VIRUSTOTAL_API_KEY=${VIRUSTOTAL_API_KEY}
    volumes:
      - ./models:/app/models
      - ./data:/app/data
```

---

## 8. CONCLUSION

This document provides complete implementation for the Phishing Detection Model including:

- **Feature Extraction**: Comprehensive URL feature extraction
- **Model Training**: Random Forest, XGBoost, LightGBM
- **Model Testing**: Evaluation metrics and visualization
- **API Integration**: FastAPI REST API
- **VirusTotal Integration**: Enhanced detection with external service
- **Combined Detection**: Ensemble of ML and VirusTotal

**Next Steps:**
1. Collect phishing dataset
2. Train models using provided pipeline
3. Evaluate performance
4. Deploy API using Docker
5. Integrate with main system

---

## APPENDICES

### Appendix A: Feature Importance Analysis

```python
def analyze_feature_importance(model, feature_names):
    """Analyze and display feature importance"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    print("Feature Importance Ranking:")
    for i, idx in enumerate(indices[:10]):
        print(f"{i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
```

### Appendix B: Hyperparameter Tuning

```python
def tune_random_forest(X_train, y_train):
    """Hyperparameter tuning for Random Forest"""
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestClassifier(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    return grid_search.best_estimator_
```

### Appendix C: Model Comparison

```python
def compare_models(results):
    """Compare model performance"""
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    
    comparison = {}
    for metric in metrics:
        comparison[metric] = [results[model][metric] for model in models]
    
    df = pd.DataFrame(comparison, index=models)
    print(df)
```
