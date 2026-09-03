"""
Lightweight, self-contained demo classifier for the "Live Detection Demo" page.

WHY A SYNTHETIC MODEL?
-----------------------
The notebook's real models (cuML Random Forest / Logistic Regression / Linear
SVC) were trained on the GPU with RAPIDS cuML against the full 1,373,802-row
CIC-IDS2017 dataset. That dataset is not shipped in the repository (see
README — it is fetched at run time via `kagglehub`), and RAPIDS/cuML require
an NVIDIA GPU that a typical Streamlit deployment (e.g. Streamlit Community
Cloud) does not provide.

So this module builds a small, honest, CPU-only stand-in: it generates a
synthetic dataset whose feature correlations and class balance are
statistically calibrated to match the *actual* correlation matrix and class
ratio discovered during the notebook's EDA (see `data/correlation_matrix.csv`
and `data/dataset_summary.json`, both copied verbatim from the executed
notebook), then trains a small scikit-learn RandomForestClassifier on it.

The result lets a visitor interact with a real, trained classifier that
mirrors the *shape* of the original data — but it is clearly labelled in the
UI as a simplified educational reproduction, not the benchmarked GPU model.
For the authoritative, GPU-measured results, see the Model Performance page.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# The 8 real features most correlated with `is_attack` in the notebook's EDA
# (Cell 36 / 40), in the same order as data/correlation_matrix.csv.
FEATURES = [
    "bwd_packet_length_std",
    "bwd_packet_length_mean",
    "avg_bwd_segment_size",
    "bwd_packet_length_max",
    "packet_length_std",
    "max_packet_length",
    "packet_length_variance",
    "avg_bytes_per_packet",
]

FEATURE_LABELS = {
    "bwd_packet_length_std": "Backward Packet Length — Std Dev (bytes)",
    "bwd_packet_length_mean": "Backward Packet Length — Mean (bytes)",
    "avg_bwd_segment_size": "Avg Backward Segment Size (bytes)",
    "bwd_packet_length_max": "Backward Packet Length — Max (bytes)",
    "packet_length_std": "Packet Length — Std Dev (bytes)",
    "max_packet_length": "Max Packet Length (bytes)",
    "packet_length_variance": "Packet Length Variance (bytes²)",
    "avg_bytes_per_packet": "Avg Bytes per Packet (engineered feature)",
}

# Illustrative log-scale center/spread per feature (order of magnitude only —
# see module docstring). These are not per-flow ground truth values.
_LOGNORMAL_PARAMS = {
    "bwd_packet_length_std": (np.log(80), 0.70),
    "bwd_packet_length_mean": (np.log(120), 0.70),
    "avg_bwd_segment_size": (np.log(120), 0.70),
    "bwd_packet_length_max": (np.log(300), 0.65),
    "packet_length_std": (np.log(90), 0.70),
    "max_packet_length": (np.log(350), 0.60),
    "packet_length_variance": (np.log(8000), 1.10),
    "avg_bytes_per_packet": (np.log(150), 0.95),
}

ATTACK_SHARE = 0.2195  # exact attack share measured in the notebook (21.95%)
RANDOM_STATE = 42


def _load_correlation_matrix() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "correlation_matrix.csv", index_col=0)


def _nearest_psd(matrix: np.ndarray) -> np.ndarray:
    """Clip tiny negative eigenvalues so the empirical matrix is usable as a
    covariance matrix for sampling (numerical safety net only)."""
    eigvals, eigvecs = np.linalg.eigh(matrix)
    eigvals_clipped = np.clip(eigvals, 1e-6, None)
    return (eigvecs * eigvals_clipped) @ eigvecs.T


@st.cache_resource(show_spinner=False)
def build_demo_assets(n_samples: int = 24000, seed: int = RANDOM_STATE):
    """
    Generates the calibrated synthetic dataset, trains the demo RandomForest,
    and returns everything the Live Demo page needs. Cached for the life of
    the app process, so this only runs once.
    """
    corr_df = _load_correlation_matrix()
    ordered_cols = FEATURES + ["is_attack"]
    corr = corr_df.loc[ordered_cols, ordered_cols].to_numpy()
    corr = _nearest_psd(corr)

    rng = np.random.default_rng(seed)
    z = rng.multivariate_normal(mean=np.zeros(len(ordered_cols)), cov=corr, size=n_samples)

    z_features = z[:, :-1]
    z_latent = z[:, -1]

    # Threshold the latent attack factor so the synthetic attack share
    # matches the real measured share (21.95%).
    threshold = np.quantile(z_latent, 1 - ATTACK_SHARE)
    is_attack = (z_latent >= threshold).astype(int)

    data = {}
    for i, feature in enumerate(FEATURES):
        mu, sigma = _LOGNORMAL_PARAMS[feature]
        data[feature] = np.exp(mu + sigma * z_features[:, i])

    X = pd.DataFrame(data)
    y = pd.Series(is_attack, name="is_attack")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        max_features="sqrt",
        class_weight="balanced",
        random_state=seed,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    demo_accuracy = float(accuracy_score(y_test, preds))
    demo_f1 = float(f1_score(y_test, preds))

    importances = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)

    sample_benign = X[y == 0].median().to_dict()
    sample_attack = X[y == 1].median().to_dict()

    return {
        "model": model,
        "feature_importances": importances,
        "demo_accuracy": demo_accuracy,
        "demo_f1": demo_f1,
        "sample_benign": sample_benign,
        "sample_attack": sample_attack,
        "feature_ranges": {f: (float(X[f].quantile(0.01)), float(X[f].quantile(0.99))) for f in FEATURES},
        "feature_medians": X.median().to_dict(),
    }


def predict_flow(model: RandomForestClassifier, feature_values: dict):
    row = pd.DataFrame([{f: feature_values[f] for f in FEATURES}])
    proba = model.predict_proba(row)[0]
    classes = list(model.classes_)
    attack_idx = classes.index(1)
    attack_probability = float(proba[attack_idx])
    label = "Attack" if attack_probability >= 0.5 else "Benign"
    return label, attack_probability
