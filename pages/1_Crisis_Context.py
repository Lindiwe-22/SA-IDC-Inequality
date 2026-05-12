import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Crisis Context", page_icon="📉", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

st.markdown(page_masthead(
    "Section 1 of 5 &nbsp;·&nbsp; Context",
    "The Crisis the DFIs<br>Exist to <em>Solve</em>",
    "Before interrogating where the money goes, the scale of the problem must be established. "
    "Every cost-per-job figure in this analysis must be read against one number — 31.9%. "
    "That is the share of South Africans who want to work and cannot find work."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Why this matters:</strong> Development finance institutions exist to solve unemployment. "
    "Every cost-per-job figure, every provincial allocation, and every sector decision in this "
    "analysis must be read against one number — <strong>31.9%</strong>. That is the share of "
    "South Africans who want to work and cannot find work. By the expanded definition, it is 42.4%. "
    "Among youth aged 15–24, it exceeds 60%.",
    "alert"
), unsafe_allow_html=True)

# ── Data (original, unchanged) ─────────────────────────────────────────────────
unemployment = pd.DataFrame({
    'Category': [
        'Official Unemployment',
        'Expanded Unemployment (LU3)',
        'Youth Unemployment (15–34)',
        'Youth Unemployment (15–24)',
    ],
    'Rate': [31.9, 42.4, 46.1, 60.0],
    'Color': ['#A32D2D', '#A32D2D', '#C53030', '#8B1A1A'],
})

global_comparisons = pd.DataFrame({
    'Country': ['South Africa', 'Nigeria', 'Kenya', 'Brazil', 'India', 'USA', 'Germany', 'Global Avg'],
    'Rate':    [31.9, 5.3, 5.7, 7.8, 8.0, 3.7, 3.0, 6.5],
    'Color':   ['#A32D2D','#BA7517','#BA7517','#185FA5','#185FA5','#0F6E56','#0F6E56','#888780'],
})

# ── Chart 1 ────────────────────────────────────────────────────────────────────
st.markdown(section_rule("South Africa's unemployment — four measures"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Source: Stats SA Quarterly Labour Force Survey Q3 2025</div>', unsafe_allow_html=True)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=unemployment['Category'],
    y=unemployment['Rate'],
    marker_color=unemployment['Color'],
    text=[f"{v}%" for v in unemployment['Rate']],
    textposition='outside',
    textfont=dict(size=13, color='#2C2C2A', family='Source Serif 4, Georgia, serif'),
    hovertemplate='<b>%{x}</b><br>Rate: %{y}%<extra></extra>',
))
fig1.add_hline(
    y=6.5, line_dash='dash', line_color='#B4B2A9', line_width=1.5,
    annotation_text='Global average ~6.5%',
    annotation_position='top right',
    annotation_font=dict(color='#888780', size=11),
)
fig1 = apply_plotly_theme(fig1, height=400)
fig1.update_layout(
    yaxis=dict(title='Unemployment Rate (%)', range=[0, 75], ticksuffix='%', gridcolor='#EDECEA'),
    xaxis=dict(title='', tickfont=dict(size=12)),
    showlegend=False,
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(callout(
    "<strong>Finding:</strong> South Africa's official unemployment rate is nearly "
    "<strong>5× the global average</strong>. For youth aged 15–24, it is nearly "
    "<strong>10× the global benchmark</strong>. Stats SA has recorded unemployment "
    "above 25% consistently since 2008."
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 2 ────────────────────────────────────────────────────────────────────
st.markdown(section_rule("Global comparison — SA vs peer economies"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">South Africa\'s unemployment is not just high by African standards — it is exceptional globally.</div>', unsafe_allow_html=True)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=global_comparisons['Country'],
    y=global_comparisons['Rate'],
    marker_color=global_comparisons['Color'],
    text=[f"{v}%" for v in global_comparisons['Rate']],
    textposition='outside',
    textfont=dict(size=12, color='#2C2C2A', family='Source Serif 4, Georgia, serif'),
    hovertemplate='<b>%{x}</b><br>Unemployment: %{y}%<extra></extra>',
))
fig2 = apply_plotly_theme(fig2, height=380)
fig2.update_layout(
    yaxis=dict(title='Unemployment Rate (%)', range=[0, 40], ticksuffix='%', gridcolor='#EDECEA'),
    xaxis=dict(title='', tickfont=dict(size=12)),
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── DFI mandate ────────────────────────────────────────────────────────────────
st.markdown(section_rule("The DFI mandate"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:22px;">
  <div class="info-card-label" style="margin-bottom:12px;">What DFIs are supposed to do</div>
  <ul style="color:#2C2C2A; font-size:14px; line-height:2.1; padding-left:18px; font-family:'Source Serif 4',Georgia,serif;">
    <li>Fund businesses that create sustainable employment</li>
    <li>Prioritise transformation and BEE ownership structures</li>
    <li>Reach sectors and geographies underserved by private finance</li>
    <li>Support small and micro-enterprises with limited credit access</li>
    <li>Diversify the economy beyond its historical mining base</li>
  </ul>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:22px;">
  <div class="info-card-label" style="margin-bottom:12px;">The benchmark question</div>
  <p style="color:#2C2C2A; font-size:14px; line-height:1.8; font-family:'Source Serif 4',Georgia,serif;">
    If the IDC and NEF together deployed <strong>R69.5 billion</strong> of public money
    over the period examined, and South Africa still has <strong>13.3 million
    underutilised workers</strong> — what is the cost per job created?
    And more importantly: <strong>who received the money, and did it reach
    those who need it most?</strong>
  </p>
  <p style="color:#888780; font-size:12px; margin-top:12px; font-family:'Source Serif 4',Georgia,serif;">
    Use the sidebar to explore the evidence across five analytical sections.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── At a glance ────────────────────────────────────────────────────────────────
st.markdown(section_rule("At a glance — the numbers behind the crisis"), unsafe_allow_html=True)
st.markdown("""
<div class="metric-row">
  <div class="metric-card red">
    <div class="metric-label">Underutilised persons</div>
    <div class="metric-value red">13.3M</div>
    <div class="metric-sub">SA labour market · Stats SA Q3 2025</div>
  </div>
  <div class="metric-card gold">
    <div class="metric-label">Total IDC + NEF funding</div>
    <div class="metric-value amber">R69.5B</div>
    <div class="metric-sub">Combined in this dataset</div>
  </div>
  <div class="metric-card teal">
    <div class="metric-label">NEF jobs supported</div>
    <div class="metric-value teal">31,654</div>
    <div class="metric-sub">Self-reported, parliamentary question</div>
  </div>
  <div class="metric-card red">
    <div class="metric-label">IDC jobs reported</div>
    <div class="metric-value red">0</div>
    <div class="metric-sub">No public cost-per-job data published</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
