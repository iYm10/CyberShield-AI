# 🛡️ CyberShield AI

### GPU-Accelerated Network Intrusion Detection Using RAPIDS

CyberShield AI is a GPU-accelerated machine learning project designed to detect malicious network traffic using the **CIC-IDS2017** dataset.

The project demonstrates an end-to-end scalable data science workflow using **RAPIDS cuDF** for large-scale data processing and **cuML** for GPU-accelerated machine learning.

The system processes **1.5 million network flow records**, performs data cleaning, feature engineering, exploratory data analysis, model training, and evaluation while also measuring GPU performance and comparing CPU and GPU execution.

---

## 🎯 Project Objective

The main goal of CyberShield AI is to classify network traffic into:

- **Benign**
- **Attack**

while evaluating both:

- Predictive performance
- GPU computational efficiency

The project investigates whether GPU-accelerated machine learning can provide accurate and efficient intrusion detection on large-scale network traffic data.

---

## 📊 Dataset

**Dataset:** CIC-IDS2017 Network Intrusion Dataset

The dataset contains normal network traffic and multiple types of malicious network activity.

### Dataset Summary

| Item | Value |
|---|---:|
| Source Files | 8 CSV files |
| Rows Loaded | 1,500,000 |
| Original Columns | 80 |
| Duplicates Removed | 126,198 |
| Final Rows | 1,373,802 |
| Modeling Features | 72 |
| Benign Records | 1,072,232 |
| Attack Records | 301,570 |
| Attack Share | 21.95% |

The original attack labels were converted into a binary target:

- `0` → Benign
- `1` → Attack

---

## ⚙️ Project Workflow

The project follows an end-to-end GPU-accelerated machine learning pipeline:

```text
Dataset Acquisition
        ↓
GPU Data Loading
        ↓
Data Cleaning
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Train/Test Split
        ↓
Class Balancing
        ↓
Feature Scaling
        ↓
GPU Model Training
        ↓
Model Evaluation
        ↓
GPU Performance Analysis
        ↓
CPU vs GPU Comparison
```

---

## 🧹 Data Preprocessing

The preprocessing pipeline includes:

- Removing exact duplicate records
- Creating the binary `is_attack` target
- Removing identifiers and potential leakage columns
- Converting candidate features to numeric values
- Replacing infinite values
- Handling missing values using median imputation
- Removing empty and constant features
- Converting modeling features to `float32`
- Preserving the original test distribution

Class balancing was applied **only to the training set**, with a maximum Benign-to-Attack ratio of approximately **3:1**.

---

## 🧠 Feature Engineering

Two additional network features were created:

### `avg_bytes_per_packet`

Represents the average number of transferred bytes per packet.

### `fwd_bwd_packet_ratio`

Represents the relationship between forward and backward packet counts.

EDA showed that `avg_bytes_per_packet` was more useful for distinguishing benign traffic from attack traffic.

---

## 🔍 Exploratory Data Analysis

EDA was used to investigate:

- Class distribution
- Engineered feature behavior
- Feature relationships with the attack target
- Correlation between network-flow features and malicious traffic

Packet-length-related features showed some of the strongest relationships with the attack target.

The strongest observed absolute correlation was approximately **0.58** for:

`bwd_packet_length_std`

---

## 🤖 Machine Learning Models

Three GPU-accelerated classifiers were implemented using **cuML**:

1. Logistic Regression
2. Random Forest
3. Linear SVC

### Random Forest Configuration

```python
RandomForestClassifier(
    n_estimators=200,
    max_depth=18,
    max_features="sqrt",
    n_bins=128,
    random_state=RANDOM_STATE
)
```

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| **cuML Random Forest** | **99.80%** | **99.66%** | **99.45%** | **99.55%** |
| cuML Logistic Regression | 94.69% | 87.05% | 89.05% | 88.04% |
| cuML Linear SVC | 94.03% | 86.09% | 86.80% | 86.45% |

### 🏆 Best Model

**cuML Random Forest** achieved the strongest overall predictive performance.

It achieved:

- **Accuracy:** 99.80%
- **Precision:** 99.66%
- **Attack Recall:** 99.45%
- **F1-Score:** 99.55%

For an intrusion-detection system, recall is particularly important because false negatives represent real attacks that were not detected.

---

## 🔎 Random Forest Error Analysis

The Random Forest confusion matrix produced:

| Actual / Predicted | Benign | Attack |
|---|---:|---:|
| **Benign** | 214,253 | 206 |
| **Attack** | 331 | 59,971 |

Only **331 attacks** were incorrectly classified as benign, which is consistent with the model's high **99.45% attack recall**.

---

## ⚡ GPU Performance

### Training & Inference Time

| Model | Training Time | Inference Time |
|---|---:|---:|
| Random Forest | 18.286 s | 0.312 s |
| Logistic Regression | 2.693 s | 0.064 s |
| **Linear SVC** | **0.226 s** | **0.027 s** |

Linear SVC was the fastest model, while Random Forest required more computation but achieved significantly better predictive performance.

---

## 🚀 CPU vs GPU Comparison

A controlled experiment was performed using the same **250,000 records** and Logistic Regression workflow.

| Environment | Rows | Time |
|---|---:|---:|
| CPU – scikit-learn | 250,000 | 22.569 s |
| **GPU – cuML** | 250,000 | **1.548 s** |

### Observed GPU Speedup

# **14.58×**

The GPU implementation reduced execution time from approximately **22.57 seconds to 1.55 seconds**.

---

## 💻 Technologies Used

- Python
- NVIDIA RAPIDS
- cuDF
- cuML
- CuPy
- Pandas
- NumPy
- scikit-learn
- Matplotlib
- KaggleHub
- NVIDIA GPU / CUDA

---

## 📁 Suggested Repository Structure

```text
CyberShield-AI/
│
├── CyberShield_AI.ipynb
├── README.md
│
├── report/
│   └── CyberShield_AI_Report.pdf
│
├── figures/
│   ├── class_distribution.png
│   ├── engineered_features.png
│   ├── correlation.png
│   ├── model_performance.png
│   ├── gpu_timing.png
│   ├── gpu_utilization.png
│   └── gpu_memory.png
│
└── requirements.txt
```

> The CIC-IDS2017 dataset is not stored directly in the repository. It can be accessed separately through the dataset source.

---

## 🔮 Future Work

Future improvements could include:

- Multiclass attack classification
- Real-time network traffic inference
- SHAP-based model explainability
- Classification threshold tuning
- Automated hyperparameter optimization
- Multi-GPU processing using Dask-cuDF
- Evaluation on newer intrusion-detection datasets
- Interactive cybersecurity monitoring dashboard

---

## ⚠️ Limitations

CIC-IDS2017 was generated in a controlled network environment, so real production traffic may behave differently.

The current system performs binary classification and does not identify individual attack families.

CyberShield AI is an academic machine learning prototype and is not intended to replace a complete production cybersecurity platform.

---

## 🎓 Academic Context

This project was developed as part of the:

**Diploma in Data Science and AI**  
**Tuwaiq Academy**

**Course:** Scalable Data Science

---

## 👤 Author

**Yahya Ali Majrashi**

Data Science & AI Diploma  
Tuwaiq Academy

---

## 📚 References

- Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization.*
- CIC-IDS2017 Network Intrusion Dataset
- NVIDIA RAPIDS Documentation
- KaggleHub Documentation
- Scikit-learn Documentation

---

## ⭐ Project Summary

**CyberShield AI** demonstrates how GPU-accelerated data science can be applied to large-scale cybersecurity analytics.

Using **1.5 million network flows**, RAPIDS cuDF and cuML enabled scalable preprocessing and machine learning, while **cuML Random Forest achieved a 99.55% F1-score** and the controlled CPU/GPU experiment demonstrated a **14.58× GPU speedup**.
