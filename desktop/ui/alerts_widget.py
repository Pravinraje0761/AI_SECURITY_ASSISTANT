from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QComboBox
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


class AlertsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._workers = []
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Security Alerts")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #e94560;")
        layout.addWidget(title)

        controls = QHBoxLayout()
        self.severity_filter = QComboBox()
        self.severity_filter.addItems(["All", "Critical", "High", "Medium", "Low", "Info"])
        self.severity_filter.currentTextChanged.connect(self._load)
        controls.addWidget(QLabel("Filter:"))
        controls.addWidget(self.severity_filter)
        controls.addStretch()
        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self._load)
        controls.addWidget(refresh)
        ack_all = QPushButton("Clear Acknowledged")
        ack_all.clicked.connect(self._clear_ack)
        controls.addWidget(ack_all)
        layout.addLayout(controls)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Severity", "Title", "Source", "Time", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def _load(self):
        sev = self.severity_filter.currentText().lower()
        if sev == "all":
            sev = None
        try:
            if sev:
                w = _ApiWorker(api.alerts, sev)
            else:
                w = _ApiWorker(api.alerts)
            w.finished.connect(self._on_alerts)
            self._workers.append(w)
            w.start()
        except Exception:
            pass

    def _on_alerts(self, alerts):
        try:
            self.table.setRowCount(len(alerts))
            for i, a in enumerate(alerts):
                sev_item = QTableWidgetItem(a.get("severity", "").upper())
                sev_item.setForeground(Qt.GlobalColor.red if a.get("severity") in ("critical", "high") else Qt.GlobalColor.yellow if a.get("severity") == "medium" else Qt.GlobalColor.green)
                self.table.setItem(i, 0, sev_item)
                self.table.setItem(i, 1, QTableWidgetItem(a.get("title", "")))
                self.table.setItem(i, 2, QTableWidgetItem(a.get("source", "")))
                self.table.setItem(i, 3, QTableWidgetItem(a.get("created_at", "")[:19]))

                btn = QPushButton("Ack")
                alert_id = a.get("id")
                btn.clicked.connect(lambda checked, aid=alert_id: self._ack(aid))
                self.table.setCellWidget(i, 4, btn)
        except Exception:
            pass

    def _ack(self, alert_id):
        try:
            api.ack_alert(alert_id)
            self._load()
        except Exception:
            pass

    def _clear_ack(self):
        try:
            api.delete("/api/v1/alerts/clear-acknowledged")
            self._load()
        except Exception:
            pass
