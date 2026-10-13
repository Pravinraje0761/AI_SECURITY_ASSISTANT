def test_health(client):
    assert client.get("/health").status_code == 200


def test_login_rejects_wrong_password(client, auth_headers):
    r = client.post("/api/v1/auth/login", data={"username": "tester@example.com", "password": "nope"})
    assert r.status_code in (400, 401)


def test_me_requires_a_token(client):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_me_returns_the_logged_in_user(client, auth_headers):
    r = client.get("/api/v1/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "tester@example.com"


def test_scanning_requires_a_token(client):
    r = client.post("/api/v1/scan/url", json={"type": "phishing", "target": "http://example.com"})
    assert r.status_code == 401


def test_benign_and_phishing_urls_are_separated(client, auth_headers):
    safe = client.post("/api/v1/scan/url", headers=auth_headers,
                       json={"type": "phishing", "target": "https://www.wikipedia.org"}).json()
    bad = client.post("/api/v1/scan/url", headers=auth_headers,
                      json={"type": "phishing", "target": "http://paypa1-secure-login.verify-account.tk/login.php"}).json()
    assert safe["result"] == "safe"
    assert bad["result"] != "safe"
    assert bad["score"] > safe["score"]


def test_scans_are_recorded_in_history(client, auth_headers):
    client.post("/api/v1/scan/url", headers=auth_headers, json={"type": "phishing", "target": "http://example.org"})
    r = client.get("/api/v1/scan/history", headers=auth_headers)
    assert r.status_code == 200
    assert any(item["target"] == "http://example.org" for item in r.json())


def test_scam_email_scores_higher_than_a_normal_one(client, auth_headers):
    normal = client.post("/api/v1/protection/analyze-email", headers=auth_headers, json={
        "subject": "Team lunch on Friday", "sender": "colleague@company.com",
        "body": "Shall we meet at 1pm at the usual place?"}).json()
    scam = client.post("/api/v1/protection/analyze-email", headers=auth_headers, json={
        "subject": "URGENT: your account will be suspended", "sender": "security@paypa1-verify.tk",
        "body": "Verify your password immediately at http://paypa1-verify.tk/login or lose access. "
                "You have won a $1000 gift card, click here to claim."}).json()
    key = next(k for k in ("score", "combined_score", "probability", "risk_score") if k in scam)
    assert scam[key] > normal[key]
