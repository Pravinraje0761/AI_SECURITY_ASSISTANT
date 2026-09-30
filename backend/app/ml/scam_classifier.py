import re
from typing import List, Tuple


class ScamClassifier:
    SCAM_KEYWORDS = {
        'urgent': 3, 'immediately': 3, 'suspended': 3, 'verify now': 4,
        'act now': 3, 'limited time': 2, 'expires today': 2, 'congratulations': 3,
        'you won': 4, 'claim your prize': 5, 'click here': 2, 'wire transfer': 4,
        'gift card': 3, 'bitcoin': 2, 'send money': 5, 'nigerian prince': 5,
        'bank transfer': 3, 'social security': 3, 'tax refund': 2, 'lottery': 4,
        'inheritance': 3, 'beneficiary': 3, 'urgent request': 3, 'business proposal': 3,
        'confidential': 2, 'do not share': 2, 'account compromised': 4,
        'unauthorized access': 3, 'confirm identity': 3, 'update payment': 3,
    }

    def predict(self, text: str) -> Tuple[str, float, List[str]]:
        text_lower = text.lower()
        indicators = []
        score = 0

        for keyword, weight in self.SCAM_KEYWORDS.items():
            if keyword in text_lower:
                score += weight
                indicators.append(f"Scam phrase: '{keyword}'")

        if re.search(r'\$\d[\d,]*\.?\d*', text):
            score += 2
            indicators.append("Monetary amount")

        if re.search(r'wire\s+(transfer|money)', text_lower):
            score += 4
            indicators.append("Wire transfer request")

        if re.search(r'https?://[^\s]+', text):
            links = re.findall(r'https?://[^\s]+', text)
            if len(links) > 3:
                score += 2
                indicators.append(f"Many links ({len(links)})")

        if re.search(r'(act|respond|click)\s+now', text_lower):
            score += 3
            indicators.append("Immediate action pressure")

        if re.search(r'don\'t?\s+tell\s+anyone|keep\s+(this|it)\s+(quiet|secret|confidential)', text_lower):
            score += 4
            indicators.append("Secrecy request")

        probability = min(score / 30, 1.0)

        if probability >= 0.6:
            label = "scam"
        elif probability >= 0.3:
            label = "suspicious"
        else:
            label = "safe"

        return label, probability, indicators


scam_classifier = ScamClassifier()
