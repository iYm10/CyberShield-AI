# -*- coding: utf-8 -*-
"""
CyberShield AI — website & live prediction demo.

Serves a single-page research showcase for the CyberShield AI project
(GPU-accelerated network intrusion detection on CIC-IDS2017) and a small
JSON API backing an interactive "Live Demo" prediction form.

Run locally:
    pip install -r requirements.txt
    python app.py

Deploy: see render.yaml (Render free-tier web service, gunicorn app:app).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request

import site_data as data

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "ml_model"

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load the demo model + feature schema once at startup.
# ---------------------------------------------------------------------------
_model = None
_schema = None


def _load_model():
    global _model, _schema
    if _model is None:
        _model = joblib.load(MODEL_DIR / "model.pkl")
    if _schema is None:
        _schema = json.loads((MODEL_DIR / "feature_schema.json").read_text(encoding="utf-8"))
    return _model, _schema


FEATURE_LABELS = {
    "bwd_packet_length_std": "Backward Packet Length — Std Dev (bytes)",
    "bwd_packet_length_mean": "Backward Packet Length — Mean (bytes)",
    "bwd_packet_length_max": "Backward Packet Length — Max (bytes)",
    "packet_length_std": "Packet Length — Std Dev (bytes)",
    "max_packet_length": "Max Packet Length in Flow (bytes)",
    "packet_length_variance": "Packet Length — Variance",
    "avg_bytes_per_packet": "Avg. Bytes per Packet (engineered)",
    "fwd_bwd_packet_ratio": "Forward / Backward Packet Ratio (engineered)",
}


@app.route("/")
def index():
    model, schema = _load_model()
    features = schema["features"]
    form_fields = [
        {
            "name": f,
            "label": FEATURE_LABELS.get(f, f),
            "typical_benign": schema["feature_ranges"][f]["typical_benign"],
            "typical_attack": schema["feature_ranges"][f]["typical_attack"],
            "max_suggested": schema["feature_ranges"][f]["max_suggested"],
        }
        for f in features
    ]
    return render_template(
        "index.html",
        hero_stats=data.HERO_STATS,
        dataset_stats=data.DATASET_STATS,
        model_results=data.MODEL_RESULTS,
        confusion=data.CONFUSION_MATRIX_RF,
        workflow_metrics=data.WORKFLOW_METRICS,
        cpu_gpu=data.CPU_GPU_COMPARISON,
        top_correlations=data.TOP_CORRELATIONS,
        engineered_features=data.ENGINEERED_FEATURES,
        charts=data.CHARTS,
        tech_stack=data.TECH_STACK,
        author=data.AUTHOR,
        repo_url=data.REPO_URL,
        notebook_url=data.NOTEBOOK_URL,
        report_url=data.REPORT_URL,
        limitations=data.LIMITATIONS,
        form_fields=form_fields,
        demo_metrics=schema["demo_model_metrics"],
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/predict", methods=["POST"])
def predict():
    model, schema = _load_model()
    features = schema["features"]

    payload = request.get_json(silent=True) or {}
    values = []
    for f in features:
        raw = payload.get(f)
        try:
            v = float(raw)
        except (TypeError, ValueError):
            return jsonify({"error": f"Missing or invalid value for '{f}'."}), 400
        if v < 0:
            return jsonify({"error": f"'{f}' cannot be negative."}), 400
        values.append(v)

    X = np.array([values], dtype="float64")
    proba = model.predict_proba(X)[0]
    # class order follows model.classes_ (0 = Benign, 1 = Attack)
    classes = list(model.classes_)
    attack_idx = classes.index(1)
    benign_idx = classes.index(0)
    attack_prob = float(proba[attack_idx])
    benign_prob = float(proba[benign_idx])

    prediction = "Attack" if attack_prob >= 0.5 else "Benign"
    confidence = max(attack_prob, benign_prob)

    if attack_prob < 0.25:
        risk_level = "Low"
    elif attack_prob < 0.5:
        risk_level = "Elevated"
    elif attack_prob < 0.75:
        risk_level = "High"
    else:
        risk_level = "Critical"

    return jsonify(
        {
            "prediction": prediction,
            "attack_probability": round(attack_prob, 4),
            "benign_probability": round(benign_prob, 4),
            "confidence": round(confidence, 4),
            "risk_level": risk_level,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
