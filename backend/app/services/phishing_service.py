import re
from urllib.parse import urlparse
from typing import Dict


class PhishingService:
    KEYWORDS = [
        'login', 'signin', 'account', 'verify', 'bank', 'secure',
        'update', 'confirm', 'password', 'credential', 'wallet',
        'paypal', 'amazon', 'apple', 'microsoft', 'netflix',
        'facebook', 'instagram', 'whatsapp', 'crypto', 'metamask',
    ]
    BAD_TLDS = ['.xyz', '.top', '.tk', '.ml', '.ga', '.cf', '.buzz', '.click', '.link']
    SHORTENERS = {'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd', 'cutt.ly', 'rebrand.ly'}

    def __init__(self):
        self.scan_count = 0
        self.threats_found = 0

    def scan_url(self, url: str) -> Dict:
        self.scan_count += 1
        indicators = []
        score = 0

        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower().split(':')[0]
        except Exception:
            return {"is_phishing": False, "probability": 0.0, "indicators": [], "score": 0}

        for kw in self.KEYWORDS:
            if kw in domain:
                score += 12
                indicators.append(f"Keyword in domain: {kw}")

        for tld in self.BAD_TLDS:
            if domain.endswith(tld):
                score += 25
                indicators.append(f"Suspicious TLD: {tld}")

        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
            score += 40
            indicators.append("Raw IP address")

        if len(url) > 150:
            score += 10
            indicators.append("Very long URL")
        elif len(url) > 100:
            score += 5

        if domain.count('.') > 4:
            score += 10
            indicators.append("Excessive subdomains")

        if '@' in url:
            score += 30
            indicators.append("@ symbol in URL")

        if any(c in url for c in ['%2f', '%5c', '%00']):
            score += 15
            indicators.append("Encoded characters")

        if domain.split('.')[0] in self.SHORTENERS or any(s in domain for s in self.SHORTENERS):
            score += 10
            indicators.append("URL shortener")

        if parsed.scheme == 'http' and 'login' in domain:
            score += 15
            indicators.append("HTTP login page")

        port = parsed.port
        if port and port not in (80, 443):
            score += 8
            indicators.append(f"Non-standard port {port}")

        probability = min(score / 100, 1.0)
        is_phishing = probability > 0.35

        if is_phishing:
            self.threats_found += 1

        return {
            "is_phishing": is_phishing,
            "probability": round(probability, 3),
            "indicators": indicators,
            "score": min(score, 100),
            "domain": domain,
        }

    def scan_email_content(self, subject: str, body: str, sender: str) -> Dict:
        self.scan_count += 1
        indicators = []
        score = 0
        text = f"{subject} {body} {sender}".lower()

        urgent_words = ['urgent', 'immediately', 'suspended', 'verify now', 'act now',
                        'limited time', 'expires today', 'account locked', 'unauthorized',
                        'click here', 'confirm your identity', 'update your payment']
        for w in urgent_words:
            if w in text:
                score += 10
                indicators.append(f"Urgency phrase: '{w}'")

        phishing_links = re.findall(r'https?://[^\s<>"]+', body)
        if len(phishing_links) > 3:
            score += 15
            indicators.append(f"Multiple links ({len(phishing_links)})")

        for link in phishing_links:
            link_result = self.scan_url(link)
            if link_result["is_phishing"]:
                score += 20
                indicators.append(f"Phishing link: {link[:60]}")

        if sender:
            sender_domain = sender.split('@')[-1].strip('>').lower() if '@' in sender else ''
            if sender_domain and not any(d in sender_domain for d in ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'protonmail.com']):
                if any(imp in sender_domain for imp in ['paypa1', 'amaz0n', 'micros0ft', 'appl']):
                    score += 25
                    indicators.append(f"Spoofed sender domain: {sender_domain}")

        if re.search(r'\$\d+[\d,]*\.\d{2}', text):
            score += 5
            indicators.append("Money amount detected")

        if any(w in text for w in ['wire transfer', 'gift card', 'bitcoin', 'crypto wallet', 'send money']):
            score += 15
            indicators.append("Financial scam keywords")

        if re.search(r'<script|javascript:|data:', body, re.I):
            score += 30
            indicators.append("Executable content in email")

        probability = min(score / 100, 1.0)
        is_scam = probability > 0.3

        if is_scam:
            self.threats_found += 1

        return {
            "is_scam": is_scam,
            "probability": round(probability, 3),
            "indicators": indicators,
            "score": min(score, 100),
        }

    def get_stats(self):
        return {"total_scans": self.scan_count, "threats_found": self.threats_found}


phishing_service = PhishingService()
