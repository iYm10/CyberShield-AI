"""
generate_data.py
-----------------
Builds every static results file used by the CyberShield AI Streamlit app.

All numbers below are copied verbatim from the executed outputs of
`CyberShield_AI.ipynb` (RAPIDS cuDF / cuML run on a Tesla T4 GPU) and from
the project README — nothing here is invented. Run this once if you ever
need to regenerate the `data/*.csv` and `data/*.json` files:

    python data/generate_data.py
"""

import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. Source files discovered from the CIC-IDS2017 Kaggle dataset (Cell 14)
# ---------------------------------------------------------------------------
source_files = pd.DataFrame([
    {"file": "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", "size_mb": 73.55},
    {"file": "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv", "size_mb": 73.34},
    {"file": "Friday-WorkingHours-Morning.pcap_ISCX.csv", "size_mb": 55.62},
    {"file": "Monday-WorkingHours.pcap_ISCX.csv", "size_mb": 168.73},
    {"file": "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv", "size_mb": 79.25},
    {"file": "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv", "size_mb": 49.61},
    {"file": "Tuesday-WorkingHours.pcap_ISCX.csv", "size_mb": 128.82},
    {"file": "Wednesday-workingHours.pcap_ISCX.csv", "size_mb": 214.74},
])
source_files.to_csv(OUT / "source_files.csv", index=False)

# ---------------------------------------------------------------------------
# 2. Detailed multi-class label distribution (Cell 20 / 23 output)
# ---------------------------------------------------------------------------
label_distribution = pd.DataFrame([
    {"label": "BENIGN", "count": 1125098},
    {"label": "DoS Hulk", "count": 122530},
    {"label": "PortScan", "count": 114678},
    {"label": "DDoS", "count": 114258},
    {"label": "FTP-Patator", "count": 7063},
    {"label": "DoS slowloris", "count": 5126},
    {"label": "DoS Slowhttptest", "count": 4895},
    {"label": "SSH-Patator", "count": 2649},
    {"label": "Bot", "count": 1749},
    {"label": "Web Attack - Brute Force", "count": 1326},
    {"label": "Web Attack - XSS", "count": 582},
    {"label": "Infiltration", "count": 29},
    {"label": "Web Attack - Sql Injection", "count": 17},
])
label_distribution.to_csv(OUT / "label_distribution.csv", index=False)

# ---------------------------------------------------------------------------
# 3. Binary target distribution (Cell 32 output)
# ---------------------------------------------------------------------------
binary_distribution = pd.DataFrame([
    {"traffic_class": "Benign", "count": 1072232},
    {"traffic_class": "Attack", "count": 301570},
])
binary_distribution.to_csv(OUT / "binary_distribution.csv", index=False)

# ---------------------------------------------------------------------------
# 4. Dataset / cleaning / split summary (Cells 18, 22, 26, 28, 43, 45, 46)
# ---------------------------------------------------------------------------
dataset_summary = {
    "source_files": 8,
    "rows_loaded": 1500000,
    "original_columns": 80,
    "duplicates_removed": 126198,
    "rows_after_dedup": 1373802,
    "constant_features_removed": 8,
    "numeric_features_retained": 70,
    "engineered_features_added": 2,
    "final_feature_count": 72,
    "final_rows": 1373802,
    "benign_records": 1072232,
    "attack_records": 301570,
    "attack_share_percent": 21.95,
    "training_rows_before_balancing": 1099041,
    "testing_rows": 274761,
    "training_benign_before_balancing": 857773,
    "training_attack_before_balancing": 241268,
    "training_rows_after_balancing": 965072,
    "training_benign_after_balancing": 723804,
    "training_attack_after_balancing": 241268,
    "max_benign_to_attack_ratio": 3.0,
    "test_size": 0.20,
    "random_state": 42,
}
with open(OUT / "dataset_summary.json", "w", encoding="utf-8") as f:
    json.dump(dataset_summary, f, indent=2)

# ---------------------------------------------------------------------------
# 5. Top-15 features correlated with is_attack (Cell 36 output, exact values)
# ---------------------------------------------------------------------------
feature_correlations = pd.DataFrame([
    {"feature": "bwd_packet_length_std", "abs_correlation": 0.577005},
    {"feature": "bwd_packet_length_mean", "abs_correlation": 0.562562},
    {"feature": "avg_bwd_segment_size", "abs_correlation": 0.562562},
    {"feature": "bwd_packet_length_max", "abs_correlation": 0.561920},
    {"feature": "packet_length_std", "abs_correlation": 0.533636},
    {"feature": "max_packet_length", "abs_correlation": 0.513703},
    {"feature": "packet_length_variance", "abs_correlation": 0.503395},
    {"feature": "avg_bytes_per_packet", "abs_correlation": 0.500532},
    {"feature": "average_packet_size", "abs_correlation": 0.491874},
    {"feature": "packet_length_mean", "abs_correlation": 0.490435},
    {"feature": "fwd_iat_std", "abs_correlation": 0.440008},
    {"feature": "idle_max", "abs_correlation": 0.404208},
    {"feature": "flow_iat_max", "abs_correlation": 0.398607},
    {"feature": "fwd_iat_max", "abs_correlation": 0.397947},
    {"feature": "idle_mean", "abs_correlation": 0.397259},
])
feature_correlations.to_csv(OUT / "feature_correlations.csv", index=False)

# ---------------------------------------------------------------------------
# 6. 8x8 correlation heatmap matrix for the top features (Cell 40 output)
# ---------------------------------------------------------------------------
corr_features = [
    "bwd_packet_length_std", "bwd_packet_length_mean", "avg_bwd_segment_size",
    "bwd_packet_length_max", "packet_length_std", "max_packet_length",
    "packet_length_variance", "avg_bytes_per_packet", "is_attack",
]
corr_values = {
    "bwd_packet_length_std":  [1.000000, 0.942326, 0.942326, 0.983133, 0.934998, 0.923546, 0.888651, 0.859375, 0.577005],
    "bwd_packet_length_mean": [0.942326, 1.000000, 1.000000, 0.959172, 0.911050, 0.895399, 0.789568, 0.921598, 0.562562],
    "avg_bwd_segment_size":   [0.942326, 1.000000, 1.000000, 0.959172, 0.911050, 0.895399, 0.789568, 0.921598, 0.562562],
    "bwd_packet_length_max":  [0.983133, 0.959172, 0.959172, 1.000000, 0.931303, 0.938314, 0.850077, 0.881867, 0.561920],
    "packet_length_std":      [0.934998, 0.911050, 0.911050, 0.931303, 1.000000, 0.983644, 0.929730, 0.951074, 0.533636],
    "max_packet_length":      [0.923546, 0.895399, 0.895399, 0.938314, 0.983644, 1.000000, 0.899363, 0.919600, 0.513703],
    "packet_length_variance": [0.888651, 0.789568, 0.789568, 0.850077, 0.929730, 0.899363, 1.000000, 0.828974, 0.503395],
    "avg_bytes_per_packet":   [0.859375, 0.921598, 0.921598, 0.881867, 0.951074, 0.919600, 0.828974, 1.000000, 0.500532],
    "is_attack":              [0.577005, 0.562562, 0.562562, 0.561920, 0.533636, 0.513703, 0.503395, 0.500532, 1.000000],
}
correlation_matrix = pd.DataFrame(corr_values, index=corr_features)
correlation_matrix.to_csv(OUT / "correlation_matrix.csv")

# ---------------------------------------------------------------------------
# 7. Engineered feature comparison — median of log1p(value) by class (Cell 38)
# ---------------------------------------------------------------------------
engineered_feature_comparison = pd.DataFrame([
    {"feature": "avg_bytes_per_packet", "benign_log_median": 4.247066, "attack_log_median": 6.682860},
    {"feature": "fwd_bwd_packet_ratio", "benign_log_median": 0.693147, "attack_log_median": 0.693147},
])
engineered_feature_comparison.to_csv(OUT / "engineered_feature_comparison.csv", index=False)

# ---------------------------------------------------------------------------
# 8. Model comparison table (Cell 58 output, exact values)
# ---------------------------------------------------------------------------
model_comparison = pd.DataFrame([
    {
        "model": "cuML Random Forest", "accuracy": 0.998046, "precision": 0.996577,
        "recall": 0.994511, "f1_score": 0.995543,
        "train_time_seconds": 18.286441, "inference_time_seconds": 0.311667,
        "train_avg_gpu_util_percent": 97.244444, "train_max_gpu_util_percent": 100.0,
        "train_avg_memory_used_mb": 4972.676389, "train_max_memory_used_mb": 4974.1875,
        "inference_avg_gpu_util_percent": 18.0, "inference_max_gpu_util_percent": 18.0,
        "inference_avg_memory_used_mb": 4702.1875, "inference_max_memory_used_mb": 4702.1875,
    },
    {
        "model": "cuML Logistic Regression", "accuracy": 0.946892, "precision": 0.870469,
        "recall": 0.890534, "f1_score": 0.880388,
        "train_time_seconds": 2.693004, "inference_time_seconds": 0.063987,
        "train_avg_gpu_util_percent": 66.230769, "train_max_gpu_util_percent": 83.0,
        "train_avg_memory_used_mb": 4860.802885, "train_max_memory_used_mb": 4882.1875,
        "inference_avg_gpu_util_percent": None, "inference_max_gpu_util_percent": None,
        "inference_avg_memory_used_mb": None, "inference_max_memory_used_mb": None,
    },
    {
        "model": "cuML Linear SVC", "accuracy": 0.940257, "precision": 0.860931,
        "recall": 0.867998, "f1_score": 0.864450,
        "train_time_seconds": 0.225556, "inference_time_seconds": 0.027167,
        "train_avg_gpu_util_percent": 10.000000, "train_max_gpu_util_percent": 10.0,
        "train_avg_memory_used_mb": 4910.187500, "train_max_memory_used_mb": 4910.1875,
        "inference_avg_gpu_util_percent": None, "inference_max_gpu_util_percent": None,
        "inference_avg_memory_used_mb": None, "inference_max_memory_used_mb": None,
    },
]).sort_values("f1_score", ascending=False).reset_index(drop=True)
model_comparison.to_csv(OUT / "model_comparison.csv", index=False)

# ---------------------------------------------------------------------------
# 9. Per-model confusion matrices + classification reports (Cells 52, 54, 56)
# ---------------------------------------------------------------------------
confusion_matrices = {
    "cuML Random Forest": {
        "matrix": [[214253, 206], [331, 59971]],
        "labels": ["Benign", "Attack"],
        "report": {
            "Benign": {"precision": 0.9985, "recall": 0.9990, "f1": 0.9987, "support": 214459},
            "Attack": {"precision": 0.9966, "recall": 0.9945, "f1": 0.9955, "support": 60302},
            "accuracy": 0.9980,
        },
    },
    "cuML Logistic Regression": {
        "matrix": [[206468, 7991], [6601, 53701]],
        "labels": ["Benign", "Attack"],
        "report": {
            "Benign": {"precision": 0.9690, "recall": 0.9627, "f1": 0.9659, "support": 214459},
            "Attack": {"precision": 0.8705, "recall": 0.8905, "f1": 0.8804, "support": 60302},
            "accuracy": 0.9469,
        },
    },
    "cuML Linear SVC": {
        "matrix": [[206004, 8455], [7960, 52342]],
        "labels": ["Benign", "Attack"],
        "report": {
            "Benign": {"precision": 0.9628, "recall": 0.9606, "f1": 0.9617, "support": 214459},
            "Attack": {"precision": 0.8609, "recall": 0.8680, "f1": 0.8644, "support": 60302},
            "accuracy": 0.9403,
        },
    },
}
with open(OUT / "confusion_matrices.json", "w", encoding="utf-8") as f:
    json.dump(confusion_matrices, f, indent=2)

# ---------------------------------------------------------------------------
# 10. Workflow-level GPU metrics (Cell 69 output)
# ---------------------------------------------------------------------------
workflow_metrics = pd.DataFrame([
    {"operation": "Data Loading (cuDF)", "time_seconds": 2.99, "avg_gpu_percent": 21.00, "max_gpu_percent": 48.0, "avg_memory_mb": 1739.11, "max_memory_mb": 4166.19},
    {"operation": "Data Cleaning (cuDF)", "time_seconds": 3.53, "avg_gpu_percent": 30.88, "max_gpu_percent": 55.0, "avg_memory_mb": 2945.83, "max_memory_mb": 3212.19},
    {"operation": "Feature Scaling (cuML)", "time_seconds": 2.30, "avg_gpu_percent": 28.36, "max_gpu_percent": 100.0, "avg_memory_mb": 4634.01, "max_memory_mb": 4790.19},
])
workflow_metrics.to_csv(OUT / "workflow_gpu_metrics.csv", index=False)

# ---------------------------------------------------------------------------
# 11. Controlled CPU vs GPU comparison (Cells 72, 74)
# ---------------------------------------------------------------------------
cpu_gpu_comparison = pd.DataFrame([
    {"environment": "CPU - scikit-learn", "rows": 250000, "time_seconds": 22.568548},
    {"environment": "GPU - cuML", "rows": 250000, "time_seconds": 1.547914},
])
cpu_gpu_comparison.to_csv(OUT / "cpu_gpu_comparison.csv", index=False)

with open(OUT / "cpu_gpu_speedup.json", "w", encoding="utf-8") as f:
    json.dump({"speedup_x": 14.58, "cpu_seconds": 22.569, "gpu_seconds": 1.548, "rows": 250000}, f, indent=2)

# ---------------------------------------------------------------------------
# 12. Overall project summary
# ---------------------------------------------------------------------------
project_summary = {
    "project_name": "CyberShield AI",
    "dataset": "CIC-IDS2017 Network Intrusion Dataset (chethuhn/network-intrusion-dataset)",
    "loaded_rows": 1373802,
    "feature_count": 72,
    "best_model": "cuML Random Forest",
    "best_accuracy": 0.998046,
    "best_precision": 0.996577,
    "best_recall": 0.994511,
    "best_f1_score": 0.995543,
    "cpu_gpu_speedup": 14.58,
    "gpu_used": "NVIDIA Tesla T4",
    "author": "Yahya Ali Majrashi",
    "program": "Diploma in Data Science and AI, Tuwaiq Academy",
    "course": "Scalable Data Science",
}
with open(OUT / "project_summary.json", "w", encoding="utf-8") as f:
    json.dump(project_summary, f, indent=2)

print("All data files generated in:", OUT)
for p in sorted(OUT.iterdir()):
    if p.suffix in (".csv", ".json"):
        print(" -", p.name)
