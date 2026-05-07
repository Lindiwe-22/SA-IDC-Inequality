import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Anomaly Detection", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 7 of 7 &nbsp;·&nbsp; Anomaly Detection",
    "Which Deals Fall<br>Outside the <em>Pattern?</em>",
    "Isolation Forest was applied to the NEF dataset to surface statistical outliers — "
    "both red flags and positive outliers. The most anomalous record in the dataset is "
    "CK Mafutha. The most efficient is Umnotho Maize."
), unsafe_allow_html=True)

st.markdown(section_rule("Model configuration"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-3">
  <div class="stat-cell info">
    <div class="stat-number blue">10%</div>
    <div class="stat-desc">Contamination rate. Proportion of data flagged as anomalous.</div>
  </div>
  <div class="stat-cell info">
    <div class="stat-number blue">200</div>
    <div class="stat-desc">Estimators. Stable results across 5%–20% contamination sensitivity test.</div>
  </div>
  <div class="stat-cell info">
    <div class="stat-number blue">5–20%</div>
    <div class="stat-desc">Contamination range tested. Key anomalies remain stable across all thresholds.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(section_rule("Named outliers"), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>CK Mafutha</strong> is the most anomalous record in the dataset — "
    "an extreme outlier on both disbursement amount and cost-per-job. "
    "<strong>Umnotho Maize</strong> is the positive outlier: the most efficient deal in the dataset "
    "at R3,827 per job on R9M disbursed."
), unsafe_allow_html=True)

# ── Anomaly scatter ────────────────────────────────────────────────────────────
try:
    df = pd.read_csv("data/NEF_Funded_Businesses.csv")

    if all(c in df.columns for c in ["Company", "Amount", "Jobs"]):
        from sklearn.ensemble import IsolationForest
        import numpy as np

        features = df[["Amount", "Jobs"]].dropna()
        features_log = np.log1p(features)
        model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
        df_clean = df.loc[features.index].copy()
        df_clean["anomaly"] = model.fit_predict(features_log)
        df_clean["anomaly_label"] = df_clean["anomaly"].map({1: "Normal", -1: "Anomalous"})

        fig = px.scatter(
            df_clean[df_clean["Jobs"] > 0],
            x="Amount",
            y="Jobs",
            color="anomaly_label",
            hover_name="Company",
            color_discrete_map={"Normal": "#BA7517", "Anomalous": "#A32D2D"},
            log_x=True,
            log_y=True,
        )
        fig.update_traces(marker=dict(size=7, opacity=0.75))
        fig.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Amount disbursed (R, log scale)",
            yaxis_title="Jobs created (log scale)",
            legend_title="",
            legend=dict(orientation="h", y=-0.15),
            height=420,
        )
        fig.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        st.plotly_chart(fig, use_container_width=True)

except Exception:
    st.markdown(callout(
        "Anomaly scatter renders from live data in the deployed app. "
        "scikit-learn required.",
        "info"
    ), unsafe_allow_html=True)

st.markdown(section_rule("Province anomaly concentration"), unsafe_allow_html=True)

try:
    if "anomaly_label" in df_clean.columns and "Province" in df_clean.columns:
        prov_anom = df_clean.groupby("Province").apply(
            lambda x: (x["anomaly"] == -1).sum() / len(x) * 100
        ).reset_index()
        prov_anom.columns = ["Province", "Anomaly Rate (%)"]
        prov_anom = prov_anom.sort_values("Anomaly Rate (%)", ascending=True)

        fig3 = px.bar(
            prov_anom, x="Anomaly Rate (%)", y="Province", orientation="h",
            color_discrete_sequence=["#A32D2D"],
        )
        fig3.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=0, r=20, t=20, b=20),
            xaxis_title="Anomaly rate (%)",
            yaxis_title="",
            showlegend=False,
            height=320,
        )
        fig3.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig3.update_yaxes(showgrid=False)
        st.plotly_chart(fig3, use_container_width=True)
except Exception:
    pass

st.markdown(section_rule("What anomalies mean in this context"), unsafe_allow_html=True)

st.markdown("""
<p>
Anomaly detection does not prove wrongdoing. It surfaces deals that fall outside the statistical
pattern of the programme — either because they are extraordinarily inefficient or extraordinarily
effective. Both warrant scrutiny.
</p>
<p style="margin-top:14px;">
The stability of flagged records across contamination thresholds of 5% to 20% indicates these
are genuine structural outliers, not artefacts of model sensitivity.
</p>
""", unsafe_allow_html=True)

st.markdown(data_note(
    "Model: Isolation Forest · 200 estimators · contamination=0.10 · log-transformed features. "
    "Sensitivity tested at 5%, 10%, 15%, 20% contamination — key outliers stable across all thresholds. "
    "Source: NEF Parliamentary Question PQ705 via dtic.gov.za · Dataset compiled by @AfikaSoyamba."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
