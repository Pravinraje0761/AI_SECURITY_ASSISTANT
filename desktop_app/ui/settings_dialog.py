"""
Settings Dialog for AI Digital Bodyguard
Configuration UI for application settings
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QCheckBox, QSpinBox, QLineEdit, QPushButton, 
    QTabWidget, QWidget, QGroupBox, QFormLayout,
    QFileDialog
)
from PyQt6.QtCore import Qt
from desktop_app.config_manager import ConfigManager

class SettingsDialog(QDialog):
    """Settings configuration dialog"""
    
    def __init__(self, config: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("AI Digital Bodyguard - Settings")
        self.setFixedSize(600, 500)
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self):
        """Setup settings UI"""
        layout = QVBoxLayout(self)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # General tab
        self.general_tab = self._create_general_tab()
        self.tabs.addTab(self.general_tab, "General")
        
        # Monitoring tab
        self.monitoring_tab = self._create_monitoring_tab()
        self.tabs.addTab(self.monitoring_tab, "Monitoring")
        
        # Scanning tab
        self.scanning_tab = self._create_scanning_tab()
        self.tabs.addTab(self.scanning_tab, "Scanning")
        
        # Alerts tab
        self.alerts_tab = self._create_alerts_tab()
        self.tabs.addTab(self.alerts_tab, "Alerts")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _create_general_tab(self) -> QWidget:
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Auto-startup
        self.auto_start_checkbox = QCheckBox("Start with Windows")
        layout.addWidget(self.auto_start_checkbox)
        
        # Minimize to tray
        self.minimize_tray_checkbox = QCheckBox("Minimize to system tray")
        layout.addWidget(self.minimize_tray_checkbox)
        
        # Show notifications
        self.notifications_checkbox = QCheckBox("Show desktop notifications")
        layout.addWidget(self.notifications_checkbox)
        
        # Sound alerts
        self.sound_alerts_checkbox = QCheckBox("Enable sound alerts")
        layout.addWidget(self.sound_alerts_checkbox)
        
        layout.addStretch()
        return widget
    
    def _create_monitoring_tab(self) -> QWidget:
        """Create monitoring settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Monitoring Options")
        group_layout = QVBoxLayout()
        
        self.email_monitoring_checkbox = QCheckBox("Email monitoring")
        group_layout.addWidget(self.email_monitoring_checkbox)
        
        self.url_monitoring_checkbox = QCheckBox("URL monitoring")
        group_layout.addWidget(self.url_monitoring_checkbox)
        
        self.file_monitoring_checkbox = QCheckBox("File monitoring")
        group_layout.addWidget(self.file_monitoring_checkbox)
        
        self.system_monitoring_checkbox = QCheckBox("System monitoring")
        group_layout.addWidget(self.system_monitoring_checkbox)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Monitored folders
        folders_group = QGroupBox("Monitored Folders")
        folders_layout = QVBoxLayout()
        
        self.downloads_checkbox = QCheckBox("Downloads folder")
        folders_layout.addWidget(self.downloads_checkbox)
        
        self.desktop_checkbox = QCheckBox("Desktop")
        folders_layout.addWidget(self.desktop_checkbox)
        
        self.documents_checkbox = QCheckBox("Documents")
        folders_layout.addWidget(self.documents_checkbox)
        
        folders_group.setLayout(folders_layout)
        layout.addWidget(folders_group)
        
        layout.addStretch()
        return widget
    
    def _create_scanning_tab(self) -> QWidget:
        """Create scanning settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Scanning Options")
        group_layout = QVBoxLayout()
        
        self.yara_rules_checkbox = QCheckBox("YARA rules scanning")
        group_layout.addWidget(self.yara_rules_checkbox)
        
        self.virustotal_checkbox = QCheckBox("VirusTotal API scanning")
        group_layout.addWidget(self.virustotal_checkbox)
        
        self.ml_scanning_checkbox = QCheckBox("Machine learning scanning")
        group_layout.addWidget(self.ml_scanning_checkbox)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # VirusTotal API key
        api_group = QGroupBox("VirusTotal API")
        api_layout = QFormLayout()
        
        self.virustotal_api_key = QLineEdit()
        self.virustotal_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("API Key:", self.virustotal_api_key)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        layout.addStretch()
        return widget
    
    def _create_alerts_tab(self) -> QWidget:
        """Create alerts settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        group = QGroupBox("Alert Thresholds")
        form_layout = QFormLayout()
        
        self.safe_threshold = QSpinBox()
        self.safe_threshold.setRange(0, 100)
        self.safe_threshold.setSuffix("%")
        form_layout.addRow("Safe Threshold:", self.safe_threshold)
        
        self.suspicious_threshold = QSpinBox()
        self.suspicious_threshold.setRange(0, 100)
        self.suspicious_threshold.setSuffix("%")
        form_layout.addRow("Suspicious Threshold:", self.suspicious_threshold)
        
        self.dangerous_threshold = QSpinBox()
        self.dangerous_threshold.setRange(0, 100)
        self.dangerous_threshold.setSuffix("%")
        form_layout.addRow("Dangerous Threshold:", self.dangerous_threshold)
        
        group.setLayout(form_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return widget
    
    def _load_settings(self):
        """Load settings from config"""
        # General
        self.auto_start_checkbox.setChecked(self.config.get("app.auto_start", True))
        self.minimize_tray_checkbox.setChecked(self.config.get("app.minimize_to_tray", True))
        self.notifications_checkbox.setChecked(self.config.get("app.show_notifications", True))
        self.sound_alerts_checkbox.setChecked(self.config.get("app.sound_alerts", True))
        
        # Monitoring
        self.email_monitoring_checkbox.setChecked(self.config.get("monitoring.email_monitoring", True))
        self.url_monitoring_checkbox.setChecked(self.config.get("monitoring.url_monitoring", True))
        self.file_monitoring_checkbox.setChecked(self.config.get("monitoring.file_monitoring", True))
        self.system_monitoring_checkbox.setChecked(self.config.get("monitoring.system_monitoring", True))
        
        # Scanning
        self.yara_rules_checkbox.setChecked(self.config.get("scanning.yara_rules_enabled", True))
        self.virustotal_checkbox.setChecked(self.config.get("scanning.virustotal_enabled", True))
        self.ml_scanning_checkbox.setChecked(self.config.get("scanning.ml_scanning_enabled", True))
        self.virustotal_api_key.setText(self.config.get("scanning.virustotal_api_key", ""))
        
        # Alerts
        self.safe_threshold.setValue(int(self.config.get("alerts.safe_threshold", 0.3) * 100))
        self.suspicious_threshold.setValue(int(self.config.get("alerts.suspicious_threshold", 0.6) * 100))
        self.dangerous_threshold.setValue(int(self.config.get("alerts.dangerous_threshold", 0.8) * 100))
    
    def _save_settings(self):
        """Save settings to config"""
        # General
        self.config.set("app.auto_start", self.auto_start_checkbox.isChecked())
        self.config.set("app.minimize_to_tray", self.minimize_tray_checkbox.isChecked())
        self.config.set("app.show_notifications", self.notifications_checkbox.isChecked())
        self.config.set("app.sound_alerts", self.sound_alerts_checkbox.isChecked())
        
        # Monitoring
        self.config.set("monitoring.email_monitoring", self.email_monitoring_checkbox.isChecked())
        self.config.set("monitoring.url_monitoring", self.url_monitoring_checkbox.isChecked())
        self.config.set("monitoring.file_monitoring", self.file_monitoring_checkbox.isChecked())
        self.config.set("monitoring.system_monitoring", self.system_monitoring_checkbox.isChecked())
        
        # Scanning
        self.config.set("scanning.yara_rules_enabled", self.yara_rules_checkbox.isChecked())
        self.config.set("scanning.virustotal_enabled", self.virustotal_checkbox.isChecked())
        self.config.set("scanning.ml_scanning_enabled", self.ml_scanning_checkbox.isChecked())
        self.config.set("scanning.virustotal_api_key", self.virustotal_api_key.text())
        
        # Alerts
        self.config.set("alerts.safe_threshold", self.safe_threshold.value() / 100)
        self.config.set("alerts.suspicious_threshold", self.suspicious_threshold.value() / 100)
        self.config.set("alerts.dangerous_threshold", self.dangerous_threshold.value() / 100)
        
        self.config.save()
        self.accept()
