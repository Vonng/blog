
(function () {
  function nav(dir) {
    if (window.parent && window.parent !== window) {
      window.parent.postMessage({ type: "deck-nav", dir: dir }, "*");
    }
  }
  function isInteractiveTarget(target) {
    return target && target.closest && target.closest("input, textarea, select, [contenteditable='true'], [role='textbox']");
  }
  document.addEventListener("keydown", function (event) {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    if (isInteractiveTarget(event.target)) return;
    if (event.key === "ArrowRight" || event.key === "PageDown" || event.key === " ") {
      event.preventDefault();
      event.stopImmediatePropagation();
      nav("next");
    }
    if (event.key === "ArrowLeft" || event.key === "PageUp" || (event.key === " " && event.shiftKey)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      nav("prev");
    }
  }, true);
})();
