"""
Configuration Manager for AI Digital Bodyguard
Handles application settings and user preferences
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "app": {
                "name": "AI Digital Bodyguard",
                "version": "1.0.0",
                "auto_start": True,
                "minimize_to_tray": True,
                "show_notifications": True,
                "sound_alerts": True
            },
            "backend": {
                "host": "127.0.0.1",
                "port": 8000,
                "api_key": ""
            },
            "monitoring": {
                "email_monitoring": True,
                "url_monitoring": True,
                "file_monitoring": True,
                "system_monitoring": True,
                "monitored_folders": [
                    os.path.expanduser("~/Downloads"),
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Documents")
                ]
            },
            "scanning": {
                "yara_rules_enabled": True,
                "virustotal_enabled": True,
                "virustotal_api_key": "",
                "ml_scanning_enabled": True
            },
            "alerts": {
                "safe_threshold": 0.3,
                "suspicious_threshold": 0.6,
                "dangerous_threshold": 0.8
            },
            "logging": {
                "level": "INFO",
                "file": "digital_bodyguard.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = yaml.safe_load(f)
                    # Merge with defaults
                    return self._merge_configs(default_config, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        
        # Create default config file
        self._save_config(default_config)
        return default_config
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Merge loaded config with defaults"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def save(self):
        """Save current configuration"""
        self._save_config(self.config)
