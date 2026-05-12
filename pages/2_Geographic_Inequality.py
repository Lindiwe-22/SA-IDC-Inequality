import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Geographic Inequality", page_icon="📍", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

st.markdown(page_masthead(
    "Section 2 of 5 &nbsp;·&nbsp; Geographic Inequality",
    "Where Does the<br>Money <em>Land?</em>",
    "Two provinces received 55.9% of all NEF disbursements. The provincial Gini "
    "coefficient is 0.469. This is not random — it is a measurable pattern with "
    "measurable consequences."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Key finding:</strong> Gauteng and KwaZulu-Natal — South Africa's two wealthiest, "
    "most economically active provinces — received <strong>55.9% of all NEF disbursements</strong> "
    "and <strong>65.6% of all deals</strong>. Meanwhile, the Northern Cape received "
    "<strong>17.8% of all money</strong> through just 14 deals — almost entirely driven by "
    "two high-value, low-job-creation recipients. Unemployed South Africans live in every province. "
    "The money does not reach them equally."
), unsafe_allow_html=True)

# ── Original hardcoded data ────────────────────────────────────────────────────
nef_provincial = pd.DataFrame({
    'Province':       ['Gauteng','KwaZulu-Natal','Northern Cape','Western Cape',
                       'Eastern Cape','Mpumalanga','Limpopo','Free State','North West'],
    'Deals':          [135, 122, 14, 31, 23, 18, 19, 10, 20],
    'Disbursed_M':    [1041.3, 970.5, 641.4, 271.9, 203.4, 150.0, 133.0, 109.2, 75.7],
    'Jobs':           [14138, 8440, 326, 1363, 1904, 1098, 1741, 1881, 763],
    'Cost_Per_Job':   [73650, 114992, 1967485, 199490, 106828, 136650, 76372, 58075, 99156],
    'Pct_Disbursed':  [29.0, 27.0, 17.8, 7.6, 5.7, 4.2, 3.7, 3.0, 2.1],
    'Pct_Jobs':       [44.7, 26.7, 1.0, 4.3, 6.0, 3.5, 5.5, 5.9, 2.4],
})

# ── Chart 1: Money vs Jobs ─────────────────────────────────────────────────────
st.markdown(section_rule("Share of money vs share of jobs — by province"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">When the share of money a province receives far exceeds its share of jobs, funding is inefficient.</div>', unsafe_allow_html=True)

prov_sorted = nef_provincial.sort_values('Pct_Disbursed', ascending=True)
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    name='% of Total Disbursed',
    y=prov_sorted['Province'],
    x=prov_sorted['Pct_Disbursed'],
    orientation='h',
    marker_color='#BA7517',
    opacity=0.9,
    text=[f"{v}%" for v in prov_sorted['Pct_Disbursed']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Share of Money: %{x}%<extra></extra>',
))
fig1.add_trace(go.Bar(
    name='% of Total Jobs',
    y=prov_sorted['Province'],
    x=prov_sorted['Pct_Jobs'],
    orientation='h',
    marker_color='#0F6E56',
    opacity=0.9,
    text=[f"{v}%" for v in prov_sorted['Pct_Jobs']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Share of Jobs: %{x}%<extra></extra>',
))
fig1.update_layout(barmode='group')
fig1.add_annotation(
    x=17.8, y='Northern Cape',
    text='17.8% of money<br>only 1.0% of jobs',
    showarrow=True, arrowhead=2, arrowcolor='#C53030',
    ax=80, ay=0,
    font=dict(color='#C53030', size=11, family='Source Serif 4, Georgia, serif'),
    bgcolor='#FDF0F0', bordercolor='#C53030', borderwidth=1,
)
fig1 = apply_plotly_theme(fig1, height=420)
fig1.update_layout(
    xaxis=dict(title='Share of National Total (%)', ticksuffix='%', gridcolor='#EDECEA'),
    yaxis=dict(title=''),
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
        font=dict(size=12, family='Source Serif 4, Georgia, serif'),
    ),
    margin=dict(t=40, b=24, l=20, r=100),
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(callout(
    "<strong>Northern Cape anomaly:</strong> 17.8% of all NEF money — R641M — went to a province "
    "that received just 14 deals and accounts for only 1.0% of supported jobs. "
    "Two companies drive this: Khatu Industrial & Chemical (R534M, 26 jobs) "
    "and CK Mafutha (R77M, 4 jobs). Combined, they cost <strong>R18.8M per job</strong>.",
    "alert"
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 2: Cost per job ──────────────────────────────────────────────────────
st.markdown(section_rule("Cost per job by province"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">How much public money does it take to support one job in each province? Lower is better.</div>', unsafe_allow_html=True)

prov_cpj = nef_provincial.sort_values('Cost_Per_Job', ascending=True)
cpj_colors = ['#C53030' if v > 500000 else '#BA7517' if v > 100000 else '#0F6E56'
              for v in prov_cpj['Cost_Per_Job']]

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    y=prov_cpj['Province'],
    x=prov_cpj['Cost_Per_Job'],
    orientation='h',
    marker_color=cpj_colors,
    text=[f"R{v:,.0f}" for v in prov_cpj['Cost_Per_Job']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Cost per Job: R%{x:,.0f}<extra></extra>',
))
fig2.add_vline(
    x=113616, line_dash='dash', line_color='#888780', line_width=1.5,
    annotation_text='National avg: R113,616',
    annotation_position='top',
    annotation_font=dict(color='#888780', size=11, family='Source Serif 4, Georgia, serif'),
)
fig2 = apply_plotly_theme(fig2, height=380)
fig2.update_layout(
    xaxis=dict(title='Cost per Job (R)', gridcolor='#EDECEA'),
    yaxis=dict(title=''),
    margin=dict(t=24, b=24, l=20, r=200),
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:#E8F5EF; border-left:3px solid #0F6E56; padding:16px;">
  <div class="info-card-label" style="color:#084D3A; margin-bottom:6px;">Most Efficient</div>
  <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:#084D3A;">Free State</div>
  <div style="font-size:13px; color:#0F6E56; margin-top:4px; font-family:'Source Serif 4',serif;">R58,075 per job</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FDF6E8; border-left:3px solid #BA7517; padding:16px;">
  <div class="info-card-label" style="color:#5C3A06; margin-bottom:6px;">National Average</div>
  <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:#5C3A06;">All Provinces</div>
  <div style="font-size:13px; color:#BA7517; margin-top:4px; font-family:'Source Serif 4',serif;">R113,616 per job</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:#FDF0F0; border-left:3px solid #C53030; padding:16px;">
  <div class="info-card-label" style="color:#7A1F1F; margin-bottom:6px;">Least Efficient</div>
  <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:700; color:#7A1F1F;">Northern Cape</div>
  <div style="font-size:13px; color:#C53030; margin-top:4px; font-family:'Source Serif 4',serif;">R1,967,485 per job</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Detailed table ─────────────────────────────────────────────────────────────
st.markdown(section_rule("Full provincial breakdown"), unsafe_allow_html=True)

with st.expander("View detailed provincial data table", expanded=False):
    display_df = nef_provincial[[
        'Province','Deals','Disbursed_M','Jobs','Cost_Per_Job','Pct_Disbursed','Pct_Jobs'
    ]].copy()
    display_df.columns = [
        'Province','Deals','Disbursed (R millions)','Jobs Supported',
        'Cost per Job (R)','% of Total Money','% of Total Jobs'
    ]
    display_df['Disbursed (R millions)'] = display_df['Disbursed (R millions)'].map('R{:,.1f}M'.format)
    display_df['Cost per Job (R)'] = display_df['Cost per Job (R)'].map('R{:,.0f}'.format)
    display_df['% of Total Money'] = display_df['% of Total Money'].map('{:.1f}%'.format)
    display_df['% of Total Jobs'] = display_df['% of Total Jobs'].map('{:.1f}%'.format)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Concentration stats ────────────────────────────────────────────────────────
st.markdown(section_rule("Concentration statistics"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:22px;">
  <div class="info-card-label" style="margin-bottom:14px;">Gauteng + KZN Combined</div>
  <table class="info-card-table">
    <tr><td>Share of all deals</td><td style="text-align:right; font-weight:600;">65.6%</td></tr>
    <tr><td>Share of total money</td><td style="text-align:right; font-weight:600;">55.9%</td></tr>
    <tr><td>Share of total jobs</td><td style="text-align:right; font-weight:600;">71.4%</td></tr>
    <tr><td>Number of provinces</td><td style="text-align:right; font-weight:600;">2 of 9</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:22px;">
  <div class="info-card-label" style="margin-bottom:14px;">Bottom 5 Provinces by Funding</div>
  <table class="info-card-table">
    <tr><td>Provinces</td><td style="text-align:right; font-weight:600; font-size:11px;">NC, FS, Lim, MP, EC</td></tr>
    <tr><td>Share of total money</td><td style="text-align:right; font-weight:600;">18.7%</td></tr>
    <tr><td>Share of total jobs</td><td style="text-align:right; font-weight:600;">23.3%</td></tr>
    <tr><td>Provincial Gini coefficient</td><td style="text-align:right; font-weight:600; color:#A32D2D;">0.469</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "<strong>What the Gini means:</strong> A Gini of 0.469 on provincial disbursements indicates "
    "moderate-to-high geographic concentration. South Africa's income Gini is ~0.63 — one of the "
    "highest in the world. The NEF's geographic funding distribution partially mirrors "
    "the same inequality it is mandated to address.",
    "info"
), unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
