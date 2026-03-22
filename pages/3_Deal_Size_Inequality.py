import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Deal Size Inequality", page_icon="📊", layout="wide")

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #fafafa; }
  [data-testid="stSidebar"]          { background: #f1f5f9; border-right: 1px solid #e2e8f0; }
  h1, h2, h3 { color: #1e293b; font-family: 'Georgia', serif; }
  p, li      { color: #334155; font-size: 15px; line-height: 1.75; }
  .finding-box {
    background: #fffbeb; border-left: 5px solid #f0a500;
    border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 18px 0;
  }
  .finding-box p { color: #1e293b; font-size: 15px; margin: 0; }
  .alert-box {
    background: #fef2f2; border-left: 5px solid #e05c5c;
    border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 18px 0;
  }
  .alert-box p { color: #7f1d1d; font-size: 15px; margin: 0; }
  .info-box {
    background: #f0fdfa; border-left: 5px solid #00c9a7;
    border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 18px 0;
  }
  .info-box p { color: #134e4a; font-size: 15px; margin: 0; }
  .section-divider { border: none; border-top: 1px solid #e2e8f0; margin: 32px 0; }
  #MainMenu { visibility: hidden; } footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
deal_sizes = pd.DataFrame({
    'Bracket':       ['Under R1m','R1m–R5m','R5m–R10m','R10m–R25m','R25m–R50m','R50m+'],
    'Deals':         [47, 130, 106, 87, 20, 2],
    'Pct_Deals':     [12.0, 33.2, 27.0, 22.2, 5.1, 0.5],
    'Disbursed_M':   [24.4, 335.1, 746.5, 1175.8, 703.4, 611.2],
    'Pct_Disbursed': [0.7, 9.3, 20.8, 32.7, 19.6, 17.0],
})

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📊 Deal Size Inequality")
st.markdown("### Who gets access at what scale — and what does that reveal?")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>Key finding:</strong> The NEF operates a two-speed system.
  The bottom 12% of deals — under R1 million — share just <strong>0.7% of all disbursed money</strong>.
  The top 0.5% of deals — over R50 million — absorb <strong>17% of all money</strong>.
  The Lorenz curve confirms this: the NEF's deal-size Gini coefficient is <strong>0.56</strong>,
  approaching South Africa's own income inequality levels. Public development capital
  is not being distributed equitably even within the programme itself.
</p>
</div>
""", unsafe_allow_html=True)

# ── Chart 1: Side-by-side % deals vs % money ──────────────────────────────────
st.markdown("## Access vs Money — The Two-Speed System")
st.markdown("*Each bar shows a deal size bracket's share of deals (how many companies) vs share of money (how much they got).*")

bracket_colors = ['#00c9a7','#00c9a7','#f0a500','#f0a500','#e05c5c','#e05c5c']

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
        hovertemplate='<b>%{y}</b><br>Share of Deals: %{x}%<extra></extra>',
    ))
    fig_deals.update_layout(
        title=dict(text='% of Total Deals', font=dict(size=14, color='#1e293b')),
        plot_bgcolor='white', paper_bgcolor='#fafafa',
        xaxis=dict(title='Share of All Deals (%)', ticksuffix='%', gridcolor='#f1f5f9', range=[0, 45]),
        yaxis=dict(title=''),
        margin=dict(t=40, b=20, l=20, r=60),
        height=340, showlegend=False,
        font=dict(color='#334155'),
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
        hovertemplate='<b>%{y}</b><br>Share of Money: %{x}%<extra></extra>',
    ))
    fig_money.update_layout(
        title=dict(text='% of Total Money Disbursed', font=dict(size=14, color='#1e293b')),
        plot_bgcolor='white', paper_bgcolor='#fafafa',
        xaxis=dict(title='Share of Total Disbursed (%)', ticksuffix='%', gridcolor='#f1f5f9', range=[0, 45]),
        yaxis=dict(title=''),
        margin=dict(t=40, b=20, l=20, r=60),
        height=340, showlegend=False,
        font=dict(color='#334155'),
    )
    st.plotly_chart(fig_money, use_container_width=True)

st.markdown("""
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;
            padding:14px 20px; font-size:13px; color:#475569;">
  🟢 <strong>Teal = small deals</strong> (under R5m) &nbsp;·&nbsp;
  🟡 <strong>Gold = mid-tier deals</strong> (R5m–R25m) &nbsp;·&nbsp;
  🔴 <strong>Red = large deals</strong> (over R25m)
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 2: Lorenz curve ──────────────────────────────────────────────────────
st.markdown("## Lorenz Curve — Measuring Funding Concentration")
st.markdown("*The further the curve bows below the diagonal, the more concentrated the funding. A straight diagonal = perfect equality.*")

cum_deals     = np.cumsum(deal_sizes['Pct_Deals'].values) / 100
cum_disbursed = np.cumsum(deal_sizes['Pct_Disbursed'].values) / 100
cum_deals     = np.insert(cum_deals, 0, 0)
cum_disbursed = np.insert(cum_disbursed, 0, 0)

fig_lorenz = go.Figure()
# Equality line
fig_lorenz.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1],
    mode='lines',
    line=dict(color='#94a3b8', dash='dash', width=1.5),
    name='Perfect Equality',
    hoverinfo='skip',
))
# Shaded inequality area
fig_lorenz.add_trace(go.Scatter(
    x=np.concatenate([cum_deals, cum_deals[::-1]]),
    y=np.concatenate([cum_deals, cum_disbursed[::-1]]),
    fill='toself',
    fillcolor='rgba(224, 92, 92, 0.12)',
    line=dict(color='rgba(0,0,0,0)'),
    name='Inequality Area',
    hoverinfo='skip',
))
# Lorenz curve
fig_lorenz.add_trace(go.Scatter(
    x=cum_deals, y=cum_disbursed,
    mode='lines+markers',
    line=dict(color='#f0a500', width=3),
    marker=dict(size=9, color='#f0a500', line=dict(color='white', width=2)),
    name='NEF Lorenz Curve',
    hovertemplate='Cumulative Deals: %{x:.0%}<br>Cumulative Money: %{y:.0%}<extra></extra>',
))
fig_lorenz.add_annotation(
    x=cum_deals[-2], y=cum_disbursed[-2],
    text='Top 5.6% of deals<br>receive 36% of money',
    showarrow=True, arrowhead=2, arrowcolor='#e05c5c',
    ax=-100, ay=-40,
    font=dict(color='#e05c5c', size=11),
    bgcolor='#fef2f2', bordercolor='#e05c5c', borderwidth=1,
)
fig_lorenz.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(
        title='Cumulative Share of Deals',
        tickformat='.0%', gridcolor='#f1f5f9', range=[0, 1.05],
    ),
    yaxis=dict(
        title='Cumulative Share of Disbursements',
        tickformat='.0%', gridcolor='#f1f5f9', range=[0, 1.05],
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(t=40, b=20, l=20, r=20),
    height=440,
)
st.plotly_chart(fig_lorenz, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:20px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">Gini Coefficients — Context</div>
  <table style="width:100%; font-size:14px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">NEF deal-size Gini</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">0.560</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">SA income Gini</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">~0.630</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">Perfect equality</td>
      <td style="color:#00c9a7; font-weight:700; text-align:right;">0.000</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:7px 0;">Total concentration</td>
      <td style="color:#64748b; font-weight:700; text-align:right;">1.000</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:20px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">The 34× Gap</div>
  <p style="font-size:14px; color:#334155; line-height:1.7;">
    The average disbursement for an <strong>under-R1m deal</strong> is approximately
    <strong>R520,000</strong>. The average for an <strong>R50m+ deal</strong> is
    <strong>R305,600,000</strong>. That is a <strong>587× difference</strong>
    in money per recipient — within the same public development finance programme.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Grants vs Loans ────────────────────────────────────────────────────────────
st.markdown("## Grants vs Loans — Who Receives Non-Repayable Funding?")
st.markdown("*Grants are the most direct form of public support — they do not need to be repaid.*")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:white; border-top:3px solid #00c9a7; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; text-align:center;">
  <div style="font-size:11px; color:#64748b; text-transform:uppercase; margin-bottom:8px;">
    Companies Receiving Grants</div>
  <div style="font-size:28px; font-weight:800; color:#1e293b;">77</div>
  <div style="font-size:12px; color:#94a3b8; margin-top:4px;">19.6% of portfolio</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:white; border-top:3px solid #f0a500; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; text-align:center;">
  <div style="font-size:11px; color:#64748b; text-transform:uppercase; margin-bottom:8px;">
    Total Grants Disbursed</div>
  <div style="font-size:28px; font-weight:800; color:#1e293b;">R194.8M</div>
  <div style="font-size:12px; color:#94a3b8; margin-top:4px;">5.2% of all funding</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:white; border-top:3px solid #e05c5c; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; text-align:center;">
  <div style="font-size:11px; color:#64748b; text-transform:uppercase; margin-bottom:8px;">
    Loans-Only Companies</div>
  <div style="font-size:28px; font-weight:800; color:#1e293b;">315</div>
  <div style="font-size:12px; color:#94a3b8; margin-top:4px;">80.4% of portfolio</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="alert-box" style="margin-top:20px;">
<p>
  <strong>Data discrepancy flagged:</strong> Grants (R194.8M) + Loans (R3,516.2M) = R3,710.9M —
  but total disbursed is stated as R3,596.4M. The <strong>R114.5M gap (3.2%)</strong> likely
  reflects committed but not yet drawn-down facilities. This is a data quality limitation
  in the source parliamentary question.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Source: NEF Parliamentary Question PQ705 · dtic.gov.za
</div>
""", unsafe_allow_html=True)