"""
AI Digital Bodyguard - Full Demo Script
Exercises every backend feature end-to-end against a running server.

Prereq: backend running (run `python start.py` or `uvicorn app.main:app`
from the backend/ folder first).
"""
import requests
import time
import sys

BASE = "http://127.0.0.1:8000"
EMAIL = "demo_user@example.com"
PASSWORD = "Demo1234!"


def line(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def show(label, resp):
    try:
        body = resp.json()
    except ValueError:
        body = resp.text
    print(f"[{resp.status_code}] {label}")
    print(body)


def wait_for_backend(timeout=30):
    print("[*] Waiting for backend...")
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health", timeout=2)
            if r.status_code == 200:
                print("[+] Backend is up:", r.json())
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False


def register_and_login():
    line("AUTH: register + login")
    r = requests.post(f"{BASE}/api/v1/auth/register", json={
        "email": EMAIL, "password": PASSWORD,
        "first_name": "Demo", "last_name": "User",
    })
    if r.status_code == 400:
        print("[i] User already registered, continuing to login")
    else:
        show("register", r)

    r = requests.post(f"{BASE}/api/v1/auth/login", data={
        "username": EMAIL, "password": PASSWORD,
    })
    show("login", r)
    r.raise_for_status()
    token = r.json()["access_token"]

    r = requests.get(f"{BASE}/api/v1/auth/me", headers=auth_header(token))
    show("me", r)
    return token


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def demo_scanning(token):
    line("SCANNING: phishing URL detection")
    r = requests.post(f"{BASE}/api/v1/scan/url", headers=auth_header(token),
                       json={"type": "phishing", "target": "http://paypal-login-verify.xyz"})
    show("scan/url (suspicious)", r)

    r = requests.post(f"{BASE}/api/v1/scan/url", headers=auth_header(token),
                       json={"type": "phishing", "target": "https://www.google.com"})
    show("scan/url (safe)", r)

    r = requests.get(f"{BASE}/api/v1/scan/history", headers=auth_header(token))
    show("scan/history", r)


def demo_protection(token):
    line("PROTECTION: email + browser URL analysis")
    r = requests.post(f"{BASE}/api/v1/protection/analyze-email", headers=auth_header(token), json={
        "subject": "Urgent: Verify your account now",
        "sender": "security@paypa1-support.com",
        "body": "Your account has been suspended. Click here immediately to verify your password and avoid permanent closure.",
    })
    show("analyze-email", r)

    r = requests.post(f"{BASE}/api/v1/protection/check-url", headers=auth_header(token), json={
        "url": "http://secure-bank-update.com/login", "browser": "chrome",
    })
    show("check-url", r)

    r = requests.get(f"{BASE}/api/v1/protection/email-history", headers=auth_header(token))
    show("email-history", r)

    r = requests.get(f"{BASE}/api/v1/protection/website-history", headers=auth_header(token))
    show("website-history", r)


def demo_monitoring(token):
    line("MONITORING: system + threat telemetry")
    show("monitoring/threat", requests.get(f"{BASE}/api/v1/monitoring/threat", headers=auth_header(token)))
    show("monitoring/score", requests.get(f"{BASE}/api/v1/monitoring/score", headers=auth_header(token)))
    show("monitoring/resources", requests.get(f"{BASE}/api/v1/monitoring/resources", headers=auth_header(token)))
    show("monitoring/processes", requests.get(f"{BASE}/api/v1/monitoring/processes", headers=auth_header(token)))
    show("monitoring/connections", requests.get(f"{BASE}/api/v1/monitoring/connections", headers=auth_header(token)))
    show("monitoring/startup", requests.get(f"{BASE}/api/v1/monitoring/startup", headers=auth_header(token)))
    show("monitoring/file-monitor/status", requests.get(f"{BASE}/api/v1/monitoring/file-monitor/status", headers=auth_header(token)))


def demo_alerts(token):
    line("ALERTS: seed demo alerts + review")
    show("alerts/demo-seed", requests.post(f"{BASE}/api/v1/alerts/demo-seed", headers=auth_header(token)))
    r = requests.get(f"{BASE}/api/v1/alerts/", headers=auth_header(token))
    show("alerts list", r)
    show("alerts/counts", requests.get(f"{BASE}/api/v1/alerts/counts", headers=auth_header(token)))

    alerts = r.json()
    if alerts:
        first_id = alerts[0]["id"]
        show(f"alerts/{first_id}/acknowledge", requests.post(
            f"{BASE}/api/v1/alerts/{first_id}/acknowledge", headers=auth_header(token)))

    show("alerts/monitor-status", requests.get(f"{BASE}/api/v1/alerts/monitor-status", headers=auth_header(token)))


def demo_dashboard():
    line("DASHBOARD: aggregate security overview")
    show("dashboard", requests.get(f"{BASE}/api/v1/dashboard"))


def main():
    if not wait_for_backend():
        print("[-] Backend never came up. Start it first:")
        print("    python start.py")
        sys.exit(1)

    token = register_and_login()
    demo_scanning(token)
    demo_protection(token)
    demo_monitoring(token)
    demo_alerts(token)
    demo_dashboard()

    line("DEMO COMPLETE")
    print("All AI Digital Bodyguard features exercised successfully.")


if __name__ == "__main__":
    main()
