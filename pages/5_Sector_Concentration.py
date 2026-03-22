import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Sector Concentration", page_icon="⛏️", layout="wide")

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
idc_sectors = pd.DataFrame({
    'Sector': [
        'Mining and Metals', 'Basic Metals & Mining',
        'Automotive & Transport', 'Agro Processing & Agriculture',
        'Basic & Speciality Chemicals', 'Heavy Manufacturing',
        'Industrial Infrastructure', 'Machinery & Equipment',
        'Chemical Products & Pharma', 'Clothing & Textiles',
        'Media & Motion Pictures', 'New Industries',
    ],
    'Investment_B': [9.74, 6.46, 2.08, 2.38, 1.79, 1.67,
                     1.24, 1.16, 0.92, 0.50, 0.38, 0.37],
    'Category': [
        'Mining/Metals','Mining/Metals','Manufacturing','Agriculture',
        'Chemicals','Manufacturing','Infrastructure','Manufacturing',
        'Chemicals','Manufacturing','Other','New Industries',
    ],
})
idc_sectors = idc_sectors.sort_values('Investment_B', ascending=True).reset_index(drop=True)

idc_fiscal = pd.DataFrame({
    'FY':         ['2017-18','2018-19','2019-20','2020-21','2021-22','2022-23','2024-25'],
    'Deals':      [140, 150, 66, 29, 127, 141, 201],
    'Invest_B':   [9.29, 5.30, 5.51, 1.94, 9.63, 17.01, 17.24],
    'AvgDeal_M':  [66.4, 35.3, 83.5, 66.9, 75.8, 120.6, 85.8],
})

cat_colors = {
    'Mining/Metals': '#e05c5c',
    'Manufacturing': '#f0a500',
    'Agriculture':   '#00c9a7',
    'Chemicals':     '#a78bfa',
    'Infrastructure':'#4e8df5',
    'Other':         '#94a3b8',
    'New Industries':'#34d399',
}
bar_colors = [cat_colors[c] for c in idc_sectors['Category']]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# ⛏️ Sector Concentration & Accountability")
st.markdown("### Is the IDC diversifying the economy — or entrenching historical patterns?")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>Key finding:</strong> Among the 12 named sectors in the IDC dataset,
  <strong>Mining and Metals alone accounts for 56.5%</strong> of all attributed investment —
  R16.2 billion. New Industries, the IDC's forward-looking diversification mandate
  (biotech, solar, AI), received just <strong>1.3%</strong> of named-sector funding —
  R371 million. South Africa's economy was built on mining. The IDC, at least by this measure,
  is reinforcing that structure rather than transforming it.
</p>
</div>
""", unsafe_allow_html=True)

# ── Chart 1: Sector investment ─────────────────────────────────────────────────
st.markdown("## IDC Investment by Sector (Named Sectors — R28.7B of R65.9B total)")
st.markdown("*56.5% of total IDC investment has no sector attribution in the public dashboard — a significant transparency gap.*")

fig_sectors = go.Figure()
fig_sectors.add_trace(go.Bar(
    y=idc_sectors['Sector'],
    x=idc_sectors['Investment_B'],
    orientation='h',
    marker_color=bar_colors,
    text=[f"R{v:.2f}B" for v in idc_sectors['Investment_B']],
    textposition='outside',
    customdata=idc_sectors['Category'],
    hovertemplate=(
        '<b>%{y}</b><br>'
        'Investment: R%{x:.2f}B<br>'
        'Category: %{customdata}<extra></extra>'
    ),
))
mean_val = idc_sectors['Investment_B'].mean()
fig_sectors.add_vline(
    x=mean_val, line_dash='dash', line_color='#94a3b8', line_width=1.5,
    annotation_text=f'Mean: R{mean_val:.2f}B',
    annotation_position='top',
    annotation_font=dict(color='#64748b', size=11),
)
fig_sectors.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='Total Investment (R billions, FY2017–2025)', gridcolor='#f1f5f9'),
    yaxis=dict(title=''),
    margin=dict(t=30, b=20, l=20, r=80),
    height=440,
    showlegend=False,
)
st.plotly_chart(fig_sectors, use_container_width=True)

# Colour legend
legend_items = [
    ('#e05c5c', 'Mining / Metals'),
    ('#f0a500', 'Manufacturing'),
    ('#00c9a7', 'Agriculture'),
    ('#a78bfa', 'Chemicals'),
    ('#4e8df5', 'Infrastructure'),
    ('#34d399', 'New Industries'),
    ('#94a3b8', 'Other'),
]
legend_html = ' &nbsp;·&nbsp; '.join(
    f'<span style="color:{c}; font-weight:600;">■</span> {l}'
    for c, l in legend_items
)
st.markdown(f"""
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;
            padding:12px 20px; font-size:13px; color:#475569;">
  {legend_html}
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div class="alert-box" style="margin-top:16px;">
<p>
  <strong>Mining + Metals = R16.2B (56.5% of named sectors).</strong>
  These are capital-intensive industries with limited job creation per rand invested.
  South Africa already has deep mine unemployment — miners displaced by mechanisation
  are not being absorbed into new sectors funded by the IDC.
</p>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div class="info-box" style="margin-top:16px;">
<p>
  <strong>New Industries = R371M (1.3%).</strong>
  This includes biotech, solar energy, AI, and innovation-led sectors.
  These are the industries that could absorb educated youth.
  They receive the smallest allocation of any named sector.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 2: Fiscal year trend ────────────────────────────────────────────────
st.markdown("## IDC Investment Trend — FY2017 to FY2025")
st.markdown("*Total investment and deal volume over time, with key events annotated.*")

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=idc_fiscal['FY'],
    y=idc_fiscal['Invest_B'],
    name='Total Investment (R billions)',
    marker_color='#f0a500',
    opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Investment: R%{y:.2f}B<extra></extra>',
))
fig_trend.add_trace(go.Scatter(
    x=idc_fiscal['FY'],
    y=idc_fiscal['Deals'],
    name='Number of Deals',
    mode='lines+markers',
    line=dict(color='#00c9a7', width=3),
    marker=dict(size=9, color='#00c9a7', line=dict(color='white', width=2)),
    yaxis='y2',
    hovertemplate='<b>%{x}</b><br>Deals: %{y}<extra></extra>',
))

# Annotations
fig_trend.add_annotation(
    x='2020-21', y=1.94,
    text='COVID-19 trough<br>29 deals, R1.9B',
    showarrow=True, arrowhead=2, arrowcolor='#e05c5c',
    ax=0, ay=-60,
    font=dict(color='#e05c5c', size=10),
    bgcolor='#fef2f2', bordercolor='#e05c5c', borderwidth=1,
)
fig_trend.add_annotation(
    x='2022-23', y=17.01,
    text='FY2023-24 missing<br>from source data',
    showarrow=True, arrowhead=2, arrowcolor='#94a3b8',
    ax=60, ay=-40,
    font=dict(color='#64748b', size=10),
    bgcolor='#f8fafc', bordercolor='#e2e8f0', borderwidth=1,
)

fig_trend.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='Fiscal Year', gridcolor='#f1f5f9'),
    yaxis=dict(
        title='Total Investment (R billions)',
        title_font=dict(color='#f0a500'),
        tickfont=dict(color='#f0a500'),
        gridcolor='#f1f5f9',
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(t=40, b=20, l=20, r=20),
    height=400,
)
fig_trend.update_layout({
    'yaxis2': dict(
        title='Number of Deals',
        title_font=dict(color='#00c9a7'),
        tickfont=dict(color='#00c9a7'),
        overlaying='y',
        side='right',
        showgrid=False,
    )
})
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
<div class="info-box">
<p>
  <strong>COVID-19 impact is stark:</strong> FY2020-21 saw deals collapse from 150 to just 29,
  with investment falling 64.8% year-on-year. The recovery was strong — FY2021-22 saw
  a 396% investment rebound. However, <strong>FY2023-24 is entirely absent</strong> from
  the source dashboard — a data provenance gap that breaks trend continuity.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Accountability gap ─────────────────────────────────────────────────────────
st.markdown("## The Accountability Gap — IDC vs NEF")
st.markdown("*Same mandate. Very different transparency standards.*")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:24px;">
  <div style="font-size:16px; font-weight:700; color:#1e293b; margin-bottom:16px;">
    🏦 IDC — R65.9B deployed</div>
  <table style="width:100%; font-size:14px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Job creation data published</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">✗ None</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Cost per job metric</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">✗ None</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Provincial breakdown</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">✗ None</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Sector attribution (complete)</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">✗ 43.5% only</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:8px 0;">Missing fiscal year</td>
      <td style="color:#e05c5c; font-weight:700; text-align:right;">FY2023-24</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:24px;">
  <div style="font-size:16px; font-weight:700; color:#1e293b; margin-bottom:16px;">
    🏛️ NEF — R3.6B deployed (18× smaller)</div>
  <table style="width:100%; font-size:14px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Job creation data published</td>
      <td style="color:#00c9a7; font-weight:700; text-align:right;">✓ 31,654 jobs</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Cost per job metric</td>
      <td style="color:#00c9a7; font-weight:700; text-align:right;">✓ By province</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Provincial breakdown</td>
      <td style="color:#00c9a7; font-weight:700; text-align:right;">✓ All 9 provinces</td>
    </tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:8px 0;">Grants vs loans breakdown</td>
      <td style="color:#00c9a7; font-weight:700; text-align:right;">✓ Published</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:8px 0;">Data source</td>
      <td style="color:#64748b; font-weight:600; text-align:right;">Parliamentary Q</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="alert-box" style="margin-top:20px;">
<p>
  <strong>The most important finding in this analysis:</strong>
  The IDC deployed <strong>18.3× more public money</strong> than the NEF — R65.9B vs R3.6B —
  yet publishes <strong>zero job creation metrics</strong>. The NEF, despite being far smaller,
  tracks every job, every province, and every cost-per-job ratio.
  There is no technical barrier to the IDC doing the same.
  The absence of this data is a <strong>policy choice, not a limitation</strong>.
  South Africans deserve to know what R65.9B of public money created.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Data quality register ──────────────────────────────────────────────────────
st.markdown("## Data Quality & Discrepancy Register")
st.markdown("*Flagged issues identified during analysis. Relevant to both professional and journalistic audiences.*")

issues = [
    ("IDC Sector Coverage Gap", "56.5% of IDC investment (R37.3B) has no sector attribution in the public dashboard. Sector analysis covers only the named 43.5%.", "🟡"),
    ("IDC Fiscal Year Gap", "FY2023-24 is absent from the dataset. The 7-year trend skips a year, breaking continuity and preventing accurate compound growth analysis.", "🟡"),
    ("NEF Grants + Loans Discrepancy", "Grants (R194.8M) + Loans (R3,516.2M) = R3,710.9M — but total disbursed is R3,596.4M. Gap = R114.5M (3.2%). Likely: committed but not drawn-down facilities.", "🟡"),
    ("IDC Deal Count Discrepancy", "Key metrics state 852 companies; fiscal year deal sum = 854. A minor 2-deal gap, possibly due to rounding or restatement between reporting periods.", "🟢"),
    ("NEF Duplicate Entries", "KPML Group (Gauteng) and Bibi Cash & Carry (Free State) each appear twice in the top-10 job creators list with identical figures. Likely a data entry error in PQ705.", "🟡"),
    ("IDC: No Job Data", "R65.9B deployed with zero published job creation metrics. This is a public accountability failure, not a data quality issue.", "🔴"),
]

for icon, title, desc, severity in issues:
    severity_color = {'🔴': '#fef2f2', '🟡': '#fffbeb', '🟢': '#f0fdf4'}[severity]
    border_color   = {'🔴': '#e05c5c', '🟡': '#f0a500', '🟢': '#00c9a7'}[severity]
    st.markdown(f"""
<div style="background:{severity_color}; border-left:4px solid {border_color};
            border-radius:0 8px 8px 0; padding:14px 18px; margin-bottom:10px;">
  <div style="font-size:14px; font-weight:700; color:#1e293b; margin-bottom:4px;">
    {severity} {title}</div>
  <div style="font-size:13px; color:#475569;">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Source: IDC Funding Dashboard · NEF Parliamentary Question PQ705 (dtic.gov.za)
</div>
""", unsafe_allow_html=True)