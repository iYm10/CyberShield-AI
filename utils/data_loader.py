"""
Cached loaders for the pre-computed CyberShield AI result files.

Every value returned here was produced by the RAPIDS cuDF / cuML pipeline in
`CyberShield_AI.ipynb` and is copied verbatim into `data/generate_data.py`
(see that file's comments for the exact source cell). Loading from static
files keeps the dashboard instant and reproducible without requiring a GPU,
RAPIDS, or the 1.5M-row CIC-IDS2017 dataset at runtime.
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


@st.cache_data
def load_json(name: str) -> dict:
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_correlation_matrix() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "correlation_matrix.csv", index_col=0)
    return df


def get_project_summary() -> dict:
    return load_json("project_summary.json")


def get_dataset_summary() -> dict:
    return load_json("dataset_summary.json")


def get_model_comparison() -> pd.DataFrame:
    return load_csv("model_comparison.csv")


def get_confusion_matrices() -> dict:
    return load_json("confusion_matrices.json")


def get_workflow_metrics() -> pd.DataFrame:
    return load_csv("workflow_gpu_metrics.csv")


def get_cpu_gpu_comparison() -> pd.DataFrame:
    return load_csv("cpu_gpu_comparison.csv")


def get_cpu_gpu_speedup() -> dict:
    return load_json("cpu_gpu_speedup.json")


def get_feature_correlations() -> pd.DataFrame:
    return load_csv("feature_correlations.csv")


def get_engineered_feature_comparison() -> pd.DataFrame:
    return load_csv("engineered_feature_comparison.csv")


def get_label_distribution() -> pd.DataFrame:
    return load_csv("label_distribution.csv")


def get_binary_distribution() -> pd.DataFrame:
    return load_csv("binary_distribution.csv")


def get_source_files() -> pd.DataFrame:
    return load_csv("source_files.csv")
