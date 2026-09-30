"""
Main Application Entry Point for AI Digital Bodyguard
PyQt6-based desktop application with system tray
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from desktop_app.system_tray import SystemTrayIcon
from desktop_app.config_manager import ConfigManager
from desktop_app.notification_manager import NotificationManager
from desktop_app.auto_startup import AutoStartupManager
import subprocess
import threading

class DigitalBodyguardApp:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # Keep running in system tray
        
        # Initialize components
        self.config = ConfigManager()
        self.notification_manager = NotificationManager()
        self.system_tray = SystemTrayIcon()
        
        # Setup auto-startup
        app_path = os.path.abspath(sys.argv[0])
        self.startup_manager = AutoStartupManager(
            self.config.get("app.name", "AI Digital Bodyguard"),
            app_path
        )
        
        # Connect signals
        self._connect_signals()
        
        # Setup backend process
        self.backend_process = None
        self._start_backend()
        
        # Enable auto-startup if configured
        if self.config.get("app.auto_start", True):
            self.startup_manager.enable()
    
    def _connect_signals(self):
        """Connect system tray signals"""
        self.system_tray.show_dashboard.connect(self._show_dashboard)
        self.system_tray.show_settings.connect(self._show_settings)
        self.system_tray.quit_app.connect(self._quit)
        self.system_tray.toggle_protection.connect(self._toggle_protection)
    
    def _start_backend(self):
        """Start the FastAPI backend server"""
        try:
            # Start backend in a separate thread
            backend_script = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "backend", 
                "app", 
                "main.py"
            )
            
            def run_backend():
                self.backend_process = subprocess.Popen(
                    [sys.executable, "-m", "app.main"],
                    cwd=os.path.join(os.path.dirname(__file__), "..", "backend")
                )
            
            thread = threading.Thread(target=run_backend, daemon=True)
            thread.start()
            
            # Show notification after backend starts
            QTimer.singleShot(3000, self._show_startup_notification)
            
        except Exception as e:
            print(f"Error starting backend: {e}")
            self.notification_manager.show(
                "Backend Error",
                f"Failed to start backend server: {e}",
                "dangerous"
            )
    
    def _show_startup_notification(self):
        """Show startup notification"""
        self.notification_manager.show(
            "AI Digital Bodyguard",
            "Protection is now active. Your system is being monitored.",
            "safe"
        )
    
    def _show_dashboard(self):
        """Show security dashboard"""
        try:
            # Open dashboard in browser
            import webbrowser
            webbrowser.open("http://localhost:8000/docs")
        except Exception as e:
            print(f"Error opening dashboard: {e}")
    
    def _show_settings(self):
        """Show settings dialog"""
        from desktop_app.ui.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config)
        dialog.exec()
    
    def _toggle_protection(self, enabled: bool):
        """Toggle protection status"""
        status = "enabled" if enabled else "disabled"
        self.notification_manager.show(
            "Protection Status",
            f"Protection has been {status}.",
            "safe" if enabled else "suspicious"
        )
    
    def _quit(self):
        """Quit application"""
        reply = QMessageBox.question(
            None,
            "Quit",
            "Are you sure you want to quit AI Digital Bodyguard?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Stop backend if running
            if self.backend_process:
                self.backend_process.terminate()
            
            # Clear notifications
            self.notification_manager.clear_all()
            
            # Quit application
            self.system_tray.hide()
            self.app.quit()
    
    def run(self):
        """Run the application"""
        self.system_tray.show()
        return self.app.exec()

def main():
    """Main entry point"""
    try:
        app = DigitalBodyguardApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
