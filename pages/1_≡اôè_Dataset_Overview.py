import plotly.express as px
import streamlit as st

from utils.theme import apply_theme, render_sidebar, footer
from utils.data_loader import (
    get_dataset_summary,
    get_label_distribution,
    get_binary_distribution,
    get_source_files,
)

apply_theme("Dataset Overview", "📊")
render_sidebar()

summary = get_dataset_summary()

st.title("📊 Dataset Overview")
st.caption("CIC-IDS2017 Network Intrusion Dataset — `chethuhn/network-intrusion-dataset` on Kaggle")

# ---------------------------------------------------------------------------
# Summary metrics
# ---------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Source CSV Files", summary["source_files"])
c2.metric("Rows Loaded", f"{summary['rows_loaded']:,}")
c3.metric("Original Columns", summary["original_columns"])
c4.metric("Duplicates Removed", f"{summary['duplicates_removed']:,}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Final Rows (after cleaning)", f"{summary['final_rows']:,}")
c6.metric("Constant Features Removed", summary["constant_features_removed"])
c7.metric("Engineered Features Added", summary["engineered_features_added"])
c8.metric("Final Modeling Features", summary["final_feature_count"])

st.markdown("---")

# ---------------------------------------------------------------------------
# Source files
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Source Files")
    st.caption("Records were sampled from all 8 CIC-IDS2017 files (rather than a single file) to preserve traffic diversity across days and attack types.")
    source_df = get_source_files()
    fig = px.bar(
        source_df.sort_values("size_mb"),
        x="size_mb", y="file", orientation="h",
        labels={"size_mb": "File Size (MB)", "file": ""},
        color_discrete_sequence=["#00E5A0"],
    )
    fig.update_layout(
        template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        height=380, margin=dict(l=0, r=10, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Data Cleaning Pipeline")
    st.markdown(
        f"""
1. Remove exact duplicate rows → **{summary['duplicates_removed']:,}** removed
2. Create binary `is_attack` target from the original label
3. Drop identifier / leakage columns (IPs, flow ID, timestamp, source file)
4. Convert candidate features to numeric, coerce errors
5. Replace ±infinity with missing values
6. Median-impute remaining missing values
7. Remove empty & constant columns → **{summary['constant_features_removed']}** removed
8. Cast modeling features to `float32`
9. Preserve the **original class distribution in the test set**
        """
    )

st.markdown("---")

# ---------------------------------------------------------------------------
# Label distributions
# ---------------------------------------------------------------------------
st.subheader("Traffic Label Distribution")

tab1, tab2 = st.tabs(["Detailed Attack Types", "Binary: Benign vs Attack"])

with tab1:
    label_df = get_label_distribution().sort_values("count")
    fig = px.bar(
        label_df, x="count", y="label", orientation="h",
        labels={"count": "Number of Flows", "label": ""},
        color_discrete_sequence=["#00E5A0"],
    )
    fig.update_layout(
        template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        height=460, margin=dict(l=0, r=10, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "The dataset is highly imbalanced, with BENIGN traffic dominating the majority of "
        "flows. Among attacks, DoS Hulk, PortScan, and DDoS are the most common."
    )

with tab2:
    bin_df = get_binary_distribution()
    fc1, fc2 = st.columns([1, 1])
    with fc1:
        fig = px.pie(
            bin_df, names="traffic_class", values="count", hole=0.55,
            color="traffic_class",
            color_discrete_map={"Benign": "#00E5A0", "Attack": "#FF4B5C"},
        )
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            height=360, margin=dict(l=0, r=0, t=10, b=0), showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True)
    with fc2:
        st.metric("Benign Flows", f"{summary['benign_records']:,}")
        st.metric("Attack Flows", f"{summary['attack_records']:,}")
        st.metric("Attack Share", f"{summary['attack_share_percent']}%")
        st.info(
            "Class imbalance (~22% attack traffic) is an important consideration during "
            "model training — addressed later via training-set-only class balancing."
        )

st.markdown("---")

# ---------------------------------------------------------------------------
# Train/test split & balancing
# ---------------------------------------------------------------------------
st.subheader("Train / Test Split & Class Balancing")
st.markdown(
    """
The test set keeps the **natural class distribution** so evaluation reflects
real-world traffic. Balancing (max **3:1** Benign-to-Attack ratio) is applied
**only to the training set**.
"""
)

split_cols = st.columns(3)
split_cols[0].metric("Training Rows (before balancing)", f"{summary['training_rows_before_balancing']:,}")
split_cols[1].metric("Testing Rows", f"{summary['testing_rows']:,}")
split_cols[2].metric("Training Rows (after balancing)", f"{summary['training_rows_after_balancing']:,}")

before_after = px.bar(
    x=["Benign (before)", "Attack (before)", "Benign (after)", "Attack (after)"],
    y=[
        summary["training_benign_before_balancing"],
        summary["training_attack_before_balancing"],
        summary["training_benign_after_balancing"],
        summary["training_attack_after_balancing"],
    ],
    color=["Benign", "Attack", "Benign", "Attack"],
    color_discrete_map={"Benign": "#00E5A0", "Attack": "#FF4B5C"},
    labels={"x": "", "y": "Training Rows"},
)
before_after.update_layout(
    template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    height=380, margin=dict(l=0, r=10, t=10, b=0), showlegend=False,
)
st.plotly_chart(before_after, use_container_width=True)

footer()
