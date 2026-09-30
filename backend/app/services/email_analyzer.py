"""
Email Analyzer Service for AI Digital Bodyguard
Analyzes email content for phishing attempts, suspicious links, and scam language
"""

import re
from typing import Dict, List, Optional
from urllib.parse import urlparse
import tldextract

class EmailAnalyzer:
    """Analyzes email content for security threats"""
    
    def __init__(self):
        # Suspicious keywords for phishing
        self.phishing_keywords = [
            'verify your account',
            'confirm your identity',
            'urgent action required',
            'your account will be closed',
            'click here immediately',
            'password expired',
            'security alert',
            'unusual activity',
            'suspended account',
            'update payment information',
            'verify your information',
            'confirm your details',
            'account verification',
            'security verification',
            'unauthorized access',
            'account compromised',
            'immediate action',
            'act now',
            'limited time',
            'expire soon',
            'confirm subscription',
            'unsubscribe',
            'winning notification',
            'congratulations',
            'you have been selected',
            'claim your prize',
            'lottery winner',
            'inheritance',
            'nigerian',
            'western union',
            'money transfer',
            'wire transfer',
            'bank details',
            'credit card',
            'social security',
            'ssn',
            'tax refund',
            'irs',
            'government',
            'official notice',
            'legal action',
            'court order',
            'police',
            'fbi',
            'investigation',
            'fraud',
            'scam',
            'phishing'
        ]
        
        # Suspicious TLDs
        self.suspicious_tlds = [
            '.xyz', '.top', '.tk', '.ml', '.ga', '.cf', '.gq',
            '.cc', '.pw', '.club', '.online', '.site', '.win',
            '.bid', '.trade', '.download', '.racing', '.loan'
        ]
        
        # Legitimate domains (whitelist)
        self.legitimate_domains = [
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'facebook.com', 'twitter.com', 'linkedin.com', 'paypal.com',
            'ebay.com', 'netflix.com', 'spotify.com', 'adobe.com',
            'dropbox.com', 'github.com', 'gitlab.com', 'atlassian.com',
            'salesforce.com', 'oracle.com', 'ibm.com', 'cisco.com',
            'intel.com', 'amd.com', 'nvidia.com', 'samsung.com'
        ]
    
    def analyze_email(self, email_data: Dict) -> Dict:
        """
        Analyze email content for security threats
        
        Args:
            email_data: Dictionary containing email subject, sender, body, etc.
        
        Returns:
            Dictionary with analysis results
        """
        subject = email_data.get('subject', '')
        sender = email_data.get('sender', '')
        body = email_data.get('body', '')
        url = email_data.get('url', '')
        
        # Extract all components
        full_text = f"{subject} {sender} {body}".lower()
        
        # Initialize analysis
        analysis = {
            'is_phishing': False,
            'is_suspicious': False,
            'threat_level': 'safe',  # safe, suspicious, dangerous
            'confidence': 0.0,
            'indicators': [],
            'links': [],
            'attachments': [],
            'sender_analysis': {},
            'content_analysis': {}
        }
        
        # Analyze sender
        sender_analysis = self._analyze_sender(sender)
        analysis['sender_analysis'] = sender_analysis
        
        # Analyze content
        content_analysis = self._analyze_content(full_text, body)
        analysis['content_analysis'] = content_analysis
        
        # Extract and analyze links
        links = self._extract_links(body)
        link_analysis = self._analyze_links(links)
        analysis['links'] = link_analysis
        
        # Analyze attachments (if any)
        attachments = email_data.get('attachments', [])
        attachment_analysis = self._analyze_attachments(attachments)
        analysis['attachments'] = attachment_analysis
        
        # Calculate overall threat score
        threat_score = self._calculate_threat_score(
            sender_analysis,
            content_analysis,
            link_analysis,
            attachment_analysis
        )
        
        analysis['confidence'] = threat_score
        
        # Determine threat level
        if threat_score > 0.7:
            analysis['threat_level'] = 'dangerous'
            analysis['is_phishing'] = True
        elif threat_score > 0.4:
            analysis['threat_level'] = 'suspicious'
            analysis['is_suspicious'] = True
        else:
            analysis['threat_level'] = 'safe'
        
        # Collect all indicators
        analysis['indicators'] = self._collect_indicators(
            sender_analysis,
            content_analysis,
            link_analysis,
            attachment_analysis
        )
        
        return analysis
    
    def _analyze_sender(self, sender: str) -> Dict:
        """Analyze email sender for suspicious patterns"""
        analysis = {
            'is_suspicious': False,
            'indicators': [],
            'domain': '',
            'display_name': '',
            'email_address': ''
        }
        
        if not sender:
            return analysis
        
        # Extract email address
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', sender)
        if email_match:
            email = email_match.group(0)
            analysis['email_address'] = email
            
            # Extract domain
            domain = email.split('@')[1].lower()
            analysis['domain'] = domain
            
            # Check for suspicious TLD
            ext = tldextract.extract(domain)
            if ext.suffix in self.suspicious_tlds:
                analysis['is_suspicious'] = True
                analysis['indicators'].append(f'Suspicious TLD: {ext.suffix}')
            
            # Check for spoofed legitimate domains
            for legit_domain in self.legitimate_domains:
                if legit_domain in domain and domain != legit_domain:
                    analysis['is_suspicious'] = True
                    analysis['indicators'].append(f'Possible domain spoofing: {domain}')
            
            # Check for random-looking domains
            if self._is_random_domain(domain):
                analysis['is_suspicious'] = True
                analysis['indicators'].append('Random-looking domain')
        
        # Extract display name
        display_match = re.search(r'"?([^"<]+)"?\s*<', sender)
        if display_match:
            analysis['display_name'] = display_match.group(1).strip()
        
        return analysis
    
    def _analyze_content(self, full_text: str, body: str) -> Dict:
        """Analyze email content for suspicious patterns"""
        analysis = {
            'is_suspicious': False,
            'indicators': [],
            'keyword_matches': [],
            'urgency_indicators': 0,
            'pressure_indicators': 0
        }
        
        # Check for phishing keywords
        keyword_matches = []
        for keyword in self.phishing_keywords:
            if keyword in full_text:
                keyword_matches.append(keyword)
        
        analysis['keyword_matches'] = keyword_matches
        
        if len(keyword_matches) > 2:
            analysis['is_suspicious'] = True
            analysis['indicators'].append(f'Multiple phishing keywords: {len(keyword_matches)}')
        
        # Check for urgency indicators
        urgency_words = ['urgent', 'immediately', 'asap', 'right now', 'today', 'expire', 'deadline']
        urgency_count = sum(1 for word in urgency_words if word in full_text)
        analysis['urgency_indicators'] = urgency_count
        
        if urgency_count > 2:
            analysis['is_suspicious'] = True
            analysis['indicators'].append(f'High urgency language: {urgency_count} indicators')
        
        # Check for pressure tactics
        pressure_words = ['account will be closed', 'legal action', 'police', 'fraud', 'investigation']
        pressure_count = sum(1 for phrase in pressure_words if phrase in full_text)
        analysis['pressure_indicators'] = pressure_count
        
        if pressure_count > 0:
            analysis['is_suspicious'] = True
            analysis['indicators'].append(f'Pressure tactics detected: {pressure_count}')
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in body if c.isupper()) / len(body) if body else 0
        if caps_ratio > 0.3:
            analysis['is_suspicious'] = True
            analysis['indicators'].append('Excessive capitalization')
        
        # Check for excessive exclamation marks
        exclamation_count = body.count('!')
        if exclamation_count > 5:
            analysis['is_suspicious'] = True
            analysis['indicators'].append(f'Excessive exclamation marks: {exclamation_count}')
        
        return analysis
    
    def _extract_links(self, text: str) -> List[str]:
        """Extract all URLs from text"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return re.findall(url_pattern, text)
    
    def _analyze_links(self, links: List[str]) -> List[Dict]:
        """Analyze extracted links for suspicious patterns"""
        analyzed_links = []
        
        for link in links:
            link_analysis = {
                'url': link,
                'is_suspicious': False,
                'indicators': []
            }
            
            try:
                parsed = urlparse(link)
                domain = parsed.netloc.lower()
                
                # Check for suspicious TLD
                ext = tldextract.extract(domain)
                if ext.suffix in self.suspicious_tlds:
                    link_analysis['is_suspicious'] = True
                    link_analysis['indicators'].append(f'Suspicious TLD: {ext.suffix}')
                
                # Check for IP address
                if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
                    link_analysis['is_suspicious'] = True
                    link_analysis['indicators'].append('IP address in URL')
                
                # Check for URL shorteners
                shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly']
                if any(shortener in domain for shortener in shorteners):
                    link_analysis['is_suspicious'] = True
                    link_analysis['indicators'].append('URL shortener detected')
                
                # Check for suspicious subdomains
                subdomain_count = domain.count('.') - 1
                if subdomain_count > 3:
                    link_analysis['is_suspicious'] = True
                    link_analysis['indicators'].append('Too many subdomains')
                
                # Check for suspicious keywords in URL
                suspicious_keywords = ['login', 'signin', 'verify', 'account', 'secure', 'bank']
                if any(keyword in domain for keyword in suspicious_keywords):
                    link_analysis['is_suspicious'] = True
                    link_analysis['indicators'].append('Suspicious keyword in domain')
                
            except Exception as e:
                link_analysis['indicators'].append(f'Error parsing URL: {str(e)}')
            
            analyzed_links.append(link_analysis)
        
        return analyzed_links
    
    def _analyze_attachments(self, attachments: List[str]) -> List[Dict]:
        """Analyze email attachments for suspicious patterns"""
        analyzed_attachments = []
        
        dangerous_extensions = [
            '.exe', '.scr', '.bat', '.cmd', '.com', '.pif',
            '.vbs', '.js', '.jse', '.wsf', '.wsh', '.msi',
            '.zip', '.rar', '.7z', '.tar', '.gz'
        ]
        
        for attachment in attachments:
            attachment_analysis = {
                'filename': attachment,
                'is_suspicious': False,
                'indicators': []
            }
            
            # Check extension
            ext = attachment.lower().split('.')[-1] if '.' in attachment else ''
            if f'.{ext}' in dangerous_extensions:
                attachment_analysis['is_suspicious'] = True
                attachment_analysis['indicators'].append(f'Dangerous file extension: .{ext}')
            
            # Check for double extensions
            if attachment.count('.') > 1:
                attachment_analysis['is_suspicious'] = True
                attachment_analysis['indicators'].append('Double extension detected')
            
            # Check for suspicious filenames
            suspicious_names = ['invoice', 'receipt', 'payment', 'document', 'urgent']
            if any(name in attachment.lower() for name in suspicious_names):
                attachment_analysis['is_suspicious'] = True
                attachment_analysis['indicators'].append('Suspicious filename pattern')
            
            analyzed_attachments.append(attachment_analysis)
        
        return analyzed_attachments
    
    def _calculate_threat_score(self, sender_analysis: Dict, content_analysis: Dict, 
                                 link_analysis: List[Dict], attachment_analysis: List[Dict]) -> float:
        """Calculate overall threat score (0.0 to 1.0)"""
        score = 0.0
        
        # Sender analysis (weight: 0.3)
        if sender_analysis.get('is_suspicious'):
            score += 0.3 * len(sender_analysis.get('indicators', [])) / 3
        
        # Content analysis (weight: 0.3)
        if content_analysis.get('is_suspicious'):
            score += 0.3 * (content_analysis.get('urgency_indicators', 0) + 
                           content_analysis.get('pressure_indicators', 0)) / 5
        
        # Link analysis (weight: 0.3)
        suspicious_links = [link for link in link_analysis if link.get('is_suspicious')]
        if suspicious_links:
            score += 0.3 * len(suspicious_links) / max(len(link_analysis), 1)
        
        # Attachment analysis (weight: 0.1)
        suspicious_attachments = [att for att in attachment_analysis if att.get('is_suspicious')]
        if suspicious_attachments:
            score += 0.1 * len(suspicious_attachments) / max(len(attachment_analysis), 1)
        
        return min(score, 1.0)
    
    def _collect_indicators(self, sender_analysis: Dict, content_analysis: Dict,
                           link_analysis: List[Dict], attachment_analysis: List[Dict]) -> List[str]:
        """Collect all indicators from all analyses"""
        indicators = []
        
        indicators.extend(sender_analysis.get('indicators', []))
        indicators.extend(content_analysis.get('indicators', []))
        
        for link in link_analysis:
            if link.get('is_suspicious'):
                indicators.extend(link.get('indicators', []))
        
        for attachment in attachment_analysis:
            if attachment.get('is_suspicious'):
                indicators.extend(attachment.get('indicators', []))
        
        return list(set(indicators))  # Remove duplicates
    
    def _is_random_domain(self, domain: str) -> bool:
        """Check if domain looks randomly generated"""
        # Simple heuristic: check for random character sequences
        import random
        import string
        
        # Remove common words
        common_words = ['mail', 'email', 'service', 'support', 'info', 'contact']
        for word in common_words:
            domain = domain.replace(word, '')
        
        # Check if remaining part looks random
        if len(domain) > 10:
            # Calculate character diversity
            unique_chars = len(set(domain))
            if unique_chars > len(domain) * 0.7:
                return True
        
        return False

# Global instance
email_analyzer = EmailAnalyzer()
