(function () {
  "use strict";

  var PANEL_TITLES = {
    overview: "Overview",
    dataset: "Dataset",
    eda: "Exploratory Analysis",
    models: "Models",
    gpu: "GPU Performance",
    demo: "Live Analyzer",
    about: "Reports & About",
  };
  var DEFAULT_PANEL = "overview";

  // ---------- Panel router (sidebar-driven dashboard) ----------
  var panels = Array.prototype.slice.call(document.querySelectorAll(".panel"));
  var navItems = Array.prototype.slice.call(document.querySelectorAll(".nav-item"));
  var topbarTitle = document.getElementById("topbar-title");
  var sidebar = document.getElementById("sidebar");
  var sidebarBackdrop = document.getElementById("sidebar-backdrop");

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove("open");
    if (sidebarBackdrop) sidebarBackdrop.classList.remove("open");
  }

  function showPanel(name, opts) {
    opts = opts || {};
    if (!PANEL_TITLES.hasOwnProperty(name)) name = DEFAULT_PANEL;

    panels.forEach(function (p) {
      p.classList.toggle("active", p.getAttribute("data-panel") === name);
    });
    navItems.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-panel") === name);
    });
    if (topbarTitle) topbarTitle.textContent = PANEL_TITLES[name];

    if (!opts.skipScroll) {
      var main = document.querySelector(".panels");
      if (main) main.scrollTop = 0;
      window.scrollTo(0, 0);
    }
    if (!opts.skipHash) {
      history.replaceState(null, "", "#" + name);
    }
    closeSidebar();
    document.title = PANEL_TITLES[name] + " — CyberShield AI";
  }

  function panelFromHash() {
    var h = (location.hash || "").replace("#", "");
    return PANEL_TITLES.hasOwnProperty(h) ? h : DEFAULT_PANEL;
  }

  document.querySelectorAll("[data-panel-link], .nav-item").forEach(function (el) {
    el.addEventListener("click", function (e) {
      var target = el.getAttribute("data-panel") || el.getAttribute("data-panel-link");
      if (!target) return;
      e.preventDefault();
      showPanel(target);
    });
  });

  window.addEventListener("hashchange", function () {
    showPanel(panelFromHash(), { skipHash: true });
  });

  showPanel(panelFromHash(), { skipHash: true, skipScroll: true });

  // ---------- Mobile sidebar toggle ----------
  var sidebarToggle = document.getElementById("sidebar-toggle");
  var sidebarClose = document.getElementById("sidebar-close");
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.add("open");
      if (sidebarBackdrop) sidebarBackdrop.classList.add("open");
    });
  }
  if (sidebarClose) sidebarClose.addEventListener("click", closeSidebar);
  if (sidebarBackdrop) sidebarBackdrop.addEventListener("click", closeSidebar);

  // ---------- Scroll-reveal ----------
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  // ---------- Lightbox for chart images ----------
  var lightbox = document.getElementById("lightbox");
  var lightboxImg = document.getElementById("lightbox-img");
  if (lightbox && lightboxImg) {
    document.querySelectorAll("[data-lightbox]").forEach(function (img) {
      img.addEventListener("click", function () {
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add("open");
      });
    });
    lightbox.addEventListener("click", function () {
      lightbox.classList.remove("open");
      lightboxImg.src = "";
    });
  }

  // ---------- Network simulations ----------
  var heroSim = null;
  var demoSim = null;
  if (window.NetworkSim) {
    var heroCanvas = document.getElementById("hero-netsim");
    if (heroCanvas) {
      heroSim = new NetworkSim(heroCanvas, { sourceCount: 5, destCount: 2, ambientRate: 0.05 });
      heroSim.start();
    }
    var demoCanvas = document.getElementById("demo-netsim");
    if (demoCanvas) {
      demoSim = new NetworkSim(demoCanvas, { sourceCount: 4, destCount: 1, ambientRate: 0.02, speed: 1.3 });
      demoSim.start();
    }
  }

  // ---------- Analysis history (this browser only, via localStorage) ----------
  var HISTORY_KEY = "cybershield_analysis_history";
  var HISTORY_MAX = 20;

  function loadHistory() {
    try {
      var raw = localStorage.getItem(HISTORY_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function saveHistory(items) {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(items.slice(0, HISTORY_MAX)));
    } catch (e) { /* storage unavailable — history just won't persist */ }
  }

  function timeAgoLabel(ts) {
    var diff = Math.max(0, Date.now() - ts);
    var mins = Math.floor(diff / 60000);
    if (mins < 1) return "just now";
    if (mins < 60) return mins + "m ago";
    var hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + "h ago";
    return new Date(ts).toLocaleDateString();
  }

  function renderHistoryRow(item) {
    var row = document.createElement("div");
    row.className = "history-row";
    var isAttack = item.prediction === "Attack";
    row.innerHTML =
      '<span class="history-verdict ' + (isAttack ? "attack" : "benign") + '">' +
        (isAttack ? "🚨 Attack" : "🛡️ Benign") +
      "</span>" +
      '<span class="history-conf">' + (item.confidence * 100).toFixed(1) + "% confidence</span>" +
      '<span class="history-time">' + timeAgoLabel(item.ts) + "</span>";
    return row;
  }

  function renderHistory() {
    var items = loadHistory();
    var listEl = document.getElementById("history-list");
    var overviewEl = document.getElementById("overview-history");
    var countEl = document.getElementById("history-count");
    if (countEl) countEl.textContent = String(items.length);

    if (listEl) {
      listEl.innerHTML = "";
      if (items.length === 0) {
        listEl.innerHTML = '<p class="empty-note">Nothing analyzed yet this session — results you generate above will be logged here (stored only in your browser).</p>';
      } else {
        items.forEach(function (item) { listEl.appendChild(renderHistoryRow(item)); });
      }
    }
    if (overviewEl) {
      overviewEl.innerHTML = "";
      if (items.length === 0) {
        overviewEl.innerHTML = '<p class="empty-note">No analyses run yet this session. Try the <a href="#demo" data-panel-link="demo">Live Analyzer</a> to see results appear here.</p>';
      } else {
        items.slice(0, 5).forEach(function (item) { overviewEl.appendChild(renderHistoryRow(item)); });
      }
    }
    // re-bind any freshly-inserted panel links
    document.querySelectorAll("[data-panel-link]").forEach(function (el) {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", function (e) {
        var target = el.getAttribute("data-panel-link");
        if (!target) return;
        e.preventDefault();
        showPanel(target);
      });
    });

    var lastEl = document.getElementById("last-analysis-time");
    if (lastEl) {
      lastEl.textContent = items.length ? timeAgoLabel(items[0].ts) : "never";
    }
  }

  function logAnalysis(result) {
    var items = loadHistory();
    items.unshift({ prediction: result.prediction, confidence: result.confidence, ts: Date.now() });
    saveHistory(items);
    renderHistory();
  }

  var clearHistoryBtn = document.getElementById("clear-history");
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener("click", function () {
      saveHistory([]);
      renderHistory();
    });
  }

  renderHistory();
  setInterval(renderHistory, 60000); // keep "x ago" labels fresh

  // ---------- Live demo form ----------
  var form = document.getElementById("predict-form");
  var fieldsDataEl = document.getElementById("form-fields-data");
  var fields = fieldsDataEl ? JSON.parse(fieldsDataEl.textContent) : [];

  function applyPreset(kind) {
    fields.forEach(function (f) {
      var input = document.getElementById("f-" + f.name);
      if (!input) return;
      var val = kind === "attack" ? f.typical_attack : f.typical_benign;
      input.value = val;
    });
  }

  var presetBenignBtn = document.getElementById("preset-benign");
  var presetAttackBtn = document.getElementById("preset-attack");
  if (presetBenignBtn) presetBenignBtn.addEventListener("click", function () { applyPreset("benign"); });
  if (presetAttackBtn) presetAttackBtn.addEventListener("click", function () { applyPreset("attack"); });

  var resultEmpty = document.getElementById("result-empty");
  var analysisPanel = document.getElementById("analysis-panel");
  var analysisStatus = document.getElementById("analysis-status");
  var stepEls = analysisPanel ? Array.prototype.slice.call(analysisPanel.querySelectorAll(".steps li")) : [];
  var resultContent = document.getElementById("result-content");
  var verdictBox = document.getElementById("result-verdict");
  var verdictLabel = document.getElementById("verdict-label");
  var verdictSub = document.getElementById("verdict-sub");
  var resultIcon = document.getElementById("result-icon");
  var attackProbEl = document.getElementById("attack-prob");
  var benignProbEl = document.getElementById("benign-prob");
  var attackBar = document.getElementById("attack-bar");
  var benignBar = document.getElementById("benign-bar");
  var riskNote = document.getElementById("risk-note");
  var predictBtn = document.getElementById("predict-btn");

  var STEP_INTERVAL = 480; // ms between step activations

  function runStepper() {
    stepEls.forEach(function (el) { el.classList.remove("active", "done"); });
    var i = 0;
    function activate() {
      if (i > 0) stepEls[i - 1].classList.replace("active", "done");
      if (i < stepEls.length) {
        stepEls[i].classList.add("active");
        i++;
        setTimeout(activate, STEP_INTERVAL);
      }
    }
    activate();
  }

  function wait(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var payload = {};
      var valid = true;
      fields.forEach(function (f) {
        var input = document.getElementById("f-" + f.name);
        var v = parseFloat(input.value);
        if (isNaN(v) || v < 0) valid = false;
        payload[f.name] = v;
      });
      if (!valid) {
        alert("Please fill in all fields with non-negative numbers.");
        return;
      }

      predictBtn.disabled = true;
      predictBtn.textContent = "Analyzing…";
      resultEmpty.style.display = "none";
      resultContent.style.display = "none";
      analysisPanel.style.display = "flex";
      analysisStatus.textContent = "";
      if (demoSim) demoSim.burst(6, 0.35);
      runStepper();

      var slowNoticeTimer = setTimeout(function () {
        analysisStatus.textContent =
          "Still working — the free-tier server may be waking up from sleep (can take up to ~50s on the first request).";
      }, 6000);

      var minDuration = wait(stepEls.length * STEP_INTERVAL + 250);

      var fetchPromise = fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).then(function (res) {
        return res.json().then(function (data) { return { ok: res.ok, data: data }; });
      });

      Promise.all([fetchPromise, minDuration])
        .then(function (results) {
          var out = results[0];
          clearTimeout(slowNoticeTimer);
          predictBtn.disabled = false;
          predictBtn.textContent = "Analyze Traffic";

          if (!out.ok) {
            analysisPanel.style.display = "none";
            resultEmpty.style.display = "block";
            alert(out.data.error || "Prediction failed.");
            return;
          }

          var d = out.data;
          var isAttack = d.prediction === "Attack";

          if (demoSim) demoSim.burst(5, isAttack ? 0.85 : 0.05);

          stepEls.forEach(function (el) { el.classList.add("done"); el.classList.remove("active"); });
          analysisStatus.textContent = "Done.";

          setTimeout(function () {
            analysisPanel.style.display = "none";
            resultContent.style.display = "block";

            verdictBox.className = "result-verdict " + (isAttack ? "attack" : "benign");
            resultIcon.textContent = isAttack ? "🚨" : "🛡️";
            verdictLabel.textContent = isAttack ? "Attack Detected" : "Benign Traffic";
            verdictSub.textContent = "Confidence: " + (d.confidence * 100).toFixed(1) + "%";

            var attackPct = (d.attack_probability * 100).toFixed(1);
            var benignPct = (d.benign_probability * 100).toFixed(1);
            attackProbEl.textContent = attackPct + "%";
            benignProbEl.textContent = benignPct + "%";
            attackBar.style.width = attackPct + "%";
            benignBar.style.width = benignPct + "%";

            riskNote.textContent = "Risk level: " + d.risk_level;

            logAnalysis(d);
          }, 450);
        })
        .catch(function () {
          clearTimeout(slowNoticeTimer);
          predictBtn.disabled = false;
          predictBtn.textContent = "Analyze Traffic";
          analysisPanel.style.display = "none";
          resultEmpty.style.display = "block";
          alert("Could not reach the prediction service. Please try again — free-tier services can take up to a minute to wake up on the first request.");
        });
    });
  }
})();
