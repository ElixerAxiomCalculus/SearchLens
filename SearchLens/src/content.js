function addBadge(el, label) {
  if (el.querySelector('.searchlens-badge')) return;
  const badge = document.createElement('span');
  badge.className = 'searchlens-badge';
  badge.innerText = label;
  badge.style.cssText = "background:#36db96;color:#fff;border-radius:12px;padding:2px 10px;margin-left:10px;font-size:12px;font-weight:600;vertical-align:middle;";
  el.appendChild(badge);
}

function processResults() {
  const results = document.querySelectorAll('div.g');
  results.forEach(async result => {
    const title = result.querySelector('h3');
    const snippet = result.querySelector('.VwiC3b, .aCOpRe, .gL9Hy');
    if (!title || !snippet) return;
    if (title.querySelector('.searchlens-badge')) return;
    const snippetText = snippet.innerText.trim();
    if (!snippetText) return;

    chrome.runtime.sendMessage(
      { action: "classifySnippet", snippet: snippetText },
      response => {
        if (response && response.label) {
          addBadge(title, response.label);
        }
      }
    );
  });
}

let observer = new MutationObserver(processResults);
observer.observe(document.body, { childList: true, subtree: true });

processResults();
