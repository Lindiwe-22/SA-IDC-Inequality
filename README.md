# Who Really Gets the Money?
### A Public Interest Analysis of South African Development Finance

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

> *South Africa has one of the highest unemployment rates in the world. Nearly 1 in 3 working-age
> South Africans is officially unemployed — by the expanded measure, closer to 1 in 2. Among youth
> aged 15–24, it exceeds 60%. Into this crisis, the government deploys billions of rands through
> development finance institutions with a constitutional mandate to create jobs and transform the
> economy. This project asks a simple question: **is the money working, and is it reaching the
> people who need it most?***

---

## 📋 Project Overview

This project is a **two-layer data science investigation** of South African Development Finance
Institution (DFI) funding:

| Layer | Audience | File |
|-------|----------|------|
| 📓 Analytical notebook | Data scientists, policy analysts, finance professionals | `analysis.ipynb` |
| 🌐 Public Streamlit app | Journalists, civic advocates, general public | `app.py` + `pages/` |

The analysis covers **R69.5 billion** of public development finance across two institutions:
the **Industrial Development Corporation (IDC)** and the **National Empowerment Fund (NEF)**.

---

## 🔍 The Six Key Findings

### 1. Geographic Concentration is Real and Measurable
Gauteng and KwaZulu-Natal received **55.9% of NEF disbursements** and **65.6% of all deals** —
from just 2 of 9 provinces. The provincial disbursement Gini coefficient is **0.469**,
indicating moderate-to-high geographic concentration. The Northern Cape received 17.8% of
money through just 14 deals, almost entirely driven by two high-value, low-job-creation recipients.

### 2. Deal Size Inequality Mirrors Income Inequality
The NEF deal-size Lorenz curve reveals a **Gini of 0.56** — approaching South Africa's own
income inequality levels. The bottom 12% of deals (under R1m) share just **0.7% of funding**.
The top 0.5% of deals (over R50m) absorb **17% of all money**.

### 3. The Biggest Recipients Are Not the Best Job Creators — By a Factor of 5,366×
**Zero overlap** exists between the top-10 disbursement recipients and the top-10 job creators.
Khatu Industrial received R534M and created 26 jobs (**R20.5M per job**).
Umnotho Maize received R9M and created 2,352 jobs (**R3,827 per job**).
Both received public NEF money. The 5,366× gap is not a statistical outlier — it is a policy pattern.

### 4. R65.9B Deployed With Zero Job Accountability Metrics
The IDC — deploying **18.3× more capital** than the NEF — publishes no cost-per-job data,
no provincial breakdown, and no sector attribution for 56.5% of its investment.
The NEF tracks every job and every province. The absence of IDC job data is a
**policy choice, not a technical limitation**.

### 5. Mining Dominates IDC Sector Funding
Among named sectors, mining and metals account for **56.5% of attributed IDC investment** —
R16.2 billion. New Industries (biotech, solar, AI) received just **1.3%** — R371 million.
South Africa's economy was built on mining. The IDC, by this measure, is reinforcing
that structure rather than transforming it.

### 6. Multiple Data Quality Gaps Limit Full Accountability
- FY2023-24 is **absent** from the IDC dataset
- **56.5%** of IDC investment has no sector attribution
- NEF grants + loans sum to **R114.5M more** than total disbursed (likely uncommitted facilities)
- **Duplicate company entries** appear in the NEF top-10 job creators list (KPML Group, Bibi Cash & Carry)

---

## 📊 Data Sources

| Source | Institution | Description |
|--------|-------------|-------------|
| IDC Funding Dashboard | Industrial Development Corporation | 852 deals, R65.9B, FY2017–2025 |
| Parliamentary Question PQ705 | National Empowerment Fund via dtic.gov.za | 392 companies, R3.6B, all 9 provinces |
| QLFS Q3 2025 | Stats SA | Official unemployment statistics |

> **Note:** Both DFI datasets are structured from public-facing dashboard exports.
> Raw company-level transaction data is not publicly available for the IDC.
> The NEF data originates from a parliamentary question (PQ705, Mr RWC Chance, DA),
> answered via dtic.gov.za.

---

## 🗂️ Repository Structure
```
sa-idc-inequality/
│
├── app.py                          # Streamlit landing page
├── analysis.ipynb                  # Inequality analysis notebook (professional audience)
├── requirements.txt
├── README.md
│
├── notebooks/
│   ├── ml_predictor.ipynb          # Job Creation ROI Predictor — ML training notebook
│   └── anomaly_detection.ipynb     # NEF Anomaly Detection — Isolation Forest notebook
│
├── pages/
│   ├── 1_Crisis_Context.py         # Unemployment benchmarks + DFI mandate
│   ├── 2_Geographic_Inequality.py  # Provincial money vs jobs + cost per job
│   ├── 3_Deal_Size_Inequality.py   # Lorenz curve + bracket divergence + grants
│   ├── 4_Job_Efficiency.py         # Top-10 disbursed vs top-10 job creators
│   ├── 5_Sector_Concentration.py   # IDC sectors + fiscal trend + accountability gap
│   ├── 6_Job_ROI_Predictor.py      # ML-powered cost-per-job predictor
│   └── 7_Anomaly_Detection.py      # Isolation Forest anomaly flagging
│
└── data/
    ├── IDC_Funded_Businesses.csv
    └── NEF_Funded_Businesses.csv
```


---

## 🚀 Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-org/sa-dfi-inequality.git
cd sa-dfi-inequality

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py

# 4. Or open the notebook
jupyter notebook analysis.ipynb
```

---
## 🧪 Analytical Notebooks

### `analysis.ipynb` — Funding Concentration & Inequality Analysis
Linear narrative with headings per analytical lens, for data science and policy professionals.

| Section | What it covers |
|---------|---------------|
| Setup | Libraries, colour palette, matplotlib dark theme |
| Data Loading | IDC and NEF DataFrames reconstructed from dashboard exports |
| Lens 1 | Unemployment crisis as the moral benchmark |
| Lens 2 | Geographic concentration — Gini, provincial divergence, cost-per-job |
| Lens 3 | Deal size inequality — Lorenz curve, grants vs loans discrepancy |
| Lens 4 | Job creation efficiency — scatter, top-10 comparison, the 5,366× gap |
| Lens 5 | IDC sector concentration — sector breakdown, fiscal year trend |
| Lens 6 | Cross-dataset synthesis — IDC vs NEF comparison, discrepancy register |
| Conclusions | 6 numbered findings handed off to `app.py` |

### `notebooks/ml_predictor.ipynb` — Job Creation ROI Predictor
Three ML models trained to predict cost-per-job from deal characteristics.

| Section | What it covers |
|---------|---------------|
| Data Construction | 17 real anchors + 375 aggregate-derived records |
| EDA | Distribution analysis, log-log relationships |
| Feature Engineering | log_disbursed, bracket_ord, has_grant, province dummies |
| Model Training | Linear Regression · Random Forest · XGBoost with 5-fold CV |
| Model Comparison | R², RMSE, predicted vs actual charts |
| Feature Importance | Deal size dominates at >85% — the policy implication |
| Conclusions | 5 findings including the Umnotho Maize outlier note |

### `notebooks/anomaly_detection.ipynb` — NEF Anomaly Detection
Isolation Forest flags statistical outliers — both red flags and positive outliers.

| Section | What it covers |
|---------|---------------|
| EDA | Disbursed vs jobs in raw and log-log space |
| Isolation Forest | Setup, contamination=10%, 200 estimators |
| Score Distribution | Anomaly score histogram with real company annotations |
| Anomaly Map | Scatter chart — disbursed vs jobs coloured by anomaly status |
| Named Outliers | Real companies flagged with full metrics |
| Province Analysis | Anomaly rate concentration by province |
| Sensitivity Analysis | Stability across contamination rates 5%–20% |
| Conclusions | 5 findings including CK Mafutha as most anomalous record |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pandas` | Data wrangling and analysis |
| `numpy` | Statistical calculations (Gini, Lorenz) |
| `matplotlib` | Notebook visualisations (dark theme) |
| `plotly` | Interactive Streamlit charts |
| `streamlit` | Public-facing web application |
| `scikit-learn` | Machine learning — Isolation Forest, Random Forest, Linear Regression |
| `xgboost` | Gradient boosting — XGBoost regressor |

---

## 🌐 Deployment

The app is deployed on **Streamlit Cloud**. To deploy your own instance:

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo and set **Main file** to `app.py`
5. Click **Deploy** — dependencies install automatically from `requirements.txt`

---

## 📁 Project Series

| # | Title | Notebook | Streamlit Page | Status |
|---|-------|----------|----------------|--------|
| 3 | Funding Concentration & Inequality Analysis | `analysis.ipynb` | Pages 1–5 | ✅ Live |
| 2 | Job Creation ROI Predictor | `notebooks/ml_predictor.ipynb` | Page 6 | ✅ Live |
| 5 | NEF Anomaly Detection | `notebooks/anomaly_detection.ipynb` | Page 7 | ✅ Live |
```

---
```
## ⚠️ Limitations & Caveats

- IDC data covers **named sectors only** — 56.5% of investment is unattributed
- NEF job figures are **self-reported** in a parliamentary response and have not been independently audited
- FY2023-24 IDC data is **absent** from the source — trend analysis skips this year
- Provincial unemployment rates are not included in this dataset — geographic efficiency analysis uses national averages
- The NEF dataset does not include time-series data — no year-on-year comparison is possible
```
---
```
## 🤝 Contributing & Feedback

This is an open civic data project. If you have access to more granular IDC or NEF data,
or can identify errors in the source parliamentary question, please open an issue or pull request.
```
---
```
## 🙏 Acknowledgements

The underlying dataset was compiled and made publicly available by
**[@AfikaSoyamba](https://x.com/AfikaSoyamba)** on X, who built a database of
1,248 South African businesses funded by the IDC and NEF — 856 from the IDC,
392 from the NEF — including every company name, amount, and province.
This analysis would not exist without that work. Thank you.
```
---
```
## 📜 License

MIT License — see `LICENSE` for details.
Data sourced from South African public records. Analysis and code © 2025 Lindiwe Songelwa.
```
```
*Part of a data science portfolio targeting the South African mining and finance sectors.*
*Built with Python · Streamlit · Plotly · Public data.*
```
