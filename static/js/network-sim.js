/*
 * CyberShield AI — network packet-flow visualization.
 *
 * A lightweight, dependency-free canvas animation: source hosts on the left
 * send packets toward a central "CyberShield AI" analyzer node; benign
 * packets pass through to the protected network on the right, attack
 * packets are stopped (and briefly flash) at the analyzer.
 *
 * This is an illustrative visualization, not a capture of real traffic --
 * labeled as such wherever it appears on the page.
 */
(function (global) {
  "use strict";

  var REDUCED_MOTION =
    global.matchMedia && global.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function NetworkSim(canvas, opts) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.opts = Object.assign(
      {
        sourceCount: 4,
        destCount: 2,
        ambientRate: 0.045, // avg new packets per frame at rest
        attackRatio: 0.22, // matches the real ~21.95% attack share
        speed: 1,
      },
      opts || {}
    );

    this.packets = [];
    this.bursts = [];
    this.running = false;
    this.visible = true;
    this._raf = null;
    this._lastT = 0;

    this._resize = this._resize.bind(this);
    this._tick = this._tick.bind(this);

    this._resize();
    global.addEventListener("resize", this._resize);

    if ("IntersectionObserver" in global) {
      this._io = new IntersectionObserver(
        function (entries) {
          this.visible = entries[0].isIntersecting;
        }.bind(this),
        { threshold: 0.05 }
      );
      this._io.observe(canvas);
    }

    this._layout();
  }

  NetworkSim.prototype._resize = function () {
    var rect = this.canvas.parentElement.getBoundingClientRect();
    var dpr = Math.min(global.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.floor(rect.width));
    var h = Math.max(1, Math.floor(this.canvas.getAttribute("data-height") || rect.height || 220));
    this.canvas.width = w * dpr;
    this.canvas.height = h * dpr;
    this.canvas.style.width = w + "px";
    this.canvas.style.height = h + "px";
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.w = w;
    this.h = h;
    this._layout();
  };

  NetworkSim.prototype._layout = function () {
    var w = this.w || 600;
    var h = this.h || 220;
    var pad = 34;
    var srcN = this.opts.sourceCount;
    var dstN = this.opts.destCount;

    this.hub = { x: w * 0.5, y: h * 0.5 };

    this.sources = [];
    for (var i = 0; i < srcN; i++) {
      var t = srcN === 1 ? 0.5 : i / (srcN - 1);
      this.sources.push({ x: pad, y: pad + t * (h - pad * 2) });
    }

    this.dests = [];
    for (var j = 0; j < dstN; j++) {
      var t2 = dstN === 1 ? 0.5 : j / (dstN - 1);
      this.dests.push({ x: w - pad, y: pad + t2 * (h - pad * 2) });
    }
  };

  NetworkSim.prototype.start = function () {
    if (this.running) return;
    this.running = true;
    if (REDUCED_MOTION) {
      this._drawStatic();
      return;
    }
    this._lastT = performance.now();
    this._raf = requestAnimationFrame(this._tick);
  };

  NetworkSim.prototype.stop = function () {
    this.running = false;
    if (this._raf) cancelAnimationFrame(this._raf);
  };

  // Spawn an intensified, deterministic-ish burst of packets used for the
  // "Analyze Traffic" moment. `attackRatio` in [0,1] biases how many
  // packets get flagged red (blocked) vs green (passed).
  NetworkSim.prototype.burst = function (count, attackRatio) {
    var ratio = attackRatio == null ? this.opts.attackRatio : attackRatio;
    for (var i = 0; i < count; i++) {
      var delay = i * (140 + Math.random() * 90);
      setTimeout(
        function (isAttack) {
          this._spawn(isAttack);
        }.bind(this, Math.random() < ratio),
        delay
      );
    }
    if (REDUCED_MOTION) this._drawStatic();
  };

  NetworkSim.prototype._spawn = function (isAttack) {
    var src = this.sources[Math.floor(Math.random() * this.sources.length)];
    this.packets.push({
      x: src.x,
      y: src.y,
      leg: 0, // 0 = travelling to hub, 1 = travelling to dest (benign only)
      attack: isAttack,
      progress: 0,
      speed: 0.012 + Math.random() * 0.006,
      dest: this.dests[Math.floor(Math.random() * this.dests.length)],
      src: src,
    });
  };

  NetworkSim.prototype._tick = function (t) {
    if (!this.running) return;
    var dt = Math.min(48, t - this._lastT);
    this._lastT = t;

    if (this.visible) {
      if (Math.random() < this.opts.ambientRate) {
        this._spawn(Math.random() < this.opts.attackRatio);
      }
      this._update(dt);
      this._draw();
    }
    this._raf = requestAnimationFrame(this._tick);
  };

  NetworkSim.prototype._update = function (dt) {
    var next = [];
    for (var i = 0; i < this.packets.length; i++) {
      var p = this.packets[i];
      p.progress += p.speed * (dt / 16.67) * this.opts.speed;

      if (p.leg === 0 && p.progress >= 1) {
        if (p.attack) {
          this.bursts.push({ x: this.hub.x, y: this.hub.y, r: 4, alpha: 1 });
          continue; // packet stops at hub
        }
        p.leg = 1;
        p.progress = 0;
      } else if (p.leg === 1 && p.progress >= 1) {
        continue; // reached destination, drop it
      }
      next.push(p);
    }
    this.packets = next;

    var nb = [];
    for (var j = 0; j < this.bursts.length; j++) {
      var b = this.bursts[j];
      b.r += 1.6;
      b.alpha -= 0.055;
      if (b.alpha > 0) nb.push(b);
    }
    this.bursts = nb;
  };

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  NetworkSim.prototype._drawBase = function () {
    var ctx = this.ctx;
    var w = this.w,
      h = this.h;
    ctx.clearRect(0, 0, w, h);

    // connecting lines
    ctx.strokeStyle = "rgba(148,163,184,0.14)";
    ctx.lineWidth = 1;
    this.sources.forEach(
      function (s) {
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(this.hub.x, this.hub.y);
        ctx.stroke();
      }.bind(this)
    );
    this.dests.forEach(
      function (d) {
        ctx.beginPath();
        ctx.moveTo(this.hub.x, this.hub.y);
        ctx.lineTo(d.x, d.y);
        ctx.stroke();
      }.bind(this)
    );

    // source nodes
    ctx.fillStyle = "rgba(148,163,184,0.55)";
    this.sources.concat(this.dests).forEach(
      function (n) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, 4, 0, Math.PI * 2);
        ctx.fill();
      }
    );

    // hub (analyzer)
    var grad = ctx.createRadialGradient(this.hub.x, this.hub.y, 2, this.hub.x, this.hub.y, 22);
    grad.addColorStop(0, "rgba(34,211,238,0.35)");
    grad.addColorStop(1, "rgba(34,211,238,0)");
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(this.hub.x, this.hub.y, 22, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#22d3ee";
    ctx.beginPath();
    ctx.arc(this.hub.x, this.hub.y, 6, 0, Math.PI * 2);
    ctx.fill();
  };

  NetworkSim.prototype._draw = function () {
    this._drawBase();
    var ctx = this.ctx;

    this.packets.forEach(
      function (p) {
        var from = p.leg === 0 ? p.src : this.hub;
        var to = p.leg === 0 ? this.hub : p.dest;
        var x = lerp(from.x, to.x, p.progress);
        var y = lerp(from.y, to.y, p.progress);
        var color = p.attack ? "#f43f5e" : "#34d399";
        ctx.fillStyle = color;
        ctx.shadowColor = color;
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }.bind(this)
    );

    this.bursts.forEach(function (b) {
      ctx.strokeStyle = "rgba(244,63,94," + Math.max(b.alpha, 0) + ")";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
      ctx.stroke();
    });
  };

  NetworkSim.prototype._drawStatic = function () {
    // A calm, non-animated frame for prefers-reduced-motion.
    this.packets = [
      { x: this.sources[0].x, y: this.sources[0].y, leg: 0, progress: 0.5, attack: false, src: this.sources[0], dest: this.dests[0] },
      { x: this.sources[2 % this.sources.length].x, y: this.sources[2 % this.sources.length].y, leg: 1, progress: 0.4, attack: false, src: this.sources[0], dest: this.dests[0] },
    ];
    this._draw();
  };

  global.NetworkSim = NetworkSim;
})(window);
