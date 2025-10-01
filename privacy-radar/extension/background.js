function setBadge(score) {
  const s = Math.max(0, Math.min(99, Math.round(score)));
  const color = s <= 30 ? "#34a853" : s <= 60 ? "#fbbc05" : "#ea4335";
  chrome.action.setBadgeText({ text: String(s) });
  chrome.action.setBadgeBackgroundColor({ color });
}
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "SET_BADGE") setBadge(msg.score);
});
