import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Geographic Inequality", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 2 of 7 &nbsp;·&nbsp; Geographic Inequality",
    "Where Does the<br>Money <em>Land?</em>",
    "Two provinces — Gauteng and KwaZulu-Natal — dominate NEF disbursements. "
    "The provincial Gini coefficient for development finance distribution is 0.469. "
    "This is not random. It is a measurable pattern with measurable consequences."
), unsafe_allow_html=True)

st.markdown(section_rule("Provincial concentration — NEF disbursements"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-3">
  <div class="stat-cell warn">
    <div class="stat-number amber">55.9%</div>
    <div class="stat-desc">Of NEF disbursements to Gauteng and KZN combined — 2 of 9 provinces.</div>
  </div>
  <div class="stat-cell warn">
    <div class="stat-number amber">65.6%</div>
    <div class="stat-desc">Of all NEF deals located in the same two provinces.</div>
  </div>
  <div class="stat-cell warn">
    <div class="stat-number amber">0.469</div>
    <div class="stat-desc">Provincial disbursement Gini coefficient. Moderate-to-high geographic concentration.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chart ──────────────────────────────────────────────────────────────────────
try:
    df = pd.read_csv("data/NEF_Funded_Businesses.csv")
    if "Province" in df.columns and "Amount" in df.columns:
        prov = df.groupby("Province")["Amount"].sum().reset_index()
        prov.columns = ["Province", "Total (R)"]
        prov = prov.sort_values("Total (R)", ascending=True)

        fig = px.bar(
            prov, x="Total (R)", y="Province", orientation="h",
            color_discrete_sequence=["#BA7517"],
        )
        fig.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=0, r=20, t=20, b=20),
            xaxis_title="Total disbursed (R)",
            yaxis_title="",
            showlegend=False,
            height=360,
        )
        fig.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.markdown(callout(
        "Chart renders from live data in the deployed app. "
        "Run locally with the data files present to see the visualisation.",
        "info"
    ), unsafe_allow_html=True)

st.markdown(section_rule("The Northern Cape anomaly"), unsafe_allow_html=True)

st.markdown(callout(
    "The Northern Cape received <strong>17.8% of money</strong> through just 14 deals — "
    "an outsized share driven almost entirely by two high-value, low-job-creation recipients. "
    "This is not development finance reaching those who need it most. "
    "It is concentration at the top of the deal-size distribution."
), unsafe_allow_html=True)

st.markdown(section_rule("Cost per job by province"), unsafe_allow_html=True)

st.markdown("""
<p>
The provincial breakdown reveals not just where money goes — but what it buys when it gets there.
Provinces receiving large disbursements do not consistently produce proportionally more jobs.
The cost-per-job metric is the correct accountability measure, and it varies significantly across provinces.
</p>
""", unsafe_allow_html=True)

try:
    if "Jobs" in df.columns and "Province" in df.columns and "Amount" in df.columns:
        cpj = df.groupby("Province").agg({"Amount": "sum", "Jobs": "sum"}).reset_index()
        cpj["Cost per Job (R)"] = (cpj["Amount"] / cpj["Jobs"]).round(0)
        cpj = cpj[cpj["Jobs"] > 0].sort_values("Cost per Job (R)", ascending=True)

        fig2 = px.bar(
            cpj, x="Cost per Job (R)", y="Province", orientation="h",
            color_discrete_sequence=["#0F6E56"],
        )
        fig2.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=0, r=20, t=20, b=20),
            xaxis_title="Cost per job (R)",
            yaxis_title="",
            showlegend=False,
            height=360,
        )
        fig2.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig2.update_yaxes(showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)
except Exception:
    pass

st.markdown(data_note(
    "Source: NEF Parliamentary Question PQ705 via dtic.gov.za · Dataset compiled by @AfikaSoyamba · "
    "Provincial unemployment rates not included in source data — analysis uses national averages."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
