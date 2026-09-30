const API_BASE = "http://127.0.0.1:8000";

(function () {
  function injectWarning(result) {
    if (document.getElementById("__bodyguard_warning")) return;
    const div = document.createElement("div");
    div.id = "__bodyguard_warning";
    div.style.cssText = "position:fixed;top:0;left:0;right:0;z-index:999999;padding:12px 20px;font-family:sans-serif;font-size:14px;font-weight:bold;text-align:center;";
    if (result.result === "dangerous") {
      div.style.background = "#4a0000";
      div.style.color = "#ff4444";
      div.textContent = "WARNING: This website has been flagged as dangerous by AI Digital Bodyguard! Score: " + ((result.score||0)*100).toFixed(0) + "%";
    } else if (result.result === "suspicious") {
      div.style.background = "#4a3a00";
      div.style.color = "#ffaa00";
      div.textContent = "CAUTION: This website may be suspicious. Score: " + ((result.score||0)*100).toFixed(0) + "%";
    } else {
      return;
    }
    const closeBtn = document.createElement("span");
    closeBtn.textContent = " X";
    closeBtn.style.cssText = "cursor:pointer;margin-left:20px;";
    closeBtn.onclick = () => div.remove();
    div.appendChild(closeBtn);
    document.body.prepend(div);
  }

  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === "SHOW_WARNING") {
      injectWarning(msg.result);
    }
  });
})();
