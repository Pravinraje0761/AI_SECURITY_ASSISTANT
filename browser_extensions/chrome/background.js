/**
 * Background Service Worker for AI Digital Bodyguard Chrome Extension
 * Handles API communication and background processing
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Store scan results
let scanResults = new Map();

// Listen for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    analyzeUrl(tab.url, tabId);
  }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scanUrl') {
    analyzeUrl(request.url, sender.tab?.id)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true; // Keep message channel open for async response
  }
  
  if (request.action === 'scanEmail') {
    analyzeEmail(request.emailData)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true;
  }
  
  if (request.action === 'getScanResult') {
    sendResponse(scanResults.get(request.url) || null);
  }
});

// Analyze URL for phishing
async function analyzeUrl(url, tabId) {
  try {
    const response = await fetch(`${API_BASE_URL}/scan/url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'phishing',
        target: url
      })
    });
    
    const result = await response.json();
    
    // Store result
    scanResults.set(url, result);
    
    // Show notification if dangerous
    if (result.result === 'malicious' || result.score > 0.6) {
      showWarning(tabId, result);
    }
    
    // Update badge
    updateBadge(tabId, result);
    
    return result;
  } catch (error) {
    console.error('Error analyzing URL:', error);
    return { error: error.message };
  }
}

// Analyze email content
async function analyzeEmail(emailData) {
  try {
    const response = await fetch(`${API_BASE_URL}/scan/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type: 'email',
        target: emailData
      })
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error analyzing email:', error);
    return { error: error.message };
  }
}

// Show warning notification
function showWarning(tabId, result) {
  const alertType = result.result === 'malicious' ? 'dangerous' : 'suspicious';
  
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icons/icon128.png',
    title: `AI Digital Bodyguard - ${alertType.toUpperCase()} Warning`,
    message: `This ${alertType === 'dangerous' ? 'site' : 'page'} may be ${alertType}. Score: ${(result.score * 100).toFixed(0)}%`,
    priority: 2
  });
}

// Update badge based on scan result
function updateBadge(tabId, result) {
  const score = result.score || 0;
  
  let color = '#00FF00'; // Green
  let text = '';
  
  if (score > 0.8) {
    color = '#FF0000'; // Red
    text = '!';
  } else if (score > 0.5) {
    color = '#FFA500'; // Orange
    text = '?';
  }
  
  chrome.action.setBadgeBackgroundColor({ color: color });
  chrome.action.setBadgeText({ text: text, tabId: tabId });
}

// Install handler
chrome.runtime.onInstalled.addListener(() => {
  console.log('AI Digital Bodyguard extension installed');
  
  // Set default settings
  chrome.storage.local.set({
    enabled: true,
    autoScan: true,
    showNotifications: true
  });
});
