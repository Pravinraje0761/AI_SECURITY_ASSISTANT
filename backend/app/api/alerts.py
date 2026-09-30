from fastapi import APIRouter, Depends, HTTPException
from app.services.alert_service import alert_service
from app.services.monitoring_agent import monitoring_agent
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/")
async def get_alerts(severity: str = None, limit: int = 50, user_id: str = Depends(get_current_user)):
    return alert_service.get_all(severity=severity, limit=limit)


@router.get("/counts")
async def get_counts(user_id: str = Depends(get_current_user)):
    return alert_service.counts()


@router.post("/{alert_id}/acknowledge")
async def ack_alert(alert_id: str, user_id: str = Depends(get_current_user)):
    result = alert_service.acknowledge(alert_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.delete("/clear-acknowledged")
async def clear_ack(user_id: str = Depends(get_current_user)):
    return {"removed": alert_service.clear_acknowledged()}


@router.post("/demo-seed")
async def demo_seed(user_id: str = Depends(get_current_user)):
    demo_alerts = [
        ("Phishing URL Blocked", "Blocked access to paypal-login-verify.xyz posing as PayPal login", "critical", "url_scanner"),
        ("Malware Signature Match", "svchost_update.exe matched known trojan signature", "critical", "malware_scanner"),
        ("Suspicious Process Detected", "powershell.exe spawned with hidden window and encoded command", "high", "behavior_monitor"),
        ("Credential Phishing Email", "Email claiming to be from Microsoft asking to verify account", "high", "email_analyzer"),
        ("Unusual Outbound Connection", "Connection to unrecognized host on port 4444", "high", "network_monitor"),
        ("Suspicious Network: 185.220.101.7:443", "Outbound connection to known Tor exit node", "medium", "network_monitor"),
        ("New Startup Program Added", "Unknown entry 'sysupdate32' added to registry Run key", "medium", "file_monitor"),
        ("Multiple Failed Login Attempts", "3 failed login attempts detected in the last 5 minutes", "medium", "auth_monitor"),
        ("Outdated Browser Extension", "Chrome extension 'AdBlock Pro' has known vulnerability", "low", "system_scanner"),
        ("USB Device Connected", "New removable storage device detected", "low", "device_monitor"),
        ("Scheduled Scan Completed", "Full system scan completed, 0 threats found", "info", "malware_scanner"),
        ("Definitions Updated", "Threat definitions updated to latest version", "info", "system"),
    ]
    created = [alert_service.create(t, d, s, src) for t, d, s, src in demo_alerts]
    return {"created": len(created)}


@router.get("/monitor-status")
async def monitor_status(user_id: str = Depends(get_current_user)):
    return monitoring_agent.get_status()


@router.post("/monitor/start")
async def start_monitor(user_id: str = Depends(get_current_user), interval: int = 30):
    monitoring_agent.start(interval)
    return monitoring_agent.get_status()


@router.post("/monitor/stop")
async def stop_monitor(user_id: str = Depends(get_current_user)):
    monitoring_agent.stop()
    return monitoring_agent.get_status()
