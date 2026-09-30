"""
Notification Manager for AI Digital Bodyguard
Handles desktop notifications and alerts
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QColor, QFont
import sys

class NotificationWidget(QWidget):
    """Custom notification widget"""
    
    dismissed = pyqtSignal()
    
    def __init__(self, title: str, message: str, alert_type: str = "info", parent=None):
        super().__init__(parent)
        self.alert_type = alert_type
        self._setup_ui(title, message)
        self._setup_animation()
    
    def _setup_ui(self, title: str, message: str):
        """Setup notification UI"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 120)
        
        # Main frame
        self.frame = QFrame()
        self.frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self._get_title_color()};")
        layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Arial", 9))
        message_label.setStyleSheet("color: #333;")
        layout.addWidget(message_label)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        close_btn.clicked.connect(self.dismiss)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Position close button
        close_btn.setParent(self.frame)
        close_btn.move(360, 5)
    
    def _get_title_color(self) -> str:
        """Get title color based on alert type"""
        colors = {
            "safe": "#28a745",
            "suspicious": "#ffc107",
            "dangerous": "#dc3545",
            "info": "#007bff"
        }
        return colors.get(self.alert_type, "#007bff")
    
    def _setup_animation(self):
        """Setup fade in/out animations"""
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(0)
        
        # Fade in
        self.fade_in = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Auto-dismiss timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.dismiss)
        self.timer.start(5000)  # 5 seconds
    
    def show_notification(self, x: int, y: int):
        """Show notification at position"""
        self.move(x, y)
        self.fade_in.start()
        self.show()
    
    def dismiss(self):
        """Dismiss notification"""
        self.timer.stop()
        self.dismissed.emit()
        self.close()

class NotificationManager:
    """Manages desktop notifications"""
    
    def __init__(self):
        self.notifications = []
        self.screen_width = 1920  # Default, will be updated
        self.screen_height = 1080
    
    def show(self, title: str, message: str, alert_type: str = "info"):
        """Show a notification"""
        notification = NotificationWidget(title, message, alert_type)
        notification.dismissed.connect(lambda: self._remove_notification(notification))
        
        # Position notification (top-right corner)
        x = self.screen_width - notification.width() - 20
        y = 20 + len(self.notifications) * (notification.height() + 10)
        
        notification.show_notification(x, y)
        self.notifications.append(notification)
    
    def _remove_notification(self, notification: NotificationWidget):
        """Remove notification from list"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.deleteLater()
    
    def clear_all(self):
        """Clear all notifications"""
        for notification in self.notifications[:]:
            notification.dismiss()
