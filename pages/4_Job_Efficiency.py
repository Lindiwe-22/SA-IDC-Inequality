import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Job Creation Efficiency", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 4 of 7 &nbsp;·&nbsp; Job Creation Efficiency",
    "Biggest Recipients Are<br>Not the Best <em>Job Creators</em>",
    "There is zero overlap between the top 10 recipients of NEF funding and the top 10 job creators. "
    "The efficiency gap between the most and least effective deals is 5,366×. "
    "This is the central finding of this analysis."
), unsafe_allow_html=True)

st.markdown(section_rule("The 5,366× gap"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-3">
  <div class="stat-cell alert">
    <div class="stat-number red">R20.5M</div>
    <div class="stat-desc">Cost per job — Khatu Industrial. Received R534M. Created 26 jobs.</div>
  </div>
  <div class="stat-cell ok">
    <div class="stat-number teal">R3,827</div>
    <div class="stat-desc">Cost per job — Umnotho Maize. Received R9M. Created 2,352 jobs.</div>
  </div>
  <div class="stat-cell warn">
    <div class="stat-number amber">5,366×</div>
    <div class="stat-desc">Efficiency gap between these two recipients — funded by the same programme.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "Both Khatu Industrial and Umnotho Maize received public NEF money. "
    "The 5,366× cost-per-job gap is not a statistical outlier — it is evidence of a "
    "<strong>systematic absence of job creation criteria</strong> in how funding decisions are made.",
    "critical"
), unsafe_allow_html=True)

st.markdown(section_rule("Top 10 disbursements vs top 10 job creators"), unsafe_allow_html=True)

try:
    df = pd.read_csv("data/NEF_Funded_Businesses.csv")
    if all(c in df.columns for c in ["Company", "Amount", "Jobs"]):
        top_disbursed = df.nlargest(10, "Amount")[["Company", "Amount", "Jobs"]].copy()
        top_disbursed["Cost per Job (R)"] = (top_disbursed["Amount"] / top_disbursed["Jobs"].replace(0, float("nan"))).round(0)
        top_disbursed.columns = ["Company", "Disbursed (R)", "Jobs Created", "Cost per Job (R)"]

        top_jobs = df[df["Jobs"] > 0].nlargest(10, "Jobs")[["Company", "Amount", "Jobs"]].copy()
        top_jobs["Cost per Job (R)"] = (top_jobs["Amount"] / top_jobs["Jobs"]).round(0)
        top_jobs.columns = ["Company", "Disbursed (R)", "Jobs Created", "Cost per Job (R)"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
<div class="page-section-label" style="margin-bottom:10px;">Top 10 by disbursement amount</div>
""", unsafe_allow_html=True)
            st.dataframe(
                top_disbursed.style.format({
                    "Disbursed (R)": "R{:,.0f}",
                    "Jobs Created": "{:,.0f}",
                    "Cost per Job (R)": "R{:,.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
        with col2:
            st.markdown("""
<div class="page-section-label" style="margin-bottom:10px;">Top 10 by jobs created</div>
""", unsafe_allow_html=True)
            st.dataframe(
                top_jobs.style.format({
                    "Disbursed (R)": "R{:,.0f}",
                    "Jobs Created": "{:,.0f}",
                    "Cost per Job (R)": "R{:,.0f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
except Exception:
    st.markdown(callout(
        "Tables render from live data in the deployed app.",
        "info"
    ), unsafe_allow_html=True)

st.markdown(section_rule("Disbursement vs jobs — scatter"), unsafe_allow_html=True)

try:
    if all(c in df.columns for c in ["Company", "Amount", "Jobs"]):
        scatter_df = df[df["Jobs"] > 0].copy()
        fig = px.scatter(
            scatter_df,
            x="Amount",
            y="Jobs",
            hover_name="Company",
            color_discrete_sequence=["#BA7517"],
            log_x=True,
            log_y=True,
        )
        fig.update_traces(marker=dict(size=7, opacity=0.7))
        fig.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Amount disbursed (R, log scale)",
            yaxis_title="Jobs created (log scale)",
            height=400,
        )
        fig.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        st.plotly_chart(fig, use_container_width=True)
except Exception:
    pass

st.markdown(data_note(
    "Source: NEF Parliamentary Question PQ705 via dtic.gov.za · Dataset compiled by @AfikaSoyamba · "
    "NEF job figures are self-reported in a parliamentary response and have not been independently audited. "
    "Duplicate company entries (KPML Group, Bibi Cash & Carry) noted in NEF top-10 job creators list."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
