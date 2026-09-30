/**
 * Popup Script for AI Digital Bodyguard Chrome Extension
 * Handles popup UI and interactions
 */

// DOM Elements
const statusIndicator = document.getElementById('statusIndicator');
const currentUrl = document.getElementById('currentUrl');
const scanResult = document.getElementById('scanResult');
const pagesScanned = document.getElementById('pagesScanned');
const threatsBlocked = document.getElementById('threatsBlocked');
const scanBtn = document.getElementById('scanBtn');
const dashboardBtn = document.getElementById('dashboardBtn');
const settingsBtn = document.getElementById('settingsBtn');
const helpLink = document.getElementById('helpLink');

// State
let stats = {
  pagesScanned: 0,
  threatsBlocked: 0
};

// Initialize
async function init() {
  // Load stats from storage
  const storedStats = await chrome.storage.local.get(['pagesScanned', 'threatsBlocked']);
  stats.pagesScanned = storedStats.pagesScanned || 0;
  stats.threatsBlocked = storedStats.threatsBlocked || 0;
  
  updateStats();
  
  // Get current tab URL
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.url) {
    currentUrl.textContent = truncateUrl(tab.url, 50);
    
    // Get scan result from background
    chrome.runtime.sendMessage(
      { action: 'getScanResult', url: tab.url },
      (result) => {
        if (result) {
          displayScanResult(result);
        } else {
          scanResult.innerHTML = `
            <span class="result-icon">⏳</span>
            <span class="result-text">Not scanned yet</span>
          `;
        }
      }
    );
  }
  
  // Setup event listeners
  setupEventListeners();
}

function setupEventListeners() {
  // Scan button
  scanBtn.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url) {
      scanResult.innerHTML = `
        <span class="result-icon">⏳</span>
        <span class="result-text">Scanning...</span>
      `;
      
      chrome.runtime.sendMessage(
        { action: 'scanUrl', url: tab.url },
        (result) => {
          if (result && !result.error) {
            displayScanResult(result);
            stats.pagesScanned++;
            if (result.result === 'malicious') {
              stats.threatsBlocked++;
            }
            updateStats();
            saveStats();
          }
        }
      );
    }
  });
  
  // Dashboard button
  dashboardBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:8000/docs' });
  });
  
  // Settings button
  settingsBtn.addEventListener('click', () => {
    chrome.tabs.create({ url: 'chrome://extensions/?id=' + chrome.runtime.id });
  });
  
  // Help link
  helpLink.addEventListener('click', (e) => {
    e.preventDefault();
    chrome.tabs.create({ url: 'https://github.com/your-repo/ai-digital-bodyguard' });
  });
}

function displayScanResult(result) {
  const score = result.score || 0;
  const isMalicious = result.result === 'malicious';
  const isSuspicious = score > 0.5 && score < 0.8;
  
  let icon, text, color;
  
  if (isMalicious) {
    icon = '🚨';
    text = 'Dangerous';
    color = '#dc3545';
  } else if (isSuspicious) {
    icon = '⚠️';
    text = 'Suspicious';
    color = '#ffc107';
  } else {
    icon = '✅';
    text = 'Safe';
    color = '#28a745';
  }
  
  scanResult.innerHTML = `
    <span class="result-icon">${icon}</span>
    <span class="result-text" style="color: ${color}">${text} (${(score * 100).toFixed(0)}%)</span>
  `;
  
  // Update status indicator
  if (isMalicious) {
    statusIndicator.querySelector('.status-dot').style.backgroundColor = '#dc3545';
    statusIndicator.querySelector('.status-text').textContent = 'Threat Detected';
  } else if (isSuspicious) {
    statusIndicator.querySelector('.status-dot').style.backgroundColor = '#ffc107';
    statusIndicator.querySelector('.status-text').textContent = 'Suspicious Activity';
  } else {
    statusIndicator.querySelector('.status-dot').style.backgroundColor = '#28a745';
    statusIndicator.querySelector('.status-text').textContent = 'Protected';
  }
}

function updateStats() {
  pagesScanned.textContent = stats.pagesScanned;
  threatsBlocked.textContent = stats.threatsBlocked;
}

function saveStats() {
  chrome.storage.local.set({
    pagesScanned: stats.pagesScanned,
    threatsBlocked: stats.threatsBlocked
  });
}

function truncateUrl(url, maxLength) {
  if (url.length <= maxLength) return url;
  return url.substring(0, maxLength) + '...';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
