from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.api_client import api


class _ApiWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._func(*self._args, **self._kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class ScannerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._workers = []
        tabs = QTabWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)

        tabs.addTab(self._url_tab(), "URL Scanner")
        tabs.addTab(self._email_tab(), "Email Analyzer")
        tabs.addTab(self._file_tab(), "File Scanner")

    def _url_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel("Scan a URL for phishing threats"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to scan (e.g. https://suspicious-site.xyz)")
        layout.addWidget(self.url_input)
        self.url_btn = QPushButton("Scan URL")
        self.url_btn.clicked.connect(self._scan_url)
        layout.addWidget(self.url_btn)
        self.url_result = QLabel("")
        self.url_result.setWordWrap(True)
        self.url_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #16213e;")
        layout.addWidget(self.url_result)
        self.url_indicators = QPlainTextEdit()
        self.url_indicators.setReadOnly(True)
        self.url_indicators.setMaximumHeight(150)
        self.url_indicators.setPlaceholderText("Indicators will appear here...")
        layout.addWidget(self.url_indicators)
        layout.addStretch()
        return w

    def _scan_url(self):
        url = self.url_input.text().strip()
        if not url:
            return
        self.url_btn.setEnabled(False)
        self.url_btn.setText("Scanning...")
        w = _ApiWorker(api.scan_url, url)
        w.finished.connect(self._on_url_result)
        w.error.connect(self._on_url_error)
        self._workers.append(w)
        w.start()

    def _on_url_result(self, result):
        self.url_btn.setEnabled(True)
        self.url_btn.setText("Scan URL")
        try:
            res = result.get("result", "unknown")
            score = result.get("score", 0)
            if res == "malicious":
                self.url_result.setText(f"DANGEROUS - Phishing Score: {score*100:.0f}%")
                self.url_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #4a0000; color: #ff4444; font-weight: bold; font-size: 14px;")
            else:
                self.url_result.setText(f"SAFE - Risk Score: {score*100:.0f}%")
                self.url_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #003a00; color: #44ff44; font-weight: bold; font-size: 14px;")
            details = result.get("details", {})
            indicators = details.get("indicators", [])
            self.url_indicators.setPlainText("\n".join(indicators) if indicators else "No suspicious indicators found.")
        except Exception as e:
            self.url_result.setText(f"Parse error: {e}")
            self.url_result.setStyleSheet("padding: 10px; color: #ff4444;")

    def _on_url_error(self, e):
        self.url_btn.setEnabled(True)
        self.url_btn.setText("Scan URL")
        self.url_result.setText(f"Error: {e}")
        self.url_result.setStyleSheet("padding: 10px; color: #ff4444;")

    def _email_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel("Analyze an email for phishing and scam content"))
        self.email_subject = QLineEdit()
        self.email_subject.setPlaceholderText("Email subject")
        layout.addWidget(self.email_subject)
        self.email_sender = QLineEdit()
        self.email_sender.setPlaceholderText("Sender email/name")
        layout.addWidget(self.email_sender)
        self.email_body = QPlainTextEdit()
        self.email_body.setPlaceholderText("Paste email body here...")
        self.email_body.setMaximumHeight(150)
        layout.addWidget(self.email_body)
        self.email_btn = QPushButton("Analyze Email")
        self.email_btn.clicked.connect(self._analyze_email)
        layout.addWidget(self.email_btn)
        self.email_result = QLabel("")
        self.email_result.setWordWrap(True)
        self.email_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #16213e;")
        layout.addWidget(self.email_result)
        self.email_indicators = QPlainTextEdit()
        self.email_indicators.setReadOnly(True)
        self.email_indicators.setMaximumHeight(150)
        layout.addWidget(self.email_indicators)
        layout.addStretch()
        return w

    def _analyze_email(self):
        subject = self.email_subject.text().strip()
        sender = self.email_sender.text().strip()
        body = self.email_body.toPlainText().strip()
        if not subject and not body:
            return
        self.email_btn.setEnabled(False)
        self.email_btn.setText("Analyzing...")
        w = _ApiWorker(api.analyze_email, subject, sender, body)
        w.finished.connect(self._on_email_result)
        w.error.connect(self._on_email_error)
        self._workers.append(w)
        w.start()

    def _on_email_result(self, result):
        self.email_btn.setEnabled(True)
        self.email_btn.setText("Analyze Email")
        try:
            res = result.get("result", "safe")
            score = result.get("score", 0)
            if res == "dangerous":
                self.email_result.setText(f"DANGEROUS EMAIL - Score: {score*100:.0f}%")
                self.email_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #4a0000; color: #ff4444; font-weight: bold; font-size: 14px;")
            elif res == "suspicious":
                self.email_result.setText(f"SUSPICIOUS EMAIL - Score: {score*100:.0f}%")
                self.email_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #4a3a00; color: #ffaa00; font-weight: bold; font-size: 14px;")
            else:
                self.email_result.setText(f"SAFE EMAIL - Score: {score*100:.0f}%")
                self.email_result.setStyleSheet("padding: 10px; border-radius: 6px; background-color: #003a00; color: #44ff44; font-weight: bold; font-size: 14px;")
            indicators = result.get("indicators", [])
            self.email_indicators.setPlainText("\n".join(indicators) if indicators else "No suspicious indicators found.")
        except Exception as e:
            self.email_result.setText(f"Parse error: {e}")
            self.email_result.setStyleSheet("padding: 10px; color: #ff4444;")

    def _on_email_error(self, e):
        self.email_btn.setEnabled(True)
        self.email_btn.setText("Analyze Email")
        self.email_result.setText(f"Error: {e}")
        self.email_result.setStyleSheet("padding: 10px; color: #ff4444;")

    def _file_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel("File scanning coming soon - use the API endpoint /api/v1/monitoring/scan-file"))
        layout.addStretch()
        return w
