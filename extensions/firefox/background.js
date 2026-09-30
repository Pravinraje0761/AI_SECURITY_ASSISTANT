const API_BASE = "http://127.0.0.1:8000";

let token = null;

chrome.storage.local.get(["bodyguard_token"], (result) => {
  token = result.bodyguard_token || null;
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "CHECK_URL") {
    checkUrl(msg.url, msg.browser || "chrome").then(sendResponse);
    return true;
  }
  if (msg.type === "SET_TOKEN") {
    token = msg.token;
    chrome.storage.local.set({ bodyguard_token: token });
    sendResponse({ ok: true });
    return true;
  }
  if (msg.type === "GET_STATUS") {
    sendResponse({ token: !!token, api: API_BASE });
    return true;
  }
});

async function checkUrl(url, browser) {
  if (!token) return { result: "unknown", error: "Not authenticated" };
  try {
    const r = await fetch(`${API_BASE}/api/v1/protection/check-url`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ url, browser }),
    });
    if (!r.ok) return { result: "error", error: `HTTP ${r.status}` };
    return await r.json();
  } catch (e) {
    return { result: "error", error: e.message };
  }
}

chrome.webNavigation.onCompleted.addListener(async (details) => {
  if (details.frameId !== 0) return;
  if (!token) return;
  const tab = await chrome.tabs.get(details.tabId);
  const url = tab.url;
  if (!url || url.startsWith("chrome://") || url.startsWith("about:")) return;

  const result = await checkUrl(url, "chrome");
  if (result.result === "dangerous" || (result.score && result.score > 0.5)) {
    chrome.tabs.sendMessage(details.tabId, {
      type: "SHOW_WARNING",
      result: result,
    });
    chrome.action.setIcon({ tabId: details.tabId, path: "icon_red.png" });
  } else if (result.result === "suspicious" || (result.score && result.score > 0.3)) {
    chrome.action.setIcon({ tabId: details.tabId, path: "icon_yellow.png" });
  }
});
