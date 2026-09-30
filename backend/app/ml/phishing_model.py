import re
import math
from typing import List, Tuple


class PhishingModel:
    def __init__(self):
        self.trained = True

    def extract_features(self, url: str) -> List[float]:
        parsed = url.lower()
        features = [
            len(url),
            url.count('.'),
            url.count('-'),
            url.count('@'),
            url.count('//'),
            url.count('http') + url.count('https'),
            1 if re.match(r'^https?://\d+\.\d+\.\d+\.\d+', url) else 0,
            len(parsed.split('/')[2]) if len(parsed.split('/')) > 2 else 0,
            sum(1 for c in url if c.isdigit()),
            sum(1 for c in url if c in '?&=%+'),
            1 if any(w in parsed for w in ['login', 'signin', 'verify', 'account', 'bank']) else 0,
            1 if any(parsed.endswith(t) for t in ['.xyz', '.top', '.tk', '.ml', '.ga', '.cf']) else 0,
            url.count('/') - 2 if url.count('/') > 2 else 0,
            1 if '@' in url else 0,
            len(url) - len(url.replace(' ', '')),
            1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        ]
        return features

    def predict(self, url: str) -> Tuple[bool, float, List[str]]:
        features = self.extract_features(url)
        indicators = []
        score = 0

        if features[0] > 100:
            score += 15
            indicators.append("Long URL")
        if features[1] > 4:
            score += 10
            indicators.append("Many dots")
        if features[2] > 3:
            score += 10
            indicators.append("Many hyphens")
        if features[3] > 0:
            score += 30
            indicators.append("Contains @")
        if features[5] > 1:
            score += 10
            indicators.append("Multiple protocol strings")
        if features[6] > 0:
            score += 40
            indicators.append("IP-based URL")
        if features[9] > 2:
            score += 10
            indicators.append("Special characters")
        if features[10] > 0:
            score += 15
            indicators.append("Suspicious keyword")
        if features[11] > 0:
            score += 25
            indicators.append("Suspicious TLD")
        if features[14] > 0:
            score += 15
            indicators.append("URL encoding present")

        probability = min(score / 100, 1.0)
        return probability > 0.35, probability, indicators


phishing_model = PhishingModel()
