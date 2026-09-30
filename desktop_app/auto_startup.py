"""
Auto-startup Manager for AI Digital Bodyguard
Handles Windows startup registration
"""

import os
import winreg
from typing import Optional

class AutoStartupManager:
    """Manages application auto-startup on Windows"""
    
    def __init__(self, app_name: str, app_path: str):
        self.app_name = app_name
        self.app_path = app_path
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    def is_enabled(self) -> bool:
        """Check if auto-startup is enabled"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.registry_key) as key:
                value, _ = winreg.QueryValueEx(key, self.app_name)
                return value == self.app_path
        except WindowsError:
            return False
    
    def enable(self) -> bool:
        """Enable auto-startup"""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                self.registry_key, 
                0, 
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.SetValueEx(
                    key, 
                    self.app_name, 
                    0, 
                    winreg.REG_SZ, 
                    self.app_path
                )
            return True
        except Exception as e:
            print(f"Error enabling auto-startup: {e}")
            return False
    
    def disable(self) -> bool:
        """Disable auto-startup"""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                self.registry_key, 
                0, 
                winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, self.app_name)
            return True
        except Exception as e:
            print(f"Error disabling auto-startup: {e}")
            return False
    
    def toggle(self) -> bool:
        """Toggle auto-startup status"""
        if self.is_enabled():
            return self.disable()
        else:
            return self.enable()
