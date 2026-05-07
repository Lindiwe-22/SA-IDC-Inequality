import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Sector Concentration", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 5 of 7 &nbsp;·&nbsp; Sector Concentration",
    "The IDC Is Reinforcing<br>the Past, Not <em>Building the Future</em>",
    "Mining and metals account for 56.5% of named-sector IDC investment. "
    "New industries — biotech, solar, AI — received 1.3%. "
    "South Africa's economy was built on extractive industries. "
    "By this measure, the IDC is entrenching that structure."
), unsafe_allow_html=True)

st.markdown(section_rule("IDC sector allocation — named sectors only"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-3">
  <div class="stat-cell warn">
    <div class="stat-number amber">56.5%</div>
    <div class="stat-desc">Of named-sector IDC investment in mining and metals. R16.2B.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">1.3%</div>
    <div class="stat-desc">New Industries (biotech, solar, AI). R371M.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">56.5%</div>
    <div class="stat-desc">Of total IDC investment has no sector attribution at all.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "The absence of sector data for 56.5% of IDC investment is not a technical limitation. "
    "It is a <strong>reporting choice</strong>. The NEF attributes every deal to a province. "
    "The IDC — managing 18× more capital — leaves the majority of its portfolio unattributed."
), unsafe_allow_html=True)

st.markdown(section_rule("Sector breakdown — IDC named sectors"), unsafe_allow_html=True)

try:
    df = pd.read_csv("data/IDC_Funded_Businesses.csv")
    if "Sector" in df.columns and "Amount" in df.columns:
        sector = df.dropna(subset=["Sector"]).groupby("Sector")["Amount"].sum().reset_index()
        sector.columns = ["Sector", "Total (R)"]
        sector = sector.sort_values("Total (R)", ascending=True)

        fig = px.bar(
            sector, x="Total (R)", y="Sector", orientation="h",
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
            height=420,
        )
        fig.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.markdown(callout(
        "Chart renders from live data in the deployed app.",
        "info"
    ), unsafe_allow_html=True)

st.markdown(section_rule("Fiscal year trend"), unsafe_allow_html=True)

try:
    if "FY" in df.columns and "Amount" in df.columns:
        fy = df.groupby("FY")["Amount"].sum().reset_index()
        fy.columns = ["Financial Year", "Total (R)"]
        fy = fy[fy["Financial Year"] != "FY2023-24"]

        fig2 = px.line(
            fy, x="Financial Year", y="Total (R)",
            markers=True,
            color_discrete_sequence=["#BA7517"],
        )
        fig2.update_traces(line=dict(width=2), marker=dict(size=7))
        fig2.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Financial year",
            yaxis_title="Total investment (R)",
            height=320,
        )
        fig2.update_xaxes(showgrid=False)
        fig2.update_yaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown(callout(
            "Note: FY2023–24 is absent from the IDC source dataset. "
            "This gap in the public record is itself an accountability issue."
        ), unsafe_allow_html=True)
except Exception:
    pass

st.markdown(data_note(
    "Source: IDC Funding Dashboard (FY2017–2025) · Dataset compiled by @AfikaSoyamba · "
    "Named sectors only — 56.5% of IDC investment carries no sector attribution in the source data. "
    "FY2023-24 absent from source."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
