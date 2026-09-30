from typing import Dict, List
from datetime import datetime
from app.services.behavior_service import behavior_service
from app.services.malware_service import malware_service
from app.services.phishing_service import phishing_service


class ThreatEngine:
    def __init__(self):
        self.history: List[Dict] = []

    def calculate(self) -> Dict:
        behavior = behavior_service.get_behavior_summary()
        malware_stats = malware_service.get_stats()
        phishing_stats = phishing_service.get_stats()

        b_score = behavior.get("risk_score", 0)
        sus_p = len(behavior.get("suspicious_processes", []))
        sus_c = len(behavior.get("suspicious_connections", []))
        total = b_score
        factors = []
        if sus_p:
            total += 25
            factors.append({"factor": "suspicious_processes", "count": sus_p, "weight": 25})
        if sus_c:
            total += 20
            factors.append({"factor": "suspicious_connections", "count": sus_c, "weight": 20})
        total = min(total, 100)

        if total >= 70: level = "critical"
        elif total >= 50: level = "high"
        elif total >= 30: level = "medium"
        elif total >= 10: level = "low"
        else: level = "safe"

        result = {
            "overall_score": total,
            "threat_level": level,
            "factors": factors,
            "behavior_score": b_score,
            "malware_scans": malware_stats["total_scans"],
            "malware_threats": malware_stats["threats_found"],
            "url_scans": phishing_stats["total_scans"],
            "url_threats": phishing_stats["threats_found"],
            "suspicious_processes": sus_p,
            "suspicious_connections": sus_c,
            "resources": behavior.get("resources", {}),
            "indicators": behavior.get("indicators", []),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.history.append(result)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        return result

    def get_security_score(self) -> Dict:
        threat = self.calculate()
        score = max(100 - threat["overall_score"], 0)
        if score >= 80: status = "excellent"
        elif score >= 60: status = "good"
        elif score >= 40: status = "fair"
        elif score >= 20: status = "poor"
        else: status = "critical"
        return {
            "security_score": score, "status": status,
            "threat_level": threat["threat_level"],
            "threat_score": threat["overall_score"],
            "indicators": threat["indicators"],
        }

    def get_history(self, limit: int = 20):
        return self.history[-limit:]


threat_engine = ThreatEngine()
