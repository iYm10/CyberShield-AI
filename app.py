"""
CyberShield AI — Streamlit Dashboard
=====================================
Main entry point / Overview page.

Run locally:
    streamlit run app.py

This dashboard presents the results of `CyberShield_AI.ipynb`: a
GPU-accelerated (RAPIDS cuDF + cuML) network-intrusion-detection pipeline
trained on the CIC-IDS2017 dataset. All figures shown throughout the app are
taken directly from the notebook's executed output (see `data/generate_data.py`
for the exact source cell of every number).
"""

import streamlit as st

from utils.theme import apply_theme, render_sidebar, footer
from utils.data_loader import get_project_summary, get_dataset_summary

apply_theme("Overview", "🛡️")
render_sidebar()

summary = get_project_summary()
dataset = get_dataset_summary()

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="cs-hero">
        <div class="cs-badge">GPU-Accelerated</div>
        <div class="cs-badge">RAPIDS cuDF + cuML</div>
        <div class="cs-badge">CIC-IDS2017</div>
        <div class="cs-badge">Binary Intrusion Detection</div>
        <h1 style="margin-top:14px; margin-bottom:6px;">🛡️ CyberShield AI</h1>
        <h4 style="font-weight:400; opacity:0.85; margin-top:0;">
            GPU-Accelerated Network Intrusion Detection using RAPIDS
        </h4>
        <p class="cs-muted" style="max-width:800px;">
            CyberShield AI classifies network traffic flows as <b>Benign</b> or
            <b>Attack</b> using GPU-accelerated machine learning. The project processes
            1.5 million CIC-IDS2017 network flow records end-to-end — data loading,
            cleaning, feature engineering, exploratory analysis, model training, and
            GPU performance benchmarking — using NVIDIA RAPIDS cuDF and cuML.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Key results at a glance
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Best Model", "cuML Random Forest")
c2.metric("Accuracy", f"{summary['best_accuracy']*100:.2f}%")
c3.metric("F1-Score", f"{summary['best_f1_score']*100:.2f}%")
c4.metric("GPU Speedup", f"{summary['cpu_gpu_speedup']:.2f}×")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Network Flows Processed", f"{dataset['rows_loaded']:,}")
c6.metric("Final Modeling Rows", f"{dataset['final_rows']:,}")
c7.metric("Model Features", dataset["final_feature_count"])
c8.metric("Attack Share", f"{dataset['attack_share_percent']}%")

st.markdown("")

# ---------------------------------------------------------------------------
# Objective
# ---------------------------------------------------------------------------
left, right = st.columns([3, 2])

with left:
    st.markdown('<div class="cs-card">', unsafe_allow_html=True)
    st.markdown('<div class="cs-section-title">Project Objective</div>', unsafe_allow_html=True)
    st.markdown(
        """
The main goal of CyberShield AI is to classify network traffic into **Benign**
or **Attack** while evaluating both **predictive performance** and **GPU
computational efficiency**.

**Research question:** Can GPU-accelerated machine learning detect malicious
network flows accurately and efficiently on a dataset containing more than one
million records?

**Practical value** — the system can support security teams by:
- Identifying suspicious network flows in near real time
- Prioritizing high-risk traffic for manual investigation
- Reducing analyst workload on large-scale traffic logs
- Demonstrating the value of GPU acceleration for cybersecurity analytics at scale
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="cs-card">', unsafe_allow_html=True)
    st.markdown('<div class="cs-section-title">Technology Stack</div>', unsafe_allow_html=True)
    st.markdown(
        """
- **Python**
- **NVIDIA RAPIDS** — cuDF, cuML, CuPy
- **scikit-learn** (metrics + CPU baseline)
- **Pandas / NumPy / Matplotlib**
- **KaggleHub** (dataset retrieval)
- **NVIDIA GPU / CUDA** (Tesla T4)
- **Streamlit** (this dashboard)
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------
st.markdown('<div class="cs-card">', unsafe_allow_html=True)
st.markdown('<div class="cs-section-title">End-to-End Workflow</div>', unsafe_allow_html=True)

workflow_graph = """
digraph {
    rankdir=LR;
    bgcolor="transparent";
    node [shape=box, style="rounded,filled", fillcolor="#121B2E", fontcolor="#E6EEFA", color="#00E5A0", fontname="Helvetica", margin="0.18,0.12"];
    edge [color="#3A4A6B", fontcolor="#9BB0CE", fontname="Helvetica"];

    A [label="Dataset\\nAcquisition"];
    B [label="GPU Data\\nLoading (cuDF)"];
    C [label="Data\\nCleaning"];
    D [label="Feature\\nEngineering"];
    E [label="Exploratory\\nData Analysis"];
    F [label="Train / Test\\nSplit"];
    G [label="Class\\nBalancing"];
    H [label="Feature\\nScaling"];
    I [label="GPU Model\\nTraining (cuML)"];
    J [label="Model\\nEvaluation"];
    K [label="GPU Performance\\nAnalysis"];
    L [label="CPU vs GPU\\nComparison"];

    A -> B -> C -> D -> E -> F -> G -> H -> I -> J -> K -> L;
}
"""
st.graphviz_chart(workflow_graph, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Navigation hint
# ---------------------------------------------------------------------------
st.markdown('<div class="cs-card">', unsafe_allow_html=True)
st.markdown('<div class="cs-section-title">Explore the Dashboard</div>', unsafe_allow_html=True)
nc1, nc2, nc3, nc4, nc5 = st.columns(5)
nc1.markdown("**📊 Dataset Overview**\n\nSource files, cleaning, class balance")
nc2.markdown("**🔍 Exploratory Analysis**\n\nCorrelations & engineered features")
nc3.markdown("**🤖 Model Performance**\n\nAccuracy, precision, recall, F1, confusion matrices")
nc4.markdown("**⚡ GPU vs CPU**\n\nTraining time, GPU utilization, 14.58× speedup")
nc5.markdown("**🧪 Live Detection Demo**\n\nInteractively classify a sample network flow")
st.caption("Use the sidebar to navigate between pages.")
st.markdown("</div>", unsafe_allow_html=True)

footer()
