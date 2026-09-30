@echo off
rem Double-click to open the AI Digital Bodyguard dashboard (no console window).
cd /d "%~dp0"
if exist "%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe" "%~dp0launch_dashboard.pyw"
) else (
    start "" pyw -3.13 "%~dp0launch_dashboard.pyw"
)
