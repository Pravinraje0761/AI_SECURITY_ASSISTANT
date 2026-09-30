from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont
import threading


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


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._workers = []
        self._setup_ui()
        self._timer = QTimer()
        self._timer.timeout.connect(self._refresh_data)
        self._timer.start(10000)
        QTimer.singleShot(500, self._refresh_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("AI Digital Bodyguard Dashboard")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #e94560;")
        layout.addWidget(title)

        self.score_card = self._make_card("SECURITY SCORE", "---", "#0f3460")
        self.threat_card = self._make_card("THREAT LEVEL", "---", "#533483")
        self.alert_card = self._make_card("ACTIVE ALERTS", "---", "#e94560")
        self.cpu_card = self._make_card("CPU USAGE", "---", "#0f3460")
        self.mem_card = self._make_card("MEMORY", "---", "#533483")
        self.disk_card = self._make_card("DISK", "---", "#e94560")

        cards_layout = QGridLayout()
        cards_layout.setHorizontalSpacing(16)
        cards_layout.setVerticalSpacing(16)
        cards_layout.setColumnStretch(0, 1)
        cards_layout.setColumnStretch(1, 1)
        cards_layout.setColumnStretch(2, 1)
        cards_layout.addWidget(self.score_card, 0, 0)
        cards_layout.addWidget(self.threat_card, 0, 1)
        cards_layout.addWidget(self.alert_card, 0, 2)
        cards_layout.addWidget(self.cpu_card, 1, 0)
        cards_layout.addWidget(self.mem_card, 1, 1)
        cards_layout.addWidget(self.disk_card, 1, 2)
        layout.addLayout(cards_layout)

        alerts_label = QLabel("Recent Alerts")
        alerts_label.setStyleSheet("color: #e0e0e0; font-size: 13px; font-weight: bold; margin-top: 6px;")
        layout.addWidget(alerts_label)

        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(4)
        self.alerts_table.setHorizontalHeaderLabels(["Severity", "Title", "Source", "Time"])
        self.alerts_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.alerts_table.verticalHeader().setVisible(False)
        self.alerts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.alerts_table.setAlternatingRowColors(True)
        self.alerts_table.setStyleSheet(
            "QTableWidget { alternate-background-color: #1c2b4a; }"
        )
        self.alerts_table.setMaximumHeight(250)
        layout.addWidget(self.alerts_table)

        self.status_label = QLabel("Loading...")
        self.status_label.setStyleSheet("color: #707890; font-size: 11px;")
        layout.addWidget(self.status_label)

    def _make_card(self, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(
            f"QFrame {{ background-color: {color}; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); }}"
        )
        frame.setFixedHeight(108)
        v = QVBoxLayout(frame)
        v.setContentsMargins(18, 16, 18, 16)
        v.setSpacing(8)
        t = QLabel(title)
        t.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 11px; font-weight: bold; background: transparent;")
        v.addWidget(t)
        v.addStretch()
        val = QLabel(value)
        val.setStyleSheet("color: white; font-size: 26px; font-weight: bold; background: transparent;")
        val.setAlignment(Qt.AlignmentFlag.AlignLeft)
        v.addWidget(val)
        frame._val = val
        return frame

    def _set(self, card, value):
        card._val.setText(str(value))

    def _refresh_data(self):
        try:
            from services.api_client import api
            w = _ApiWorker(api.dashboard)
            w.finished.connect(self._on_dashboard_data)
            w.error.connect(lambda e: self.status_label.setText(f"Backend error: {e}"))
            self._workers.append(w)
            w.start()
        except Exception as e:
            self.status_label.setText(f"Backend error: {e}")

        try:
            from services.api_client import api
            w = _ApiWorker(api.alerts)
            w.finished.connect(self._on_alerts_data)
            self._workers.append(w)
            w.start()
        except Exception:
            pass

    def _on_dashboard_data(self, data):
        try:
            score_data = data.get("security_score", {})
            self._set(self.score_card, f"{score_data.get('security_score', 0)}%")
            self._set(self.threat_card, score_data.get("threat_level", "?").upper())

            alerts_data = data.get("alerts", {})
            self._set(self.alert_card, str(alerts_data.get("unacknowledged", 0)))

            res = data.get("resources", {})
            self._set(self.cpu_card, f"{res.get('cpu_percent', 0):.0f}%")
            self._set(self.mem_card, f"{res.get('memory_percent', 0):.0f}%")
            self._set(self.disk_card, f"{res.get('disk_percent', 0):.0f}%")

            self.status_label.setText("Last updated: just now")
        except Exception as e:
            self.status_label.setText(f"Parse error: {e}")

    def _on_alerts_data(self, alert_list):
        try:
            items = alert_list[:10] if isinstance(alert_list, list) else []
            self.alerts_table.setRowCount(len(items))
            for i, a in enumerate(items):
                sev = a.get("severity", "?")
                item = QTableWidgetItem(sev.upper())
                if sev in ("critical", "high"):
                    item.setForeground(Qt.GlobalColor.red)
                elif sev == "medium":
                    item.setForeground(Qt.GlobalColor.yellow)
                else:
                    item.setForeground(Qt.GlobalColor.green)
                self.alerts_table.setItem(i, 0, item)
                self.alerts_table.setItem(i, 1, QTableWidgetItem(a.get("title", "")))
                self.alerts_table.setItem(i, 2, QTableWidgetItem(a.get("source", "")))
                self.alerts_table.setItem(i, 3, QTableWidgetItem(str(a.get("created_at", ""))[:19]))
        except Exception:
            pass
