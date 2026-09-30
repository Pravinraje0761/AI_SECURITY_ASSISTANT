"""
System Tray Icon for AI Digital Bodyguard
Provides system tray functionality and menu
"""

from PyQt6.QtWidgets import (
    QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, 
    QLabel, QPushButton, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
import sys
import os

class SystemTrayIcon(QSystemTrayIcon):
    """System tray icon with menu"""
    
    # Signals
    show_dashboard = pyqtSignal()
    show_settings = pyqtSignal()
    quit_app = pyqtSignal()
    toggle_protection = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.protection_enabled = True
        self._setup_tray_icon()
        self._setup_menu()
    
    def _setup_tray_icon(self):
        """Setup tray icon"""
        # Create icon (using built-in icon for now, replace with custom icon)
        icon = QIcon.fromTheme("security-shield")
        if icon.isNull():
            # Fallback to a simple colored icon
            from PyQt6.QtGui import QPixmap, QPainter, QColor
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QColor("#00FF00"))  # Green for safe
            painter.drawEllipse(0, 0, 64, 64)
            painter.end()
            icon = QIcon(pixmap)
        
        self.setIcon(icon)
        self.setToolTip("AI Digital Bodyguard - Active")
        self.activated.connect(self._on_activated)
    
    def _setup_menu(self):
        """Setup context menu"""
        menu = QMenu()
        
        # Protection toggle
        self.protection_action = QAction("Protection: ON", menu)
        self.protection_action.setCheckable(True)
        self.protection_action.setChecked(True)
        self.protection_action.triggered.connect(self._toggle_protection)
        menu.addAction(self.protection_action)
        
        menu.addSeparator()
        
        # Dashboard
        dashboard_action = QAction("Open Dashboard", menu)
        dashboard_action.triggered.connect(self.show_dashboard.emit)
        menu.addAction(dashboard_action)
        
        # Settings
        settings_action = QAction("Settings", menu)
        settings_action.triggered.connect(self.show_settings.emit)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # Status
        status_action = QAction("Status: Protected", menu)
        status_action.setEnabled(False)
        menu.addAction(status_action)
        
        menu.addSeparator()
        
        # Quit
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.quit_app.emit)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
    
    def _on_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_dashboard.emit()
    
    def _toggle_protection(self, checked):
        """Toggle protection status"""
        self.protection_enabled = checked
        self.protection_action.setText(f"Protection: {'ON' if checked else 'OFF'}")
        self.toggle_protection.emit(checked)
        
        # Update icon color
        from PyQt6.QtGui import QPixmap, QPainter, QColor
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        color = QColor("#00FF00") if checked else QColor("#FF0000")
        painter.setBrush(color)
        painter.drawEllipse(0, 0, 64, 64)
        painter.end()
        self.setIcon(QIcon(pixmap))
        
        status = "Active" if checked else "Disabled"
        self.setToolTip(f"AI Digital Bodyguard - {status}")
    
    def show_notification(self, title: str, message: str, icon_type: str = "info"):
        """Show desktop notification"""
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtCore import QCoreApplication
        
        # Show message box
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        
        if icon_type == "safe":
            msg.setIcon(QMessageBox.Icon.Information)
        elif icon_type == "suspicious":
            msg.setIcon(QMessageBox.Icon.Warning)
        elif icon_type == "dangerous":
            msg.setIcon(QMessageBox.Icon.Critical)
        else:
            msg.setIcon(QMessageBox.Icon.Information)
        
        msg.exec()
        
        # Also show as tray notification
        self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 5000)
