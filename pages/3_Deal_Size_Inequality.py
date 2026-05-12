import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Deal Size Inequality", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

st.markdown(page_masthead(
    "Section 3 of 5 &nbsp;·&nbsp; Deal Size Inequality",
    "The Money Is Not<br><em>Evenly Spread</em>",
    "The NEF deal-size Gini coefficient is 0.56 — approaching South Africa's own income "
    "inequality levels. A programme designed to correct inequality is itself unequal."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Key finding:</strong> The NEF operates a two-speed system. "
    "The bottom 12% of deals — under R1 million — share just <strong>0.7% of all disbursed "
    "money</strong>. The top 0.5% of deals — over R50 million — absorb <strong>17% of all "
    "money</strong>. The Lorenz curve confirms this: the NEF's deal-size Gini coefficient is "
    "<strong>0.56</strong>, approaching South Africa's own income inequality levels."
), unsafe_allow_html=True)

# ── Original hardcoded data ────────────────────────────────────────────────────
deal_sizes = pd.DataFrame({
    'Bracket':       ['Under R1m','R1m–R5m','R5m–R10m','R10m–R25m','R25m–R50m','R50m+'],
    'Deals':         [47, 130, 106, 87, 20, 2],
    'Pct_Deals':     [12.0, 33.2, 27.0, 22.2, 5.1, 0.5],
    'Disbursed_M':   [24.4, 335.1, 746.5, 1175.8, 703.4, 611.2],
    'Pct_Disbursed': [0.7, 9.3, 20.8, 32.7, 19.6, 17.0],
})

bracket_colors = ['#0F6E56','#0F6E56','#BA7517','#BA7517','#C53030','#C53030']

# ── Chart 1: Two-speed system ──────────────────────────────────────────────────
st.markdown(section_rule("Access vs money — the two-speed system"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Each bar shows a deal size bracket\'s share of deals vs share of money.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    fig_deals = go.Figure()
    fig_deals.add_trace(go.Bar(
        y=deal_sizes['Bracket'],
        x=deal_sizes['Pct_Deals'],
        orientation='h',
        marker_color=bracket_colors,
        text=[f"{v}%" for v in deal_sizes['Pct_Deals']],
        textposition='outside',
        textfont=dict(size=11, family='Source Serif 4, Georgia, serif'),
        hovertemplate='<b>%{y}</b><br>Share of Deals: %{x}%<extra></extra>',
    ))
    fig_deals = apply_plotly_theme(fig_deals, height=340)
    fig_deals.update_layout(
        title=dict(text='% of Total Deals', font=dict(size=13, color='#2C2C2A', family='Playfair Display, Georgia, serif')),
        xaxis=dict(title='Share of All Deals (%)', ticksuffix='%', gridcolor='#EDECEA', range=[0, 45]),
        yaxis=dict(title=''),
        margin=dict(t=40, b=24, l=20, r=60),
        showlegend=False,
    )
    st.plotly_chart(fig_deals, use_container_width=True)

with col2:
    fig_money = go.Figure()
    fig_money.add_trace(go.Bar(
        y=deal_sizes['Bracket'],
        x=deal_sizes['Pct_Disbursed'],
        orientation='h',
        marker_color=bracket_colors,
        text=[f"{v}%" for v in deal_sizes['Pct_Disbursed']],
        textposition='outside',
        textfont=dict(size=11, family='Source Serif 4, Georgia, serif'),
        hovertemplate='<b>%{y}</b><br>Share of Money: %{x}%<extra></extra>',
    ))
    fig_money = apply_plotly_theme(fig_money, height=340)
    fig_money.update_layout(
        title=dict(text='% of Total Money Disbursed', font=dict(size=13, color='#2C2C2A', family='Playfair Display, Georgia, serif')),
        xaxis=dict(title='Share of Total Disbursed (%)', ticksuffix='%', gridcolor='#EDECEA', range=[0, 45]),
        yaxis=dict(title=''),
        margin=dict(t=40, b=24, l=20, r=60),
        showlegend=False,
    )
    st.plotly_chart(fig_money, use_container_width=True)

st.markdown("""
<div style="background:#F1EFE8; border:0.5px solid #D3D1C7; padding:12px 18px; font-size:12px; color:#5F5E5A; font-family:'Source Serif 4',Georgia,serif;">
  <span style="color:#0F6E56; font-weight:600;">Teal = small deals</span> (under R5m) &nbsp;·&nbsp;
  <span style="color:#BA7517; font-weight:600;">Amber = mid-tier</span> (R5m–R25m) &nbsp;·&nbsp;
  <span style="color:#C53030; font-weight:600;">Red = large deals</span> (over R25m)
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 2: Lorenz curve ──────────────────────────────────────────────────────
st.markdown(section_rule("Lorenz curve — measuring funding concentration"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">The further the curve bows below the diagonal, the more concentrated the funding. A straight diagonal = perfect equality.</div>', unsafe_allow_html=True)

cum_deals     = np.cumsum(deal_sizes['Pct_Deals'].values) / 100
cum_disbursed = np.cumsum(deal_sizes['Pct_Disbursed'].values) / 100
cum_deals     = np.insert(cum_deals, 0, 0)
cum_disbursed = np.insert(cum_disbursed, 0, 0)

fig_lorenz = go.Figure()
fig_lorenz.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1],
    mode='lines',
    line=dict(color='#D3D1C7', dash='dash', width=1.5),
    name='Perfect Equality',
    hoverinfo='skip',
))
fig_lorenz.add_trace(go.Scatter(
    x=np.concatenate([cum_deals, cum_deals[::-1]]),
    y=np.concatenate([cum_deals, cum_disbursed[::-1]]),
    fill='toself',
    fillcolor='rgba(197,48,48,0.08)',
    line=dict(color='rgba(0,0,0,0)'),
    name='Inequality Area',
    hoverinfo='skip',
))
fig_lorenz.add_trace(go.Scatter(
    x=cum_deals, y=cum_disbursed,
    mode='lines+markers',
    line=dict(color='#BA7517', width=2.5),
    marker=dict(size=8, color='#BA7517', line=dict(color='#FAFAF8', width=2)),
    name='NEF Lorenz Curve',
    hovertemplate='Cumulative Deals: %{x:.0%}<br>Cumulative Money: %{y:.0%}<extra></extra>',
))
fig_lorenz.add_annotation(
    x=cum_deals[-2], y=cum_disbursed[-2],
    text='Top 5.6% of deals<br>receive 36% of money',
    showarrow=True, arrowhead=2, arrowcolor='#C53030',
    ax=-100, ay=-40,
    font=dict(color='#C53030', size=11, family='Source Serif 4, Georgia, serif'),
    bgcolor='#FDF0F0', bordercolor='#C53030', borderwidth=1,
)
fig_lorenz = apply_plotly_theme(fig_lorenz, height=440)
fig_lorenz.update_layout(
    xaxis=dict(title='Cumulative Share of Deals', tickformat='.0%', gridcolor='#EDECEA', range=[0, 1.05]),
    yaxis=dict(title='Cumulative Share of Disbursements', tickformat='.0%', gridcolor='#EDECEA', range=[0, 1.05]),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=11, family='Source Serif 4, Georgia, serif')),
    margin=dict(t=40, b=24, l=20, r=20),
)
st.plotly_chart(fig_lorenz, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:20px;">
  <div class="info-card-label" style="margin-bottom:12px;">Gini Coefficients — Context</div>
  <table class="info-card-table">
    <tr><td>NEF deal-size Gini</td><td style="text-align:right; color:#A32D2D; font-weight:700;">0.560</td></tr>
    <tr><td>SA income Gini</td><td style="text-align:right; color:#A32D2D; font-weight:700;">~0.630</td></tr>
    <tr><td>Perfect equality</td><td style="text-align:right; color:#0F6E56; font-weight:700;">0.000</td></tr>
    <tr><td>Total concentration</td><td style="text-align:right; font-weight:700;">1.000</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:20px;">
  <div class="info-card-label" style="margin-bottom:12px;">The Scale of the Gap</div>
  <p style="font-size:14px; color:#2C2C2A; line-height:1.75; font-family:'Source Serif 4',Georgia,serif; margin:0;">
    The average disbursement for an <strong>under-R1m deal</strong> is approximately
    <strong>R520,000</strong>. The average for an <strong>R50m+ deal</strong> is
    <strong>R305,600,000</strong>. A <strong>587× difference</strong> in money
    per recipient — within the same public programme.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Grants vs Loans ────────────────────────────────────────────────────────────
st.markdown(section_rule("Grants vs loans — who receives non-repayable funding?"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #0F6E56; padding:18px; text-align:center;">
  <div class="info-card-label" style="margin-bottom:8px;">Companies Receiving Grants</div>
  <div style="font-family:'Playfair Display',serif; font-size:30px; font-weight:700; color:#111110;">77</div>
  <div style="font-size:12px; color:#888780; margin-top:4px; font-family:'Source Serif 4',serif;">19.6% of portfolio</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #BA7517; padding:18px; text-align:center;">
  <div class="info-card-label" style="margin-bottom:8px;">Total Grants Disbursed</div>
  <div style="font-family:'Playfair Display',serif; font-size:30px; font-weight:700; color:#BA7517;">R194.8M</div>
  <div style="font-size:12px; color:#888780; margin-top:4px; font-family:'Source Serif 4',serif;">5.2% of all funding</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #C53030; padding:18px; text-align:center;">
  <div class="info-card-label" style="margin-bottom:8px;">Loans-Only Companies</div>
  <div style="font-family:'Playfair Display',serif; font-size:30px; font-weight:700; color:#111110;">315</div>
  <div style="font-size:12px; color:#888780; margin-top:4px; font-family:'Source Serif 4',serif;">80.4% of portfolio</div>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Data discrepancy flagged:</strong> Grants (R194.8M) + Loans (R3,516.2M) = R3,710.9M — "
    "but total disbursed is stated as R3,596.4M. The <strong>R114.5M gap (3.2%)</strong> likely "
    "reflects committed but not yet drawn-down facilities. This is a data quality limitation "
    "in the source parliamentary question.",
    "alert"
), unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
