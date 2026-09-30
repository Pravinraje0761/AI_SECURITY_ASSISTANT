from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QGridLayout, QFrame
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


class MonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._workers = []
        tabs = QTabWidget()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("System Monitor")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #e94560;")
        layout.addWidget(title)
        tabs.addTab(self._resources_tab(), "Resources")
        tabs.addTab(self._processes_tab(), "Processes")
        tabs.addTab(self._connections_tab(), "Network")
        tabs.addTab(self._startup_tab(), "Startup")
        layout.addWidget(tabs)

    def _resources_tab(self):
        w = QWidget()
        layout = QGridLayout(w)
        layout.setHorizontalSpacing(14)
        layout.setVerticalSpacing(14)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        self.cpu_label = self._metric_card("CPU", "Loading...")
        self.mem_label = self._metric_card("Memory", "Loading...")
        self.disk_label = self._metric_card("Disk", "Loading...")
        self.net_label = self._metric_card("Network", "Loading...")
        self.uptime_label = self._metric_card("Uptime", "Loading...")
        layout.addWidget(self.cpu_label, 0, 0)
        layout.addWidget(self.mem_label, 0, 1)
        layout.addWidget(self.disk_label, 1, 0)
        layout.addWidget(self.net_label, 1, 1)
        layout.addWidget(self.uptime_label, 2, 0)
        return w

    def _metric_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #16213e; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); }")
        frame.setFixedHeight(86)
        v = QVBoxLayout(frame)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(6)
        t = QLabel(title)
        t.setStyleSheet("color: rgba(255,255,255,0.6); font-size: 11px; font-weight: bold; background: transparent;")
        v.addWidget(t)
        v.addStretch()
        val = QLabel(value)
        val.setObjectName("metric_value")
        val.setStyleSheet("color: white; font-size: 19px; font-weight: bold; background: transparent;")
        v.addWidget(val)
        frame._val = val
        return frame

    def _processes_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        self.proc_table = QTableWidget()
        self.proc_table.setColumnCount(5)
        self.proc_table.setHorizontalHeaderLabels(["PID", "Name", "Mem%", "Status", "User"])
        self.proc_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.proc_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.proc_table)
        return w

    def _connections_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        self.conn_table = QTableWidget()
        self.conn_table.setColumnCount(6)
        self.conn_table.setHorizontalHeaderLabels(["Local", "Remote", "Host", "Status", "PID", "Risk"])
        self.conn_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.conn_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.conn_table)
        return w

    def _startup_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        self.startup_table = QTableWidget()
        self.startup_table.setColumnCount(3)
        self.startup_table.setHorizontalHeaderLabels(["Name", "Path", "Registry"])
        self.startup_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.startup_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.startup_table)
        return w

    def refresh(self):
        w1 = _ApiWorker(api.resources)
        w1.finished.connect(self._on_resources)
        self._workers.append(w1)
        w1.start()

        w2 = _ApiWorker(api.processes)
        w2.finished.connect(self._on_processes)
        self._workers.append(w2)
        w2.start()

        w3 = _ApiWorker(api.connections)
        w3.finished.connect(self._on_connections)
        self._workers.append(w3)
        w3.start()

        w4 = _ApiWorker(api.startup)
        w4.finished.connect(self._on_startup)
        self._workers.append(w4)
        w4.start()

    def _on_resources(self, data):
        try:
            cpu = data.get("cpu_percent", 0)
            mem = data.get("memory_percent", 0)
            disk = data.get("disk_percent", 0)
            sent = data.get("net_bytes_sent", 0)
            recv = data.get("net_bytes_recv", 0)
            uptime = data.get("uptime_seconds", 0)
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.cpu_label._val.setText(f"{cpu:.1f}%")
            self.mem_label._val.setText(f"{mem:.1f}%")
            self.disk_label._val.setText(f"{disk:.1f}%")
            self.net_label._val.setText(f"Up: {sent/(1024*1024):.1f}MB / Down: {recv/(1024*1024):.1f}MB")
            self.uptime_label._val.setText(f"{int(hours)}h {int(minutes)}m")
        except Exception:
            pass

    def _on_processes(self, data):
        try:
            procs = data.get("processes", [])[:50]
            self.proc_table.setRowCount(len(procs))
            for i, p in enumerate(procs):
                self.proc_table.setItem(i, 0, QTableWidgetItem(str(p.get("pid", ""))))
                name_item = QTableWidgetItem(p.get("name", ""))
                if p.get("suspicious"):
                    name_item.setForeground(Qt.GlobalColor.red)
                self.proc_table.setItem(i, 1, name_item)
                self.proc_table.setItem(i, 2, QTableWidgetItem(f"{p.get('memory', 0):.1f}"))
                self.proc_table.setItem(i, 3, QTableWidgetItem(p.get("status", "")))
                self.proc_table.setItem(i, 4, QTableWidgetItem(p.get("user", "")))
        except Exception:
            pass

    def _on_connections(self, data):
        try:
            conns = data.get("connections", [])[:50]
            self.conn_table.setRowCount(len(conns))
            for i, c in enumerate(conns):
                self.conn_table.setItem(i, 0, QTableWidgetItem(str(c.get("local_port", ""))))
                self.conn_table.setItem(i, 1, QTableWidgetItem(c.get("remote_ip", "")))
                self.conn_table.setItem(i, 2, QTableWidgetItem(c.get("remote_host", "")[:40]))
                self.conn_table.setItem(i, 3, QTableWidgetItem(c.get("status", "")))
                self.conn_table.setItem(i, 4, QTableWidgetItem(str(c.get("pid", ""))))
                risk_item = QTableWidgetItem(c.get("risk_note", ""))
                if c.get("suspicious"):
                    risk_item.setForeground(Qt.GlobalColor.red)
                self.conn_table.setItem(i, 5, risk_item)
        except Exception:
            pass

    def _on_startup(self, data):
        try:
            startup = data.get("programs", [])
            self.startup_table.setRowCount(len(startup))
            for i, s in enumerate(startup):
                self.startup_table.setItem(i, 0, QTableWidgetItem(s.get("name", "")))
                self.startup_table.setItem(i, 1, QTableWidgetItem(s.get("path", "")[:80]))
                self.startup_table.setItem(i, 2, QTableWidgetItem(s.get("hive", "")))
        except Exception:
            pass
