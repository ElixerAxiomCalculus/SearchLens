chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.action === "classifySnippet") {
    try {
      const response = await fetch("https://your-proxy.onrender.com/api/nli", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: request.snippet })
      });
      const data = await response.json();
      sendResponse({ label: data.label, scores: data.scores });
    } catch (error) {
      sendResponse({ label: "Error", scores: {} });
    }
    return true;
  }
});
