# -*- coding: utf-8 -*-
"""
Static content for the CyberShield AI website.

Every number below is copied verbatim from CyberShield_AI.ipynb /
CyberShield_AI_Report.pdf / README.md in this repository -- nothing here is
invented. See the notebook for full methodology, plots, and discussion.
"""

HERO_STATS = [
    {"value": "99.80%", "label": "Best Model Accuracy"},
    {"value": "99.55%", "label": "Best Model F1-Score"},
    {"value": "14.58×", "label": "GPU vs CPU Speedup"},
    {"value": "1.5M", "label": "Network Flows Analyzed"},
]

DATASET_STATS = [
    {"value": "8", "label": "Source CSV Files (CIC-IDS2017)"},
    {"value": "1,500,000", "label": "Rows Loaded"},
    {"value": "80", "label": "Original Columns"},
    {"value": "126,198", "label": "Duplicate Rows Removed"},
    {"value": "1,373,802", "label": "Final Rows After Cleaning"},
    {"value": "72", "label": "Final Modeling Features"},
    {"value": "1,072,232", "label": "Benign Flows"},
    {"value": "301,570", "label": "Attack Flows"},
    {"value": "21.95%", "label": "Attack Share"},
]

MODEL_RESULTS = [
    {
        "model": "cuML Random Forest",
        "accuracy": 99.80,
        "precision": 99.66,
        "recall": 99.45,
        "f1": 99.55,
        "train_time": 18.286,
        "inference_time": 0.312,
        "best": True,
    },
    {
        "model": "cuML Logistic Regression",
        "accuracy": 94.69,
        "precision": 87.05,
        "recall": 89.05,
        "f1": 88.04,
        "train_time": 2.693,
        "inference_time": 0.064,
        "best": False,
    },
    {
        "model": "cuML Linear SVC",
        "accuracy": 94.03,
        "precision": 86.09,
        "recall": 86.80,
        "f1": 86.45,
        "train_time": 0.226,
        "inference_time": 0.027,
        "best": False,
    },
]

CONFUSION_MATRIX_RF = {
    "tn": 214253,
    "fp": 206,
    "fn": 331,
    "tp": 59971,
}

WORKFLOW_METRICS = [
    {"op": "Data Loading (cuDF)", "time": 2.99, "avg_gpu": 21.00, "max_gpu": 48.0},
    {"op": "Data Cleaning (cuDF)", "time": 3.53, "avg_gpu": 30.88, "max_gpu": 55.0},
    {"op": "Feature Scaling (cuML)", "time": 2.30, "avg_gpu": 28.36, "max_gpu": 100.0},
]

CPU_GPU_COMPARISON = {
    "rows": 250000,
    "cpu_seconds": 22.569,
    "gpu_seconds": 1.548,
    "speedup": 14.58,
}

TOP_CORRELATIONS = [
    ("bwd_packet_length_std", 0.577),
    ("bwd_packet_length_mean", 0.563),
    ("avg_bwd_segment_size", 0.563),
    ("bwd_packet_length_max", 0.562),
    ("packet_length_std", 0.534),
    ("max_packet_length", 0.514),
    ("packet_length_variance", 0.503),
    ("avg_bytes_per_packet", 0.501),
]

ENGINEERED_FEATURES = [
    {
        "name": "avg_bytes_per_packet",
        "formula": "(total_length_of_fwd_packets + total_length_of_bwd_packets) / (total_fwd_packets + total_backward_packets)",
        "insight": "Clear separation between classes: Benign flows median ≈ 70 bytes/packet vs. Attack flows median ≈ 798 bytes/packet.",
        "useful": True,
    },
    {
        "name": "fwd_bwd_packet_ratio",
        "formula": "total_fwd_packets / total_backward_packets",
        "insight": "Median ≈ 1.0 for both Benign and Attack traffic — the EDA found this feature was not discriminative.",
        "useful": False,
    },
]

EDA_CHARTS_TRAFFIC = [
    {
        "file": "benign_vs_attack.png",
        "title": "Benign vs. Attack Distribution",
        "caption": "1,072,232 benign flows vs. 301,570 attack flows — an attack share of 21.95%, showing clear class imbalance.",
    },
    {
        "file": "top_traffic_labels_clean.png",
        "title": "Top Network Traffic Labels",
        "caption": "BENIGN dominates the dataset; among attacks, DoS Hulk, PortScan, and DDoS are the most common traffic types.",
    },
    {
        "file": "records_per_source_file.png",
        "title": "Records per CIC-IDS2017 Source File",
        "caption": "Flows are distributed across all 8 CIC-IDS2017 capture files (~145K–195K rows each), improving traffic diversity.",
    },
]

EDA_CHARTS_CORRELATION = [
    {
        "file": "top_correlated_features.png",
        "title": "Top Features Correlated with Attack Traffic",
        "caption": "Packet-size and backward-traffic features show the strongest correlation with the attack label (up to 0.58).",
    },
    {
        "file": "correlation_heatmap.png",
        "title": "Correlation Heatmap (Top 8 Features)",
        "caption": "The strongest predictors are highly correlated with each other, indicating they capture overlapping packet-size information.",
    },
    {
        "file": "engineered_features_by_class.png",
        "title": "Engineered Features by Traffic Class",
        "caption": "avg_bytes_per_packet clearly separates Benign vs. Attack traffic; fwd_bwd_packet_ratio does not.",
    },
]

# Used individually (not looped) inside the Models and GPU Performance panels.
CHART_MODEL_PERFORMANCE = {
    "file": "model_performance_comparison.png",
    "title": "Model Performance Comparison",
    "caption": "cuML Random Forest outperforms Logistic Regression and Linear SVC on every metric.",
}
CHART_TRAIN_INFERENCE_TIME = {
    "file": "train_inference_time.png",
    "title": "GPU Training & Inference Time",
    "caption": "Linear SVC trains fastest (0.23s); Random Forest takes longer (18.3s) but delivers the best accuracy.",
}
CHART_GPU_UTILIZATION = {
    "file": "gpu_utilization.png",
    "title": "Maximum GPU Utilization",
    "caption": "Random Forest drives GPU utilization to 100% during training — the most GPU-intensive stage of the workflow.",
}
CHART_GPU_MEMORY = {
    "file": "gpu_memory_usage.png",
    "title": "Maximum GPU Memory Usage",
    "caption": "All three models use roughly ~5GB of GPU memory, slightly higher during training than inference.",
}

TECH_STACK = [
    "Python", "NVIDIA RAPIDS", "cuDF", "cuML", "CuPy", "Pandas", "NumPy",
    "scikit-learn", "Matplotlib", "KaggleHub", "NVIDIA GPU / CUDA",
    "Flask", "Gunicorn", "Render",
]

AUTHOR = {
    "name": "Yahya Ali Majrashi",
    "program": "Diploma in Data Science and AI — Tuwaiq Academy",
    "course": "Scalable Data Science",
    "dataset_ref": "Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). "
                   "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.",
}

REPO_URL = "https://github.com/iYm10/CyberShield-AI"
NOTEBOOK_URL = f"{REPO_URL}/blob/main/CyberShield_AI.ipynb"
REPORT_URL = f"{REPO_URL}/blob/main/CyberShield_AI_Report.pdf"

LIMITATIONS = [
    "CIC-IDS2017 was generated in a controlled network environment; real production traffic may behave differently.",
    "The system performs binary classification only and does not identify individual attack families.",
    "CyberShield AI is an academic machine learning prototype, not a production cybersecurity platform.",
]
