# CyberShield AI — Streamlit Dashboard

An interactive, multi-page Streamlit dashboard built on top of the results in
`CyberShield_AI.ipynb`. Every chart and number in the **Dataset Overview**,
**Exploratory Analysis**, **Model Performance**, and **GPU vs CPU** pages is
taken directly from the notebook's executed output — see
`data/generate_data.py` for the exact source cell of every figure. The
**Live Detection Demo** page is a clearly-labeled, CPU-only educational
reproduction (see that page for why).

## 1. Files added by this dashboard

```text
app.py                        # Entry point — run this with `streamlit run`
pages/
├── 1_📊_Dataset_Overview.py
├── 2_🔍_Exploratory_Analysis.py
├── 3_🤖_Model_Performance.py
├── 4_⚡_GPU_vs_CPU.py
├── 5_🧪_Live_Detection_Demo.py
└── 6_ℹ️_About.py
data/
├── generate_data.py           # Rebuilds every CSV/JSON below from notebook results
├── *.csv / *.json             # Pre-computed results (no GPU/dataset needed at runtime)
utils/
├── theme.py                   # Shared dark cybersecurity styling
├── data_loader.py             # Cached loaders for the data/ files
└── demo_model.py              # Synthetic, correlation-calibrated demo classifier
.streamlit/config.toml         # Dashboard theme
requirements.txt
.gitignore
STREAMLIT_APP.md               # This file
```

Copy all of the above into the root of the `CyberShield-AI` repository,
alongside the existing `CyberShield_AI.ipynb`, `CyberShield_AI_Report.pdf`,
and `README.md`.

## 2. Run it locally

```bash
git clone https://github.com/iYm10/CyberShield-AI.git
cd CyberShield-AI

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. No GPU, RAPIDS, or Kaggle
credentials are required — the reporting pages read the pre-computed
`data/*.csv` / `data/*.json` files, and the demo page trains a small
scikit-learn model on synthetic data in a few seconds.

## 3. Push to GitHub

From inside your local `CyberShield-AI` clone, after copying in the files above:

```bash
git add app.py pages/ data/ utils/ .streamlit/ requirements.txt .gitignore STREAMLIT_APP.md
git commit -m "Add interactive Streamlit dashboard for CyberShield AI results"
git push origin main
```

## 4. Deploy for free — Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app** → select the `iYm10/CyberShield-AI` repository and the `main` branch.
3. Set **Main file path** to `app.py`.
4. Click **Deploy**. The build installs `requirements.txt` automatically and the dashboard goes live at a public `*.streamlit.app` URL.
5. (Optional) Add that URL to your GitHub repo's **About** section and to `README.md` so visitors can try it without installing anything.

## 5. Suggested README badge

Add this near the top of `README.md` once deployed:

```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
```

## 6. Regenerating the data files

If you re-run the notebook and get new numbers, update the constants in
`data/generate_data.py` (every value is annotated with its source cell) and
re-run:

```bash
python data/generate_data.py
```

This rewrites the CSV/JSON files consumed by the dashboard — no other code changes needed.
