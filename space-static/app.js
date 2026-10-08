/* UI glue for the Shora static demo. All analysis happens locally in shora.js. */
(function () {
  "use strict";
  var I = SHORA_I18N, $ = function (id) { return document.getElementById(id); };
  var engine = null, lang = "en", last = null;
  try { lang = localStorage.getItem("shora-lang") || "en"; } catch (e) {}
  if (!I.ui[lang]) lang = "en";

  function t(k) { return (I.ui[lang] && I.ui[lang][k]) || I.ui.en[k] || ""; }

  function applyLang() {
    document.documentElement.lang = lang === "pcm" ? "pcm" : lang;
    document.querySelectorAll("[data-t]").forEach(function (el) {
      var k = el.getAttribute("data-t");
      if (el.id === "check") k = engine ? "check" : "loading";
      el.textContent = t(k);
    });
    document.querySelectorAll("[data-ph]").forEach(function (el) { el.placeholder = t(el.getAttribute("data-ph")); });
    document.querySelectorAll("#langs .chip").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
    });
    if (last) render(last);
  }

  function buildLangs() {
    var box = $("langs");
    I.langs.forEach(function (l) {
      var b = document.createElement("button");
      b.className = "chip"; b.type = "button"; b.dataset.lang = l[0]; b.textContent = l[1];
      b.addEventListener("click", function () {
        lang = l[0];
        try { localStorage.setItem("shora-lang", lang); } catch (e) {}
        applyLang();
      });
      box.appendChild(b);
    });
  }

  function buildExamples() {
    var box = $("examples");
    I.examples.forEach(function (ex) {
      var b = document.createElement("button");
      b.className = "chip"; b.type = "button"; b.textContent = ex[0]; b.title = ex[1];
      b.addEventListener("click", function () {
        $("msg").value = ex[1];
        run();
        var res = $("result");
        if (res.scrollIntoView) res.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      box.appendChild(b);
    });
  }

  function pct(p) { return Math.round(p * 100) + "%"; }

  function render(r) {
    var isScam = r.label === "scam";
    var caution = !isScam && r.verdict !== "legit";      // model says safe but rules push risk up
    var v = $("verdict");
    v.className = "verdict " + (isScam ? "v-scam" : caution ? "v-warn" : "v-safe");
    $("vIcon").textContent = isScam ? "🚨" : caution ? "⚠️" : "✅";
    $("vTitle").textContent = I.verdict[lang][r.label];
    $("vPct").textContent = pct(r.scam_probability);
    $("vBar").style.width = Math.max(3, Math.round(r.scam_probability * 100)) + "%";
    $("careful").style.display = caution ? "block" : "none";

    var ty = I.types[r.scam_type] || ["❔", r.scam_type];
    $("tIcon").textContent = ty[0];
    $("tName").textContent = ty[1];
    $("tPct").textContent = pct(r.type_probability);

    var ul = $("flags");
    ul.innerHTML = "";
    if (!r.red_flags.length) {
      var li = document.createElement("li"); li.textContent = t("noFlags"); ul.appendChild(li);
    }
    r.red_flags.forEach(function (f) {
      var li = document.createElement("li"), b = document.createElement("b"), q = document.createElement("q");
      b.textContent = "🚩 " + f.flag; q.textContent = f.evidence.trim();
      li.appendChild(b); li.appendChild(q); ul.appendChild(li);
    });

    var key;
    if (isScam || caution) key = I.advice[r.scam_type] ? r.scam_type : "_scam";
    else key = "_legit";
    $("advice").textContent = I.advice[key][lang];
    $("result").classList.add("show");
  }

  function run() {
    var text = $("msg").value.trim();
    if (!engine) return;
    if (!text) { $("msg").focus(); $("msg").placeholder = t("empty"); return; }
    last = engine.predict(text);
    render(last);
  }

  window.__shoraReady = function () {
    try {
      engine = new Shora.Engine(SHORA_MODEL);
      $("check").disabled = false;
      applyLang();
    } catch (e) { $("check").textContent = "Model failed to load"; console.error(e); }
  };

  buildLangs();
  buildExamples();
  applyLang();
  $("check").addEventListener("click", run);
  $("clear").addEventListener("click", function () {
    $("msg").value = ""; last = null; $("result").classList.remove("show"); $("msg").focus();
  });
  $("msg").addEventListener("keydown", function (e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) run();
  });
  if (typeof SHORA_MODEL !== "undefined") window.__shoraReady();
})();
