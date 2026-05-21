
(function () {
  function go(href) {
    if (href) window.location.href = href;
  }
  function isInteractiveTarget(target) {
    return target && target.closest && target.closest("input, textarea, select, button, [contenteditable='true'], [role='textbox']");
  }
  document.addEventListener("keydown", function (event) {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    if (isInteractiveTarget(event.target)) return;
    var key = event.key;
    var prev = document.body.dataset.prev;
    var next = document.body.dataset.next;
    if (key === "ArrowRight" || key === " " || key === "PageDown") {
      event.preventDefault();
      go(next);
    }
    if (key === "ArrowLeft" || key === "PageUp" || (key === " " && event.shiftKey)) {
      event.preventDefault();
      go(prev);
    }
    if (key === "Home") {
      event.preventDefault();
      go(document.body.dataset.first);
    }
    if (key === "End") {
      event.preventDefault();
      go(document.body.dataset.last);
    }
  });
  window.addEventListener("message", function (event) {
    var data = event.data || {};
    if (data.type !== "deck-nav") return;
    if (data.dir === "prev") go(document.body.dataset.prev);
    if (data.dir === "next") go(document.body.dataset.next);
  });
})();
