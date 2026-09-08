(function () {
  "use strict";
  var doc = document;
  var header = doc.querySelector(".site-header");
  var menuButton = doc.querySelector(".menu-button");
  var nav = doc.getElementById("primary-nav");
  var body = doc.body;
  var desktop = window.matchMedia("(min-width: 80rem)");

  function closeAllMenus(except) {
    doc.querySelectorAll(".nav-item.has-menu.is-open").forEach(function (item) {
      if (item !== except) {
        item.classList.remove("is-open");
        var t = item.querySelector(".nav-toggle");
        if (t) t.setAttribute("aria-expanded", "false");
      }
    });
  }

  if (menuButton && nav) {
    menuButton.addEventListener("click", function () {
      var open = body.classList.toggle("nav-open");
      menuButton.setAttribute("aria-expanded", open ? "true" : "false");
      menuButton.querySelector(".menu-label").textContent = open ? "Close" : "Menu";
      if (!open) closeAllMenus();
    });
  }

  doc.querySelectorAll(".nav-item.has-menu").forEach(function (item) {
    var toggle = item.querySelector(".nav-toggle");
    var link = item.querySelector(".nav-link");
    if (!toggle) return;
    toggle.addEventListener("click", function () {
      var open = !item.classList.contains("is-open");
      closeAllMenus(item);
      item.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    // Desktop: keyboard users open the panel with the toggle; pointer users hover.
    item.addEventListener("mouseenter", function () { if (desktop.matches) { closeAllMenus(item); item.classList.add("is-open"); toggle.setAttribute("aria-expanded", "true"); } });
    item.addEventListener("mouseleave", function () { if (desktop.matches) { item.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); } });
    item.addEventListener("focusout", function (e) {
      if (desktop.matches && !item.contains(e.relatedTarget)) { item.classList.remove("is-open"); toggle.setAttribute("aria-expanded", "false"); }
    });
    if (link) {
      link.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown") { e.preventDefault(); item.classList.add("is-open"); toggle.setAttribute("aria-expanded", "true"); var f = item.querySelector(".mega a"); if (f) f.focus(); }
      });
    }
  });

  doc.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var openItem = doc.querySelector(".nav-item.has-menu.is-open");
    if (openItem) {
      closeAllMenus();
      var l = openItem.querySelector(".nav-link");
      if (l) l.focus();
      return;
    }
    if (body.classList.contains("nav-open")) {
      body.classList.remove("nav-open");
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.querySelector(".menu-label").textContent = "Menu";
      menuButton.focus();
    }
  });

  desktop.addEventListener("change", function () {
    body.classList.remove("nav-open");
    if (menuButton) { menuButton.setAttribute("aria-expanded", "false"); menuButton.querySelector(".menu-label").textContent = "Menu"; }
    closeAllMenus();
  });

  // Review aid: open the drawer when the URL hash is #menu (used for visual QA captures).
  if (window.location.hash === "#menu" && menuButton && !desktop.matches) { menuButton.click(); }

  // Sticky header shadow after the first scroll.
  var ticking = false;
  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        header.classList.toggle("is-scrolled", window.scrollY > 24);
        ticking = false;
      });
      ticking = true;
    }
  }
  if (header) { window.addEventListener("scroll", onScroll, { passive: true }); onScroll(); }

  // Preselect a form interest from ?interest= on the intake forms.
  var params = new URLSearchParams(window.location.search);
  var interest = params.get("interest");
  if (interest) {
    var map = {
      "modular-data-centers": "Modular Data Centers", "hyperscale-data-centers": "Hyperscale Data Centers", "ai-data-centers": "AI Data Centers",
      "power-generation": "Power Generation", "planning-feasibility": "Design & Build", "commissioning": "Design & Build", "design-build": "Design & Build",
      "data-center-construction": "Design & Build", "expansions-retrofits": "Design & Build", "colocation": "Design & Build", "enterprise": "Design & Build",
      "edge": "Other", "maintenance": "Service & Maintenance"
    };
    var select = doc.querySelector('select[name="interest"], select[name="service-interest"]');
    var value = map[interest];
    if (select && value) {
      Array.prototype.forEach.call(select.options, function (o) { if (o.text === value) select.value = o.text; });
    }
  }

  // Native validation with a visible summary for assistive technology.
  doc.querySelectorAll("form.form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        var firstInvalid = form.querySelector(":invalid");
        form.classList.add("was-validated");
        if (firstInvalid) firstInvalid.focus();
      }
    });
  });
})();
