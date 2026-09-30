import sys
import os
import requests

BACKEND_URL = "http://127.0.0.1:8000"


class ApiClient:
    def __init__(self, base_url=BACKEND_URL):
        self.base_url = base_url
        self.token = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def register(self, email, password, first_name="", last_name=""):
        r = requests.post(f"{self.base_url}/api/v1/auth/register", json={
            "email": email, "password": password,
            "first_name": first_name, "last_name": last_name,
        })
        r.raise_for_status()
        return r.json()

    def login(self, email, password):
        r = requests.post(f"{self.base_url}/api/v1/auth/login",
                          data={"username": email, "password": password})
        r.raise_for_status()
        data = r.json()
        self.token = data["access_token"]
        return data

    def get(self, path, **kwargs):
        r = requests.get(f"{self.base_url}{path}", headers=self._headers(), **kwargs)
        r.raise_for_status()
        return r.json()

    def post(self, path, **kwargs):
        r = requests.post(f"{self.base_url}{path}", headers=self._headers(), **kwargs)
        r.raise_for_status()
        return r.json()

    def delete(self, path, **kwargs):
        r = requests.delete(f"{self.base_url}{path}", headers=self._headers(), **kwargs)
        r.raise_for_status()
        return r.json()

    def dashboard(self):
        return self.get("/api/v1/dashboard")

    def threat(self):
        return self.get("/api/v1/monitoring/threat")

    def score(self):
        return self.get("/api/v1/monitoring/score")

    def resources(self):
        return self.get("/api/v1/monitoring/resources")

    def processes(self):
        return self.get("/api/v1/monitoring/processes")

    def connections(self):
        return self.get("/api/v1/monitoring/connections")

    def startup(self):
        return self.get("/api/v1/monitoring/startup")

    def alerts(self, severity=None):
        params = {}
        if severity:
            params["severity"] = severity
        return self.get("/api/v1/alerts/", params=params)

    def alert_counts(self):
        return self.get("/api/v1/alerts/counts")

    def ack_alert(self, alert_id):
        return self.post(f"/api/v1/alerts/{alert_id}/acknowledge")

    def scan_url(self, url):
        return self.post("/api/v1/scan/url", json={"type": "url", "target": url})

    def scan_history(self):
        return self.get("/api/v1/scan/history")

    def analyze_email(self, subject, sender, body):
        return self.post("/api/v1/protection/analyze-email", json={
            "subject": subject, "sender": sender, "body": body,
        })

    def check_url(self, url, browser="unknown"):
        return self.post("/api/v1/protection/check-url", json={"url": url, "browser": browser})

    def email_history(self):
        return self.get("/api/v1/protection/email-history")

    def website_history(self):
        return self.get("/api/v1/protection/website-history")


api = ApiClient()
