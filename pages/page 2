import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="Geographic Inequality", page_icon="📍", layout="wide")

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

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📍 Geographic Inequality")
st.markdown("### Where does the money flow across South Africa's 9 provinces?")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>Key finding:</strong> Gauteng and KwaZulu-Natal — South Africa's two wealthiest,
  most economically active provinces — received <strong>55.9% of all NEF disbursements</strong>
  and <strong>65.6% of all deals</strong>. Meanwhile, the Northern Cape received
  <strong>17.8% of all money</strong> through just 14 deals — almost entirely driven by
  two high-value, low-job-creation recipients. Unemployed South Africans live in every province.
  The money does not reach them equally.
</p>
</div>
""", unsafe_allow_html=True)

# ── Chart 1: Money vs Jobs divergence ─────────────────────────────────────────
st.markdown("## % of Money vs % of Jobs — The Divergence")
st.markdown("*When the share of money a province receives is much higher than its share of jobs, funding is inefficient.*")

prov_sorted = nef_provincial.sort_values('Pct_Disbursed', ascending=True)

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    name='% of Total Disbursed',
    y=prov_sorted['Province'],
    x=prov_sorted['Pct_Disbursed'],
    orientation='h',
    marker_color='#f0a500',
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
    marker_color='#00c9a7',
    opacity=0.9,
    text=[f"{v}%" for v in prov_sorted['Pct_Jobs']],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Share of Jobs: %{x}%<extra></extra>',
))
fig1.update_layout(
    barmode='group',
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(
        title='Share of National Total (%)',
        ticksuffix='%', gridcolor='#f1f5f9',
    ),
    yaxis=dict(title=''),
    legend=dict(
        orientation='h', yanchor='bottom', y=1.02,
        xanchor='right', x=1,
        font=dict(size=13),
    ),
    margin=dict(t=40, b=20, l=20, r=80),
    height=420,
)

# Add annotation for Northern Cape anomaly
fig1.add_annotation(
    x=17.8, y='Northern Cape',
    text='⚠ 17.8% of money<br>but only 1.0% of jobs',
    showarrow=True, arrowhead=2, arrowcolor='#e05c5c',
    ax=80, ay=0,
    font=dict(color='#e05c5c', size=11),
    bgcolor='#fef2f2', bordercolor='#e05c5c', borderwidth=1,
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="alert-box">
<p>
  <strong>Northern Cape anomaly:</strong> 17.8% of all NEF money — R641M — went to a province
  that received just 14 deals and accounts for only 1.0% of supported jobs.
  Two companies drive this: Khatu Industrial & Chemical (R534M, 26 jobs)
  and CK Mafutha (R77M, 4 jobs). Combined, they cost <strong>R18.8M per job</strong>.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 2: Cost per job by province ─────────────────────────────────────────
st.markdown("## Cost Per Job by Province")
st.markdown("*How much public money does it take to support one job in each province? Lower is better.*")

prov_cpj = nef_provincial.sort_values('Cost_Per_Job', ascending=True)
cpj_colors = ['#e05c5c' if v > 500000 else '#f0a500' if v > 100000 else '#00c9a7'
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
    x=113616, line_dash='dash', line_color='#64748b', line_width=1.5,
    annotation_text='National avg: R113,616',
    annotation_position='top',
    annotation_font=dict(color='#64748b', size=11),
)
fig2.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(
        title='Cost per Job (R)', gridcolor='#f1f5f9',
        tickformat='R,.0f',
    ),
    yaxis=dict(title=''),
    margin=dict(t=20, b=20, l=20, r=180),
    height=380,
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:16px; text-align:center;">
  <div style="font-size:11px; color:#166534; text-transform:uppercase; margin-bottom:6px;">🟢 Most Efficient</div>
  <div style="font-size:22px; font-weight:800; color:#166534;">Free State</div>
  <div style="font-size:14px; color:#15803d; margin-top:4px;">R58,075 per job</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:16px; text-align:center;">
  <div style="font-size:11px; color:#92400e; text-transform:uppercase; margin-bottom:6px;">🟡 National Average</div>
  <div style="font-size:22px; font-weight:800; color:#92400e;">All Provinces</div>
  <div style="font-size:14px; color:#b45309; margin-top:4px;">R113,616 per job</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:16px; text-align:center;">
  <div style="font-size:11px; color:#991b1b; text-transform:uppercase; margin-bottom:6px;">🔴 Least Efficient</div>
  <div style="font-size:22px; font-weight:800; color:#991b1b;">Northern Cape</div>
  <div style="font-size:14px; color:#b91c1c; margin-top:4px;">R1,967,485 per job</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 3: Provincial breakdown table ───────────────────────────────────────
st.markdown("## Full Provincial Breakdown")

with st.expander("📋 View detailed provincial data table", expanded=False):
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
st.markdown("## Concentration Statistics")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:22px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:14px;">Gauteng + KZN Combined</div>
  <table style="width:100%; font-size:14px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Share of all deals</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">65.6%</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Share of total money</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">55.9%</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Share of total jobs</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">71.4%</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:8px 0;">Number of provinces</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">2 of 9</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:22px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:14px;">Bottom 5 Provinces by Funding</div>
  <table style="width:100%; font-size:14px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Provinces</td>
      <td style="color:#1e293b; font-weight:700; text-align:right; font-size:12px;">
        NC, FS, Lim, MP, EC</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Share of total money</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">18.7%</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Share of total jobs</td>
      <td style="color:#1e293b; font-weight:700; text-align:right;">23.3%</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:8px 0;">Gini coefficient (provincial)</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">0.469</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<p>
  <strong>What the Gini means:</strong> A Gini coefficient of 0.469 on provincial disbursements
  indicates moderate-to-high geographic concentration. For context, South Africa's income Gini
  is ~0.63 — one of the highest in the world. The NEF's geographic funding distribution
  partially mirrors the same inequality it is mandated to address.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Source: NEF Parliamentary Question PQ705 · dtic.gov.za
</div>
""", unsafe_allow_html=True)