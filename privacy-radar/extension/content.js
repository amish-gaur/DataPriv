function findPolicyLinks() {
  const anchors = [...document.querySelectorAll("a[href]")];
  const pat = /(privacy|terms|policy|cookie|gdpr|ccpa)/i;
  const urls = anchors
    .filter(a => pat.test(a.textContent) || pat.test(a.href))
    .map(a => new URL(a.getAttribute("href"), location.href).toString());
  return [...new Set(urls)].slice(0, 8);
}
chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  console.log("📋 Content script received message:", msg);
  if (msg.type === "GET_POLICY_LINKS") {
    const links = findPolicyLinks();
    console.log("🔗 Found policy links:", links);
    sendResponse({ domain: location.hostname, links: links });
  }
});
