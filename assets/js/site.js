// 공공공방 — 화면 모드 전환. 선택은 이 브라우저에만 남는다.
(function () {
  var root = document.documentElement;

  function store(key, value) {
    try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch (e) {}
  }

  // 저장값이 없으면 시스템 설정을 따른다. 버튼은 지금 보이는 모드의 반대로 바꾼다.
  // 메일 주소: 수집 봇을 피하려고 조각으로 두고 화면에서 합친다.
  var emails = document.querySelectorAll("[data-u][data-d][data-t]");
  for (var i = 0; i < emails.length; i++) {
    var el = emails[i];
    var addr = el.getAttribute("data-u") + "@" + el.getAttribute("data-d") + "." + el.getAttribute("data-t");
    var target = el.querySelector(".contact-value") || el;
    if (el.tagName === "A") {
      el.href = "mailto:" + addr;
      target.textContent = addr;
    } else {
      var a = document.createElement("a");
      a.href = "mailto:" + addr;
      a.textContent = addr;
      target.textContent = "";
      target.appendChild(a);
    }
  }

  var toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) return;
  var media = window.matchMedia("(prefers-color-scheme: dark)");

  function current() {
    var t = root.getAttribute("data-theme");
    if (t === "light" || t === "dark") return t;
    return media.matches ? "dark" : "light";
  }
  function reflect() { toggle.setAttribute("aria-pressed", current() === "dark" ? "true" : "false"); }
  function apply(next) {
    var system = media.matches ? "dark" : "light";
    if (next === system) { root.removeAttribute("data-theme"); store("theme", null); }
    else { root.setAttribute("data-theme", next); store("theme", next); }
    reflect();
  }

  reflect();
  toggle.addEventListener("click", function () { apply(current() === "dark" ? "light" : "dark"); });
  if (media.addEventListener) media.addEventListener("change", reflect);
})();
