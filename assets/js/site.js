// 공공공방 — 화면 모드 전환과 공지 닫기. 저장은 이 브라우저에만 남는다.
(function () {
  var root = document.documentElement;

  function store(key, value) {
    try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch (e) {}
  }
  function load(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  // 화면 모드: 저장값이 없으면 시스템 설정을 따른다. 버튼은 지금 보이는 모드의 반대로 바꾼다.
  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    var media = window.matchMedia("(prefers-color-scheme: dark)");
    function current() {
      var t = root.getAttribute("data-theme");
      if (t === "light" || t === "dark") return t;
      return media.matches ? "dark" : "light";
    }
    function apply(next) {
      var system = media.matches ? "dark" : "light";
      if (next === system) { root.removeAttribute("data-theme"); store("theme", null); }
      else { root.setAttribute("data-theme", next); store("theme", next); }
      toggle.setAttribute("aria-pressed", next === "dark" ? "true" : "false");
    }
    toggle.setAttribute("aria-pressed", current() === "dark" ? "true" : "false");
    toggle.addEventListener("click", function () { apply(current() === "dark" ? "light" : "dark"); });
    if (media.addEventListener) media.addEventListener("change", function () {
      toggle.setAttribute("aria-pressed", current() === "dark" ? "true" : "false");
    });
  }

  // 공지: 닫은 id 는 기억해 두고 다시 보이지 않는다.
  var bar = document.querySelector(".notice-bar");
  if (bar) {
    var id = bar.getAttribute("data-notice-id") || "";
    if (load("notice-dismissed") !== id) bar.hidden = false;
    var close = bar.querySelector("[data-notice-close]");
    if (close) close.addEventListener("click", function () { bar.hidden = true; store("notice-dismissed", id); });
  }
})();
