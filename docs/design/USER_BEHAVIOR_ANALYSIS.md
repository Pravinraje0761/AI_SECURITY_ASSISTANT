# User Behavior Analysis
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. MODEL OVERVIEW

This document provides complete implementation details for the User Behavior Analysis Model, including training code, testing code, and API integration.

### 1.1 Model Purpose

Detect anomalous user behavior patterns using machine learning:
- Login pattern analysis
- File access pattern monitoring
- Browser history analysis
- Network activity profiling
- Anomaly detection using unsupervised learning

### 1.2 Anomaly Detection Algorithms

- **Isolation Forest**: Tree-based anomaly detection
- **One-Class SVM**: Support vector machine for anomaly detection
- **Autoencoder**: Neural network for reconstruction-based anomaly detection

### 1.3 Performance Targets

- **Accuracy**: > 90%
- **Precision**: > 85%
- **Recall**: > 88%
- **F1 Score**: > 86%
- **ROC-AUC**: > 0.92

---

## 2. BEHAVIOR FEATURE EXTRACTION

### 2.1 Behavior Feature Extractor

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

class BehaviorFeatureExtractor:
    """Extract features from user behavior data"""
    
    def __init__(self):
        self.typical_login_hours = [8, 9, 18, 19]
        self.typical_session_duration = (2, 8)
    
    def extract_features(self, behavior_data):
        """Extract all features from behavior data"""
        features = {}
        
        try:
            features.update(self._extract_temporal_features(behavior_data))
            features.update(self._extract_login_features(behavior_data))
            features.update(self._extract_file_access_features(behavior_data))
            features.update(self._extract_browser_features(behavior_data))
            features.update(self._extract_network_features(behavior_data))
            features.update(self._extract_session_features(behavior_data))
        except Exception as e:
            print(f"Error extracting features: {e}")
            features = self._get_default_features()
        
        return features
    
    def _extract_temporal_features(self, data):
        """Extract temporal features"""
        features = {}
        timestamp = data.get('timestamp', datetime.now())
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        
        features['login_hour'] = timestamp.hour
        features['login_day_of_week'] = timestamp.weekday()
        features['is_weekend'] = 1 if timestamp.weekday() >= 5 else 0
        features['is_night'] = 1 if timestamp.hour < 6 or timestamp.hour > 22 else 0
        features['is_typical_hour'] = 1 if timestamp.hour in self.typical_login_hours else 0
        
        return features
    
    def _extract_login_features(self, data):
        """Extract login-related features"""
        features = {}
        features['login_attempts'] = data.get('login_attempts', 1)
        features['failed_login_attempts'] = data.get('failed_login_attempts', 0)
        features['login_location_changed'] = data.get('login_location_changed', 0)
        features['login_device_changed'] = data.get('login_device_changed', 0)
        features['login_ip_changed'] = data.get('login_ip_changed', 0)
        
        return features
    
    def _extract_file_access_features(self, data):
        """Extract file access features"""
        features = {}
        file_access_count = data.get('file_access_count', 0)
        features['file_access_count'] = file_access_count
        features['files_per_hour'] = file_access_count / max(data.get('session_duration', 1), 1)
        features['suspicious_files_accessed'] = data.get('suspicious_files_accessed', 0)
        features['suspicious_file_ratio'] = features['suspicious_files_accessed'] / max(file_access_count, 1)
        features['sensitive_dir_access'] = data.get('sensitive_dir_access', 0)
        
        return features
    
    def _extract_browser_features(self, data):
        """Extract browser activity features"""
        features = {}
        sites_visited = data.get('sites_visited', 0)
        features['sites_visited'] = sites_visited
        features['sites_per_hour'] = sites_visited / max(data.get('session_duration', 1), 1)
        features['suspicious_sites_visited'] = data.get('suspicious_sites_visited', 0)
        features['downloads'] = data.get('downloads', 0)
        
        return features
    
    def _extract_network_features(self, data):
        """Extract network activity features"""
        features = {}
        network_activity_mb = data.get('network_activity_mb', 0)
        features['network_activity_mb'] = network_activity_mb
        features['network_per_hour'] = network_activity_mb / max(data.get('session_duration', 1), 1)
        features['unique_endpoints'] = data.get('unique_endpoints', 0)
        features['suspicious_endpoints'] = data.get('suspicious_endpoints', 0)
        
        return features
    
    def _extract_session_features(self, data):
        """Extract session features"""
        features = {}
        session_duration = data.get('session_duration', 0)
        features['session_duration'] = session_duration
        features['is_long_session'] = 1 if session_duration > 10 else 0
        features['is_short_session'] = 1 if session_duration < 0.5 else 0
        
        return features
    
    def _get_default_features(self):
        """Return default features"""
        return {
            'login_hour': 12,
            'login_day_of_week': 0,
            'is_weekend': 0,
            'is_night': 0,
            'is_typical_hour': 1,
            'login_attempts': 1,
            'failed_login_attempts': 0,
            'login_location_changed': 0,
            'login_device_changed': 0,
            'login_ip_changed': 0,
            'file_access_count': 0,
            'files_per_hour': 0,
            'suspicious_files_accessed': 0,
            'suspicious_file_ratio': 0,
            'sensitive_dir_access': 0,
            'sites_visited': 0,
            'sites_per_hour': 0,
            'suspicious_sites_visited': 0,
            'downloads': 0,
            'network_activity_mb': 0,
            'network_per_hour': 0,
            'unique_endpoints': 0,
            'suspicious_endpoints': 0,
            'session_duration': 0,
            'is_long_session': 0,
            'is_short_session': 0
        }
```

---

## 3. BASELINE MANAGEMENT

### 3.1 Baseline Manager

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class BaselineManager:
    """Manage user behavior baselines"""
    
    def __init__(self):
        self.baselines = {}
    
    def establish_baseline(self, user_id, behavior_data_list):
        """Establish baseline for a user"""
        if not behavior_data_list:
            return None
        
        df = pd.DataFrame(behavior_data_list)
        
        baseline = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'sample_count': len(df),
            'statistics': {}
        }
        
        # Calculate statistics for each feature
        for column in df.columns:
            if df[column].dtype in [np.int64, np.float64]:
                baseline['statistics'][column] = {
                    'mean': float(df[column].mean()),
                    'std': float(df[column].std()),
                    'min': float(df[column].min()),
                    'max': float(df[column].max()),
                    'median': float(df[column].median()),
                    'q25': float(df[column].quantile(0.25)),
                    'q75': float(df[column].quantile(0.75))
                }
        
        self.baselines[user_id] = baseline
        return baseline
    
    def update_baseline(self, user_id, new_behavior_data):
        """Update baseline with new data"""
        if user_id not in self.baselines:
            return self.establish_baseline(user_id, new_behavior_data)
        
        # Combine old and new data
        old_data = self.baselines[user_id].get('data', [])
        combined_data = old_data + new_behavior_data
        
        # Keep only last 1000 samples
        if len(combined_data) > 1000:
            combined_data = combined_data[-1000:]
        
        return self.establish_baseline(user_id, combined_data)
    
    def compare_to_baseline(self, user_id, current_behavior):
        """Compare current behavior to baseline"""
        if user_id not in self.baselines:
            return None
        
        baseline = self.baselines[user_id]
        statistics = baseline['statistics']
        
        deviations = {}
        
        for feature, value in current_behavior.items():
            if feature in statistics:
                stats = statistics[feature]
                mean = stats['mean']
                std = stats['std']
                
                if std > 0:
                    z_score = abs((value - mean) / std)
                    deviations[feature] = {
                        'value': value,
                        'mean': mean,
                        'std': std,
                        'z_score': z_score,
                        'is_anomalous': z_score > 3
                    }
        
        return deviations
    
    def get_baseline_drift(self, user_id):
        """Calculate baseline drift over time"""
        if user_id not in self.baselines:
            return 0
        
        baseline = self.baselines[user_id]
        age_days = (datetime.now() - baseline['created_at']).days
        
        # Drift increases with age
        drift = min(age_days / 30.0, 1.0)  # Max drift after 30 days
        
        return drift
```

---

## 4. MODEL TRAINING

### 4.1 Training Pipeline

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import os
import tensorflow as tf
from tensorflow import keras

class BehaviorModelTrainer:
    """Train behavior anomaly detection models"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.extractor = BehaviorFeatureExtractor()
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = None
    
    def load_data(self):
        """Load behavior dataset"""
        df = pd.read_csv(self.data_path)
        print(f"Loaded {len(df)} samples")
        return df
    
    def prepare_features(self, df):
        """Extract features from behavior data"""
        print("Extracting features...")
        
        features_list = []
        
        for idx, row in df.iterrows():
            behavior_data = row.to_dict()
            features = self.extractor.extract_features(behavior_data)
            features_list.append(features)
        
        features_df = pd.DataFrame(features_list)
        
        # Combine with labels
        df = pd.concat([df.reset_index(drop=True), features_df], axis=1)
        
        # Select numerical features
        numerical_features = [
            'login_hour', 'login_day_of_week', 'is_weekend', 'is_night',
            'is_typical_hour', 'login_attempts', 'failed_login_attempts',
            'login_location_changed', 'login_device_changed', 'login_ip_changed',
            'file_access_count', 'files_per_hour', 'suspicious_files_accessed',
            'suspicious_file_ratio', 'sensitive_dir_access', 'sites_visited',
            'sites_per_hour', 'suspicious_sites_visited', 'downloads',
            'network_activity_mb', 'network_per_hour', 'unique_endpoints',
            'suspicious_endpoints', 'session_duration', 'is_long_session',
            'is_short_session'
        ]
        
        # Ensure all features exist
        for feature in numerical_features:
            if feature not in df.columns:
                df[feature] = 0
        
        X = df[numerical_features]
        y = df['label'] if 'label' in df.columns else None
        
        self.feature_names = numerical_features
        
        return X, y
    
    def split_data(self, X, y=None):
        """Split data into train, validation, test sets"""
        if y is not None:
            X_train, X_temp, y_train, y_temp = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=y
            )
            X_val, X_test, y_val, y_test = train_test_split(
                X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
            )
            print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
            return X_train, X_val, X_test, y_train, y_val, y_test
        else:
            # For unsupervised learning, just split X
            X_train, X_temp = train_test_split(X, test_size=0.3, random_state=42)
            X_val, X_test = train_test_split(X_temp, test_size=0.5, random_state=42)
            print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
            return X_train, X_val, X_test, None, None, None
    
    def scale_features(self, X_train, X_val, X_test):
        """Scale features"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_val_scaled, X_test_scaled
    
    def train_isolation_forest(self, X_train):
        """Train Isolation Forest model"""
        print("Training Isolation Forest...")
        
        iso_forest = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        iso_forest.fit(X_train)
        self.models['isolation_forest'] = iso_forest
        print("Isolation Forest trained")
        return iso_forest
    
    def train_one_class_svm(self, X_train):
        """Train One-Class SVM model"""
        print("Training One-Class SVM...")
        
        svm = OneClassSVM(
            kernel='rbf',
            gamma='scale',
            nu=0.1
        )
        
        svm.fit(X_train)
        self.models['one_class_svm'] = svm
        print("One-Class SVM trained")
        return svm
    
    def train_autoencoder(self, X_train):
        """Train Autoencoder model"""
        print("Training Autoencoder...")
        
        input_dim = X_train.shape[1]
        
        # Build autoencoder
        encoder = keras.Sequential([
            keras.layers.Dense(32, activation='relu', input_shape=(input_dim,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(8, activation='relu')  # Bottleneck
        ])
        
        decoder = keras.Sequential([
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(input_dim, activation='sigmoid')
        ])
        
        autoencoder = keras.Sequential([encoder, decoder])
        
        autoencoder.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        # Train
        history = autoencoder.fit(
            X_train, X_train,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.models['autoencoder'] = autoencoder
        print("Autoencoder trained")
        return autoencoder
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        if model_name == 'autoencoder':
            # For autoencoder, use reconstruction error
            reconstructions = model.predict(X_test)
            mse = np.mean(np.power(X_test - reconstructions, 2), axis=1)
            threshold = np.percentile(mse, 95)
            y_pred = (mse > threshold).astype(int)
        else:
            # For Isolation Forest and One-Class SVM
            y_pred = model.predict(X_test)
            y_pred = (y_pred == -1).astype(int)  # Convert -1 to 1 (anomaly)
        
        if y_test is not None:
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1_score': f1_score(y_test, y_pred, zero_division=0)
            }
            
            print(f"\n{model_name} Metrics:")
            print(f"Accuracy: {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall: {metrics['recall']:.4f}")
            print(f"F1 Score: {metrics['f1_score']:.4f}")
            
            return metrics
        else:
            print(f"\n{model_name} trained (unsupervised)")
            return {}
    
    def save_models(self, output_dir):
        """Save trained models and scaler"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save sklearn models
        for model_name, model in self.models.items():
            if model_name != 'autoencoder':
                joblib.dump(model, f"{output_dir}/{model_name}.pkl")
        
        # Save autoencoder
        if 'autoencoder' in self.models:
            self.models['autoencoder'].save(f"{output_dir}/autoencoder.h5")
        
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
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = self.split_data(X, y)
        
        # Scale features
        X_train_scaled, X_val_scaled, X_test_scaled = self.scale_features(X_train, X_val, X_test)
        
        # Train models
        self.train_isolation_forest(X_train_scaled)
        self.train_one_class_svm(X_train_scaled)
        self.train_autoencoder(X_train_scaled)
        
        # Evaluate models
        results = {}
        for model_name, model in self.models.items():
            results[model_name] = self.evaluate_model(model, X_test_scaled, y_test, model_name)
        
        # Save models
        self.save_models('models/behavior')
        
        return results
```

---

## 5. MODEL TESTING

### 5.1 Testing Pipeline

```python
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from behavior_feature_extractor import BehaviorFeatureExtractor
from baseline_manager import BaselineManager

class BehaviorModelTester:
    """Test behavior anomaly detection models"""
    
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.models = {}
        self.scaler = None
        self.feature_names = None
        self.extractor = BehaviorFeatureExtractor()
        self.baseline_manager = BaselineManager()
        
    def load_models(self):
        """Load trained models"""
        print("Loading models...")
        
        # Load sklearn models
        self.models['isolation_forest'] = joblib.load(f"{self.model_dir}/isolation_forest.pkl")
        self.models['one_class_svm'] = joblib.load(f"{self.model_dir}/one_class_svm.pkl")
        
        # Load autoencoder
        import tensorflow as tf
        self.models['autoencoder'] = tf.keras.models.load_model(f"{self.model_dir}/autoencoder.h5")
        
        # Load scaler
        self.scaler = joblib.load(f"{self.model_dir}/scaler.pkl")
        
        # Load feature names
        self.feature_names = joblib.load(f"{self.model_dir}/feature_names.pkl")
        
        print("Models loaded")
    
    def prepare_test_behavior(self, behavior_data):
        """Prepare behavior data for prediction"""
        # Extract features
        features = self.extractor.extract_features(behavior_data)
        
        # Create DataFrame
        df = pd.DataFrame([features])
        
        # Select features
        X = df[self.feature_names]
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def predict_behavior(self, behavior_data, user_id=None):
        """Predict if behavior is anomalous"""
        X = self.prepare_test_behavior(behavior_data)
        
        predictions = {}
        
        # Isolation Forest
        iso_pred = self.models['isolation_forest'].predict(X)[0]
        iso_score = self.models['isolation_forest'].score_samples(X)[0]
        predictions['isolation_forest'] = {
            'prediction': int(iso_pred == -1),
            'anomaly_score': float(-iso_score)  # Negative for anomalies
        }
        
        # One-Class SVM
        svm_pred = self.models['one_class_svm'].predict(X)[0]
        svm_score = self.models['one_class_svm'].score_samples(X)[0]
        predictions['one_class_svm'] = {
            'prediction': int(svm_pred == -1),
            'anomaly_score': float(-svm_score)
        }
        
        # Autoencoder
        reconstruction = self.models['autoencoder'].predict(X)[0]
        mse = np.mean(np.power(X[0] - reconstruction, 2))
        predictions['autoencoder'] = {
            'prediction': int(mse > 0.1),  # Threshold
            'anomaly_score': float(mse)
        }
        
        # Ensemble prediction
        preds = [v['prediction'] for v in predictions.values()]
        ensemble_pred = 1 if sum(preds) >= 2 else 0
        
        # Average anomaly score
        avg_score = np.mean([v['anomaly_score'] for v in predictions.values()])
        
        predictions['ensemble'] = {
            'prediction': ensemble_pred,
            'anomaly_score': avg_score
        }
        
        # Compare to baseline if user_id provided
        if user_id:
            baseline_comparison = self.baseline_manager.compare_to_baseline(user_id, behavior_data)
            predictions['baseline_comparison'] = baseline_comparison
        
        return predictions
    
    def evaluate_on_test_set(self, test_data_path):
        """Evaluate models on test dataset"""
        print("Evaluating on test set...")
        
        # Load test data
        df = pd.read_csv(test_data_path)
        
        # Prepare features
        X_list = []
        for idx, row in df.iterrows():
            behavior_data = row.to_dict()
            features = self.extractor.extract_features(behavior_data)
            X_list.append(features)
        
        X_df = pd.DataFrame(X_list)
        
        # Select features
        X = X_df[self.feature_names]
        y = df['label'] if 'label' in df.columns else None
        
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Evaluate each model
        results = {}
        for model_name, model in self.models.items():
            if model_name == 'autoencoder':
                reconstructions = model.predict(X_scaled)
                mse = np.mean(np.power(X_scaled - reconstructions, 2), axis=1)
                threshold = np.percentile(mse, 95)
                y_pred = (mse > threshold).astype(int)
            else:
                y_pred = model.predict(X_scaled)
                y_pred = (y_pred == -1).astype(int)
            
            if y is not None:
                metrics = {
                    'accuracy': accuracy_score(y, y_pred),
                    'precision': precision_score(y, y_pred, zero_division=0),
                    'recall': recall_score(y, y_pred, zero_division=0),
                    'f1_score': f1_score(y, y_pred, zero_division=0)
                }
                
                results[model_name] = metrics
                print(f"\n{model_name}:")
                print(f"Accuracy: {metrics['accuracy']:.4f}")
                print(f"Precision: {metrics['precision']:.4f}")
                print(f"Recall: {metrics['recall']:.4f}")
                print(f"F1 Score: {metrics['f1_score']:.4f}")
        
        return results
```

---

## 6. API INTEGRATION

### 6.1 FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import joblib
import pandas as pd
import numpy as np
from behavior_model_tester import BehaviorModelTester
from datetime import datetime

app = FastAPI(title="User Behavior Analysis API")

# Initialize model
model_tester = BehaviorModelTester('models/behavior')
model_tester.load_models()

class BehaviorData(BaseModel):
    timestamp: str
    login_attempts: int = 1
    failed_login_attempts: int = 0
    login_location_changed: int = 0
    login_device_changed: int = 0
    login_ip_changed: int = 0
    file_access_count: int = 0
    suspicious_files_accessed: int = 0
    sensitive_dir_access: int = 0
    sites_visited: int = 0
    suspicious_sites_visited: int = 0
    downloads: int = 0
    network_activity_mb: float = 0
    unique_endpoints: int = 0
    suspicious_endpoints: int = 0
    session_duration: float = 0

class BehaviorAnalysisResponse(BaseModel):
    user_id: Optional[str]
    is_anomalous: bool
    anomaly_score: float
    model_predictions: dict
    baseline_comparison: Optional[dict]
    timestamp: str

@app.post("/api/v1/behavior/analyze", response_model=BehaviorAnalysisResponse)
async def analyze_behavior(behavior: BehaviorData, user_id: Optional[str] = None):
    """Analyze user behavior for anomalies"""
    try:
        # Convert to dict
        behavior_dict = behavior.dict()
        
        # Get predictions
        predictions = model_tester.predict_behavior(behavior_dict, user_id)
        
        # Get ensemble result
        ensemble = predictions['ensemble']
        
        return BehaviorAnalysisResponse(
            user_id=user_id,
            is_anomalous=ensemble['prediction'] == 1,
            anomaly_score=ensemble['anomaly_score'],
            model_predictions=predictions,
            baseline_comparison=predictions.get('baseline_comparison'),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/behavior/baseline/{user_id}")
async def update_baseline(user_id: str, behavior_data: list[BehaviorData]):
    """Update user behavior baseline"""
    try:
        behavior_list = [b.dict() for b in behavior_data]
        baseline = model_tester.baseline_manager.update_baseline(user_id, behavior_list)
        return {"user_id": user_id, "baseline_updated": True, "sample_count": baseline['sample_count']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/behavior/stats")
async def get_behavior_stats():
    """Get behavior analysis statistics"""
    return {
        "model_count": len(model_tester.models),
        "models": list(model_tester.models.keys()),
        "feature_count": len(model_tester.feature_names),
        "baseline_count": len(model_tester.baseline_manager.baselines)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

---

## 7. COMPLETE IMPLEMENTATION

### 7.1 Main Application

```python
# behavior_analyzer.py
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from behavior_model_trainer import BehaviorModelTrainer
from behavior_model_tester import BehaviorModelTester

def main():
    print("AI-Powered Digital Bodyguard - User Behavior Analysis")
    print("=" * 60)
    
    # Check if models exist
    model_dir = 'models/behavior'
    if not os.path.exists(model_dir):
        print("Models not found. Training new models...")
        trainer = BehaviorModelTrainer('data/behavior/processed/behavior_features.csv')
        results = trainer.train_pipeline()
        print("Training completed!")
    else:
        print("Loading existing models...")
    
    # Initialize tester
    tester = BehaviorModelTester(model_dir)
    tester.load_models()
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Analyze behavior")
        print("2. Update baseline")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            user_id = input("Enter user ID (optional, press Enter to skip): ") or None
            
            behavior_data = {
                'timestamp': datetime.now().isoformat(),
                'login_attempts': int(input("Login attempts: ") or 1),
                'failed_login_attempts': int(input("Failed login attempts: ") or 0),
                'login_location_changed': int(input("Location changed (0/1): ") or 0),
                'login_device_changed': int(input("Device changed (0/1): ") or 0),
                'login_ip_changed': int(input("IP changed (0/1): ") or 0),
                'file_access_count': int(input("File access count: ") or 0),
                'suspicious_files_accessed': int(input("Suspicious files accessed: ") or 0),
                'sensitive_dir_access': int(input("Sensitive dir access (0/1): ") or 0),
                'sites_visited': int(input("Sites visited: ") or 0),
                'suspicious_sites_visited': int(input("Suspicious sites visited: ") or 0),
                'downloads': int(input("Downloads: ") or 0),
                'network_activity_mb': float(input("Network activity (MB): ") or 0),
                'unique_endpoints': int(input("Unique endpoints: ") or 0),
                'suspicious_endpoints': int(input("Suspicious endpoints: ") or 0),
                'session_duration': float(input("Session duration (hours): ") or 0)
            }
            
            predictions = tester.predict_behavior(behavior_data, user_id)
            
            print(f"\nIs Anomalous: {predictions['ensemble']['prediction'] == 1}")
            print(f"Anomaly Score: {predictions['ensemble']['anomaly_score']:.4f}")
            
            if predictions.get('baseline_comparison'):
                print("Baseline Comparison:")
                for feature, comp in predictions['baseline_comparison'].items():
                    if comp['is_anomalous']:
                        print(f"  {feature}: Z-score = {comp['z_score']:.2f}")
        
        elif choice == '2':
            user_id = input("Enter user ID: ")
            print("Enter behavior data (press Enter to finish):")
            
            behavior_list = []
            while True:
                behavior_data = {
                    'timestamp': datetime.now().isoformat(),
                    'login_attempts': 1,
                    'failed_login_attempts': 0,
                    'file_access_count': 0,
                    'sites_visited': 0,
                    'network_activity_mb': 0,
                    'unique_endpoints': 0,
                    'session_duration': 1
                }
                behavior_list.append(behavior_data)
                
                if input("Add more? (y/n): ").lower() != 'y':
                    break
            
            baseline = tester.baseline_manager.update_baseline(user_id, behavior_list)
            print(f"Baseline updated with {baseline['sample_count']} samples")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
```

### 7.2 Requirements File

```txt
# requirements_behavior.txt
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
tensorflow>=2.14.0
joblib>=1.3.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
```

---

## 8. DEPLOYMENT

### 8.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_behavior.txt .
RUN pip install --no-cache-dir -r requirements_behavior.txt

# Copy application code
COPY behavior_analyzer.py .
COPY behavior_model_trainer.py .
COPY behavior_model_tester.py .
COPY behavior_feature_extractor.py .
COPY baseline_manager.py .

# Copy models
COPY models/behavior/ ./models/behavior/

# Expose port
EXPOSE 8002

# Run application
CMD ["uvicorn", "behavior_analyzer:app", "--host", "0.0.0.0", "--port", "8002"]
```

### 8.2 Docker Compose

```yaml
version: '3.8'

services:
  behavior-api:
    build: .
    ports:
      - "8002:8002"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
```

---

## 9. CONCLUSION

This document provides complete implementation for the User Behavior Analysis Model including:

- **Feature Extraction**: 25+ behavior features (temporal, login, file access, browser, network, session)
- **Baseline Management**: Statistical baseline establishment and drift detection
- **Model Training**: Isolation Forest, One-Class SVM, Autoencoder
- **Model Testing**: Evaluation metrics and validation
- **API Integration**: FastAPI REST API for behavior analysis
- **Complete Application**: Interactive CLI for behavior analysis

**Next Steps:**
1. Collect behavior dataset
2. Train models using provided pipeline
3. Evaluate performance
4. Deploy API using Docker
5. Integrate with main system

---

## APPENDICES

### Appendix A: Synthetic Data Generation

```python
def generate_synthetic_behavior_data(num_samples=1000):
    """Generate synthetic behavior data"""
    import random
    from datetime import datetime, timedelta
    
    data = []
    
    for _ in range(num_samples):
        # Normal behavior (90%)
        if random.random() < 0.9:
            behavior = {
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                'login_attempts': random.randint(1, 3),
                'failed_login_attempts': random.randint(0, 1),
                'login_location_changed': 0,
                'login_device_changed': 0,
                'login_ip_changed': 0,
                'file_access_count': random.randint(10, 50),
                'suspicious_files_accessed': 0,
                'sensitive_dir_access': 0,
                'sites_visited': random.randint(20, 100),
                'suspicious_sites_visited': 0,
                'downloads': random.randint(0, 5),
                'network_activity_mb': random.uniform(100, 500),
                'unique_endpoints': random.randint(5, 20),
                'suspicious_endpoints': 0,
                'session_duration': random.uniform(2, 8),
                'label': 0
            }
        else:
            # Anomalous behavior (10%)
            behavior = {
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                'login_attempts': random.randint(5, 10),
                'failed_login_attempts': random.randint(3, 8),
                'login_location_changed': 1,
                'login_device_changed': 1,
                'login_ip_changed': 1,
                'file_access_count': random.randint(100, 200),
                'suspicious_files_accessed': random.randint(5, 20),
                'sensitive_dir_access': 1,
                'sites_visited': random.randint(200, 300),
                'suspicious_sites_visited': random.randint(10, 30),
                'downloads': random.randint(20, 50),
                'network_activity_mb': random.uniform(1000, 2000),
                'unique_endpoints': random.randint(50, 100),
                'suspicious_endpoints': random.randint(10, 30),
                'session_duration': random.uniform(10, 15),
                'label': 1
            }
        
        data.append(behavior)
    
    return pd.DataFrame(data)
```

### Appendix B: Model Comparison

```python
def compare_models(results):
    """Compare model performance"""
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    
    comparison = {}
    for metric in metrics:
        comparison[metric] = [results[model].get(metric, 0) for model in models]
    
    df = pd.DataFrame(comparison, index=models)
    print(df)
```
