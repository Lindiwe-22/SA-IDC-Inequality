import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Deal Size Inequality", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 3 of 7 &nbsp;·&nbsp; Deal Size Inequality",
    "The Money Is Not<br><em>Evenly Spread</em>",
    "The NEF deal-size Lorenz curve reveals a Gini coefficient of 0.56 — approaching South Africa's "
    "own income inequality levels. A programme designed to correct inequality is itself unequal."
), unsafe_allow_html=True)

st.markdown(section_rule("Deal size distribution — NEF"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-3">
  <div class="stat-cell warn">
    <div class="stat-number amber">0.56</div>
    <div class="stat-desc">NEF deal-size Gini coefficient. Comparable to SA income inequality.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">0.7%</div>
    <div class="stat-desc">Share of total funding going to the bottom 12% of deals (under R1M).</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">17%</div>
    <div class="stat-desc">Share absorbed by the top 0.5% of deals (over R50M).</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Lorenz curve ───────────────────────────────────────────────────────────────
try:
    df = pd.read_csv("data/NEF_Funded_Businesses.csv")
    if "Amount" in df.columns:
        amounts = df["Amount"].dropna().sort_values().values
        lorenz_y = np.cumsum(amounts) / amounts.sum()
        lorenz_x = np.arange(1, len(amounts) + 1) / len(amounts)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0] + list(lorenz_x) + [1],
            y=[0] + list(lorenz_y) + [1],
            mode="lines",
            line=dict(color="#BA7517", width=2),
            name="Lorenz curve",
            fill="tozeroy",
            fillcolor="rgba(186,117,23,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode="lines",
            line=dict(color="#D3D1C7", width=1, dash="dot"),
            name="Perfect equality",
        ))
        fig.update_layout(
            paper_bgcolor="#FAFAF8",
            plot_bgcolor="#FAFAF8",
            font_family="Source Serif 4, Georgia, serif",
            font_color="#2C2C2A",
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="Cumulative share of deals",
            yaxis_title="Cumulative share of funding",
            legend=dict(orientation="h", y=-0.15),
            height=380,
        )
        fig.update_xaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False, tickformat=".0%")
        fig.update_yaxes(showgrid=True, gridcolor="#F1EFE8", zeroline=False, tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.markdown(callout(
        "Lorenz curve renders from live data in the deployed app.",
        "info"
    ), unsafe_allow_html=True)

st.markdown(section_rule("Grants vs loans discrepancy"), unsafe_allow_html=True)

st.markdown(callout(
    "NEF grants and loans sum to <strong>R114.5M more</strong> than the total disbursed figure. "
    "This likely reflects uncommitted facilities — approved but not yet drawn down. "
    "It is a data quality issue that limits full accountability of the NEF record."
), unsafe_allow_html=True)

st.markdown(section_rule("What this means"), unsafe_allow_html=True)

st.markdown("""
<p>
A development finance programme with a Gini of 0.56 is replicating the structure it was
designed to disrupt. Small enterprises — the ones most likely to be owned by the intended
beneficiaries — receive the smallest deals and the smallest share of total capital.
</p>
<p style="margin-top:14px;">
The bottom 12% of deals share 0.7% of funding. The top 0.5% absorb 17%.
Both of these are policy outcomes, not statistical accidents.
</p>
""", unsafe_allow_html=True)

st.markdown(data_note(
    "Source: NEF Parliamentary Question PQ705 via dtic.gov.za · Dataset compiled by @AfikaSoyamba · "
    "Gini calculated using standard Lorenz curve methodology on deal-level disbursement data."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
