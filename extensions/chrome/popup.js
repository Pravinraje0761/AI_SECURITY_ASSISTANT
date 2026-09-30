const API_BASE = "http://127.0.0.1:8000";

const emailEl = document.getElementById("email");
const passEl = document.getElementById("password");
const loginBtn = document.getElementById("loginBtn");
const authSection = document.getElementById("auth-section");
const mainSection = document.getElementById("main-section");
const currentUrl = document.getElementById("current-url");
const scanBtn = document.getElementById("scanBtn");
const manualUrl = document.getElementById("manual-url");
const manualScanBtn = document.getElementById("manualScanBtn");
const indicatorsDiv = document.getElementById("indicators");

function showIndicators(indicators) {
  if (!indicators || indicators.length === 0) {
    indicatorsDiv.innerHTML = "<p>No suspicious indicators</p>";
    return;
  }
  indicatorsDiv.innerHTML = "<ul>" + indicators.map(i => `<li>${i}</li>`).join("") + "</ul>";
}

function setStatus(result, score) {
  currentUrl.className = "status " + result;
  const pct = ((score || 0) * 100).toFixed(0);
  if (result === "dangerous") {
    currentUrl.textContent = `DANGEROUS - Risk: ${pct}%`;
  } else if (result === "suspicious") {
    currentUrl.textContent = `SUSPICIOUS - Risk: ${pct}%`;
  } else if (result === "safe") {
    currentUrl.textContent = `SAFE - Risk: ${pct}%`;
  } else {
    currentUrl.textContent = "Unknown";
  }
}

chrome.storage.local.get(["bodyguard_token"], async (res) => {
  if (res.bodyguard_token) {
    authSection.style.display = "none";
    mainSection.style.display = "block";
    await scanCurrentTab();
  }
});

loginBtn.addEventListener("click", async () => {
  try {
    const r = await fetch(`${API_BASE}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `username=${encodeURIComponent(emailEl.value)}&password=${encodeURIComponent(passEl.value)}`,
    });
    if (!r.ok) throw new Error("Login failed");
    const data = await r.json();
    chrome.runtime.sendMessage({ type: "SET_TOKEN", token: data.access_token });
    authSection.style.display = "none";
    mainSection.style.display = "block";
    await scanCurrentTab();
  } catch (e) {
    alert("Login failed: " + e.message);
  }
});

async function scanCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url || tab.url.startsWith("chrome://")) {
    setStatus("unknown", 0);
    return;
  }
  currentUrl.textContent = "Scanning...";
  chrome.runtime.sendMessage({ type: "CHECK_URL", url: tab.url, browser: "chrome" }, (result) => {
    if (result && result.result) {
      setStatus(result.result, result.score);
      showIndicators(result.indicators);
    }
  });
}

scanBtn.addEventListener("click", scanCurrentTab);

manualScanBtn.addEventListener("click", async () => {
  const url = manualUrl.value.trim();
  if (!url) return;
  currentUrl.textContent = "Scanning...";
  chrome.runtime.sendMessage({ type: "CHECK_URL", url, browser: "chrome" }, (result) => {
    if (result && result.result) {
      setStatus(result.result, result.score);
      showIndicators(result.indicators);
    }
  });
});
