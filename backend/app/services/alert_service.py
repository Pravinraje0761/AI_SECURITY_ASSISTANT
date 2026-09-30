from typing import Dict, List, Optional
from datetime import datetime
import uuid


class AlertService:
    def __init__(self):
        self._alerts: List[Dict] = []
        self._callbacks = []

    def create(self, title: str, description: str, severity: str = "info", source: str = "system") -> Dict:
        alert = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "severity": severity,
            "source": source,
            "acknowledged": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._alerts.insert(0, alert)
        if len(self._alerts) > 500:
            self._alerts = self._alerts[:500]
        for cb in self._callbacks:
            try:
                cb(alert)
            except Exception:
                pass
        return alert

    def get_all(self, severity: Optional[str] = None, limit: int = 50) -> List[Dict]:
        result = self._alerts
        if severity:
            result = [a for a in result if a["severity"] == severity]
        return result[:limit]

    def acknowledge(self, alert_id: str) -> Optional[Dict]:
        for a in self._alerts:
            if a["id"] == alert_id:
                a["acknowledged"] = True
                a["acknowledged_at"] = datetime.utcnow().isoformat()
                return a
        return None

    def counts(self) -> Dict:
        return {
            "total": len(self._alerts),
            "unacknowledged": sum(1 for a in self._alerts if not a["acknowledged"]),
            "critical": sum(1 for a in self._alerts if a["severity"] == "critical"),
            "high": sum(1 for a in self._alerts if a["severity"] == "high"),
            "medium": sum(1 for a in self._alerts if a["severity"] == "medium"),
            "low": sum(1 for a in self._alerts if a["severity"] == "low"),
            "info": sum(1 for a in self._alerts if a["severity"] == "info"),
        }

    def clear_acknowledged(self) -> int:
        before = len(self._alerts)
        self._alerts = [a for a in self._alerts if not a["acknowledged"]]
        return before - len(self._alerts)

    def on_alert(self, callback):
        self._callbacks.append(callback)


alert_service = AlertService()
