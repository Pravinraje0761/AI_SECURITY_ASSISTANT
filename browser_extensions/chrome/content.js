/**
 * Content Script for AI Digital Bodyguard Chrome Extension
 * Analyzes page content and communicates with background script
 */

// Check if page is an email client
function isEmailPage() {
  const url = window.location.href;
  const emailDomains = [
    'mail.google.com',
    'outlook.live.com',
    'outlook.office.com',
    'yahoo.com/mail',
    'mail.aol.com'
  ];
  
  return emailDomains.some(domain => url.includes(domain));
}

// Extract email content if on email page
function extractEmailContent() {
  if (!isEmailPage()) return null;
  
  try {
    // Gmail
    if (window.location.hostname.includes('mail.google.com')) {
      const emailBody = document.querySelector('.a3s.aiL')?.innerText;
      const emailSubject = document.querySelector('h2[data-thread-perm-id]')?.innerText;
      const emailSender = document.querySelector('.gD')?.innerText;
      
      if (emailBody) {
        return {
          subject: emailSubject || '',
          sender: emailSender || '',
          body: emailBody,
          url: window.location.href
        };
      }
    }
    
    // Outlook
    if (window.location.hostname.includes('outlook')) {
      const emailBody = document.querySelector('[role="article"]')?.innerText;
      const emailSubject = document.querySelector('.ms-Font-xl')?.innerText;
      
      if (emailBody) {
        return {
          subject: emailSubject || '',
          body: emailBody,
          url: window.location.href
        };
      }
    }
    
    return null;
  } catch (error) {
    console.error('Error extracting email content:', error);
    return null;
  }
}

// Analyze page text for suspicious content
function analyzePageText() {
  const bodyText = document.body.innerText;
  
  // Suspicious keywords
  const suspiciousKeywords = [
    'verify your account',
    'confirm your identity',
    'urgent action required',
    'your account will be closed',
    'click here immediately',
    'password expired',
    'security alert',
    'unusual activity',
    'suspended account',
    'update payment information'
  ];
  
  const foundKeywords = suspiciousKeywords.filter(keyword => 
    bodyText.toLowerCase().includes(keyword.toLowerCase())
  );
  
  // Check for fake login forms
  const passwordInputs = document.querySelectorAll('input[type="password"]');
  const loginForms = document.querySelectorAll('form');
  
  return {
    hasSuspiciousKeywords: foundKeywords.length > 0,
    suspiciousKeywords: foundKeywords,
    hasPasswordInput: passwordInputs.length > 0,
    hasLoginForm: loginForms.length > 0,
    pageText: bodyText.substring(0, 1000) // First 1000 chars
  };
}

// Inject warning banner if page is dangerous
function injectWarningBanner(result) {
  if (result.result !== 'malicious' && result.score < 0.6) return;
  
  // Check if banner already exists
  if (document.getElementById('ai-bodyguard-warning')) return;
  
  const banner = document.createElement('div');
  banner.id = 'ai-bodyguard-warning';
  banner.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: ${result.result === 'malicious' ? '#dc3545' : '#ffc107'};
    color: ${result.result === 'malicious' ? 'white' : 'black'};
    padding: 15px;
    z-index: 999999;
    text-align: center;
    font-family: Arial, sans-serif;
    font-size: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  `;
  
  banner.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <span style="font-size: 20px;">⚠️</span>
      <span><strong>AI Digital Bodyguard Warning:</strong> This page may be ${result.result === 'malicious' ? 'dangerous' : 'suspicious'}. Score: ${(result.score * 100).toFixed(0)}%</span>
      <button onclick="this.parentElement.parentElement.remove()" style="background: rgba(255,255,255,0.3); border: none; padding: 5px 10px; cursor: pointer; border-radius: 3px;">Dismiss</button>
    </div>
  `;
  
  document.body.insertBefore(banner, document.body.firstChild);
}

// Main initialization
function init() {
  // Get current URL
  const currentUrl = window.location.href;
  
  // Send URL to background for analysis
  chrome.runtime.sendMessage({
    action: 'scanUrl',
    url: currentUrl
  }, (result) => {
    if (result && !result.error) {
      injectWarningBanner(result);
    }
  });
  
  // If email page, analyze email content
  if (isEmailPage()) {
    const emailContent = extractEmailContent();
    if (emailContent) {
      chrome.runtime.sendMessage({
        action: 'scanEmail',
        emailData: emailContent
      });
    }
  }
}

// Run on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Listen for URL changes (SPA navigation)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    init();
  }
}).observe(document, { subtree: true, childList: true });
