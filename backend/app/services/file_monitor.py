import os
import threading
import time
import logging
from typing import Dict, List, Callable
from app.services.malware_service import malware_service
from app.services.alert_service import alert_service

logger = logging.getLogger(__name__)

WATCHED_FOLDERS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Documents"),
]

SCANNABLE_EXT = {'.exe', '.bat', '.cmd', '.com', '.msi', '.scr', '.pif', '.jar', '.zip', '.7z', '.rar', '.ps1', '.vbs', '.js'}


class FileMonitor:
    def __init__(self):
        self._running = False
        self._thread = None
        self._interval = 10
        self._snapshots: Dict[str, float] = {}
        self._callbacks: List[Callable] = []

    def start(self, interval: int = 10):
        if self._running:
            return
        self._interval = interval
        self._take_snapshot()
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("File monitor started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _take_snapshot(self):
        for folder in WATCHED_FOLDERS:
            if not os.path.isdir(folder):
                continue
            for f in os.listdir(folder):
                path = os.path.join(folder, f)
                try:
                    if os.path.isfile(path):
                        self._snapshots[path] = os.path.getmtime(path)
                except OSError:
                    pass

    def _loop(self):
        while self._running:
            try:
                self._check()
            except Exception as e:
                logger.error(f"File monitor error: {e}")
            time.sleep(self._interval)

    def _check(self):
        new_files = []
        for folder in WATCHED_FOLDERS:
            if not os.path.isdir(folder):
                continue
            for f in os.listdir(folder):
                path = os.path.join(folder, f)
                try:
                    if not os.path.isfile(path):
                        continue
                    mtime = os.path.getmtime(path)
                    if path not in self._snapshots:
                        new_files.append(path)
                    self._snapshots[path] = mtime
                except OSError:
                    pass

        for path in new_files:
            _, ext = os.path.splitext(path.lower())
            if ext in SCANNABLE_EXT:
                try:
                    result = malware_service.scan_file(path)
                    fname = os.path.basename(path)
                    if result.get("is_malicious"):
                        alert_service.create(
                            title=f"Malicious File: {fname}",
                            description=f"Risk: {result['risk_score']}/100. " + ", ".join(result.get("indicators", [])),
                            severity="critical", source="file_monitor",
                        )
                    elif result.get("risk_score", 0) > 20:
                        alert_service.create(
                            title=f"Suspicious File: {fname}",
                            description=f"Risk: {result['risk_score']}/100. " + ", ".join(result.get("indicators", [])),
                            severity="medium", source="file_monitor",
                        )
                except Exception as e:
                    logger.error(f"File scan error: {e}")

    @property
    def is_running(self):
        return self._running

    def get_status(self):
        return {"running": self._running, "interval": self._interval, "watched_folders": WATCHED_FOLDERS}


file_monitor = FileMonitor()
