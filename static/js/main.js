(function () {
  "use strict";

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

      fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
        .then(function (out) {
          predictBtn.disabled = false;
          predictBtn.textContent = "Analyze Traffic";

          if (!out.ok) {
            alert(out.data.error || "Prediction failed.");
            return;
          }

          var d = out.data;
          resultEmpty.style.display = "none";
          resultContent.style.display = "block";

          var isAttack = d.prediction === "Attack";
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
        })
        .catch(function () {
          predictBtn.disabled = false;
          predictBtn.textContent = "Analyze Traffic";
          alert("Could not reach the prediction service. Please try again.");
        });
    });
  }

  // ---------- Mobile nav (simple anchor smooth-scroll close, no-op placeholder) ----------
})();
