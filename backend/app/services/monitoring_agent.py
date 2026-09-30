import threading
import time
import logging
from app.services.behavior_service import behavior_service
from app.services.threat_engine import threat_engine
from app.services.alert_service import alert_service

logger = logging.getLogger(__name__)


class MonitoringAgent:
    def __init__(self):
        self._running = False
        self._thread = None
        self._interval = 30
        self._ticks = 0

    def start(self, interval: int = 30):
        if self._running:
            return
        self._interval = interval
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Monitoring agent started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Monitoring agent stopped")

    def _loop(self):
        while self._running:
            try:
                self._tick()
            except Exception as e:
                logger.error(f"Monitor tick error: {e}")
            time.sleep(self._interval)

    def _tick(self):
        self._ticks += 1
        summary = behavior_service.get_behavior_summary()

        for proc in summary.get("suspicious_processes", []):
            alert_service.create(
                title=f"Suspicious Process: {proc['name']}",
                description=f"PID {proc['pid']}, User: {proc.get('user', '?')}",
                severity="high", source="process_monitor",
            )
        for conn in summary.get("suspicious_connections", []):
            alert_service.create(
                title=f"Suspicious Network: {conn['remote_ip']}:{conn['remote_port']}",
                description=f"Status: {conn['status']}. {conn.get('risk_note', '')}",
                severity="medium", source="network_monitor",
            )

        resources = summary.get("resources", {})
        if resources.get("cpu_percent", 0) > 95:
            alert_service.create("High CPU Usage", f"CPU at {resources['cpu_percent']}%", "high", "resource_monitor")
        if resources.get("memory_percent", 0) > 95:
            alert_service.create("High Memory Usage", f"Memory at {resources['memory_percent']}%", "high", "resource_monitor")

    @property
    def is_running(self):
        return self._running

    def get_status(self):
        return {"running": self._running, "interval": self._interval, "total_ticks": self._ticks}


monitoring_agent = MonitoringAgent()
