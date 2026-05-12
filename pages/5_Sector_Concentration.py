import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Sector Concentration", page_icon="⛏️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

st.markdown(page_masthead(
    "Section 5 of 5 &nbsp;·&nbsp; Sector Concentration",
    "The IDC Is Reinforcing<br>the Past, Not <em>Building the Future</em>",
    "Mining and metals account for 56.5% of named-sector IDC investment. "
    "New industries — biotech, solar, AI — received 1.3%. "
    "South Africa's economy was built on extractive industries. "
    "By this measure, the IDC is entrenching that structure."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Key finding:</strong> Among the 12 named sectors in the IDC dataset, "
    "<strong>Mining and Metals alone accounts for 56.5%</strong> of all attributed investment — "
    "R16.2 billion. New Industries — the IDC's forward-looking diversification mandate "
    "(biotech, solar, AI) — received just <strong>1.3%</strong> of named-sector funding. "
    "South Africa's economy was built on mining. The IDC, at least by this measure, "
    "is reinforcing that structure rather than transforming it."
), unsafe_allow_html=True)

# ── Original hardcoded data ────────────────────────────────────────────────────
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
    'Mining/Metals': '#A32D2D',
    'Manufacturing': '#BA7517',
    'Agriculture':   '#0F6E56',
    'Chemicals':     '#5B4A9E',
    'Infrastructure':'#185FA5',
    'Other':         '#888780',
    'New Industries':'#2E9C6B',
}
bar_colors = [cat_colors[c] for c in idc_sectors['Category']]

# ── Chart 1: Sector investment ─────────────────────────────────────────────────
st.markdown(section_rule("IDC investment by sector (named sectors — R28.7B of R65.9B total)"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">56.5% of total IDC investment has no sector attribution — a significant transparency gap.</div>', unsafe_allow_html=True)

fig_sectors = go.Figure()
fig_sectors.add_trace(go.Bar(
    y=idc_sectors['Sector'],
    x=idc_sectors['Investment_B'],
    orientation='h',
    marker_color=bar_colors,
    text=[f"R{v:.2f}B" for v in idc_sectors['Investment_B']],
    textposition='outside',
    textfont=dict(size=11, family='Source Serif 4, Georgia, serif'),
    customdata=idc_sectors['Category'],
    hovertemplate=(
        '<b>%{y}</b><br>'
        'Investment: R%{x:.2f}B<br>'
        'Category: %{customdata}<extra></extra>'
    ),
))
mean_val = idc_sectors['Investment_B'].mean()
fig_sectors.add_vline(
    x=mean_val, line_dash='dash', line_color='#B4B2A9', line_width=1.5,
    annotation_text=f'Mean: R{mean_val:.2f}B',
    annotation_position='top',
    annotation_font=dict(color='#888780', size=11, family='Source Serif 4, Georgia, serif'),
)
fig_sectors = apply_plotly_theme(fig_sectors, height=440)
fig_sectors.update_layout(
    xaxis=dict(title='Total Investment (R billions, FY2017–2025)', gridcolor='#EDECEA'),
    yaxis=dict(title=''),
    margin=dict(t=30, b=24, l=20, r=80),
    showlegend=False,
)
st.plotly_chart(fig_sectors, use_container_width=True)

legend_items = [
    ('#A32D2D', 'Mining / Metals'),
    ('#BA7517', 'Manufacturing'),
    ('#0F6E56', 'Agriculture'),
    ('#5B4A9E', 'Chemicals'),
    ('#185FA5', 'Infrastructure'),
    ('#2E9C6B', 'New Industries'),
    ('#888780', 'Other'),
]
legend_html = ' &nbsp;·&nbsp; '.join(
    f'<span style="color:{c}; font-weight:700;">■</span> <span style="color:#5F5E5A;">{l}</span>'
    for c, l in legend_items
)
st.markdown(f'<div style="background:#F1EFE8; border:0.5px solid #D3D1C7; padding:11px 18px; font-size:12px; font-family:\'Source Serif 4\',Georgia,serif;">{legend_html}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(callout(
        "<strong>Mining + Metals = R16.2B (56.5% of named sectors).</strong> "
        "These are capital-intensive industries with limited job creation per rand invested. "
        "Miners displaced by mechanisation are not being absorbed into new sectors "
        "funded by the IDC.",
        "alert"
    ), unsafe_allow_html=True)
with col2:
    st.markdown(callout(
        "<strong>New Industries = R371M (1.3%).</strong> "
        "This includes biotech, solar energy, AI, and innovation-led sectors — "
        "the industries that could absorb educated youth. "
        "They receive the smallest allocation of any named sector.",
        "info"
    ), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 2: Fiscal year trend ─────────────────────────────────────────────────
st.markdown(section_rule("IDC investment trend — FY2017 to FY2025"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Total investment and deal volume over time, with key events annotated.</div>', unsafe_allow_html=True)

fig_trend = go.Figure()
fig_trend.add_trace(go.Bar(
    x=idc_fiscal['FY'],
    y=idc_fiscal['Invest_B'],
    name='Total Investment (R billions)',
    marker_color='#BA7517',
    opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Investment: R%{y:.2f}B<extra></extra>',
))
fig_trend.add_trace(go.Scatter(
    x=idc_fiscal['FY'],
    y=idc_fiscal['Deals'],
    name='Number of Deals',
    mode='lines+markers',
    line=dict(color='#0F6E56', width=2.5),
    marker=dict(size=8, color='#0F6E56', line=dict(color='#FAFAF8', width=2)),
    yaxis='y2',
    hovertemplate='<b>%{x}</b><br>Deals: %{y}<extra></extra>',
))
fig_trend.add_annotation(
    x='2020-21', y=1.94,
    text='COVID-19 trough<br>29 deals, R1.9B',
    showarrow=True, arrowhead=2, arrowcolor='#C53030',
    ax=0, ay=-60,
    font=dict(color='#C53030', size=10, family='Source Serif 4, Georgia, serif'),
    bgcolor='#FDF0F0', bordercolor='#C53030', borderwidth=1,
)
fig_trend.add_annotation(
    x='2022-23', y=17.01,
    text='FY2023-24 missing<br>from source data',
    showarrow=True, arrowhead=2, arrowcolor='#888780',
    ax=60, ay=-40,
    font=dict(color='#888780', size=10, family='Source Serif 4, Georgia, serif'),
    bgcolor='#F1EFE8', bordercolor='#D3D1C7', borderwidth=1,
)
fig_trend = apply_plotly_theme(fig_trend, height=400)
fig_trend.update_layout(
    xaxis=dict(title='Fiscal Year', gridcolor='#EDECEA'),
    yaxis=dict(
        title='Total Investment (R billions)',
        title_font=dict(color='#BA7517'),
        tickfont=dict(color='#BA7517'),
        gridcolor='#EDECEA',
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=11, family='Source Serif 4, Georgia, serif')),
    margin=dict(t=40, b=24, l=20, r=20),
)
fig_trend.update_layout({
    'yaxis2': dict(
        title='Number of Deals',
        title_font=dict(color='#0F6E56'),
        tickfont=dict(color='#0F6E56'),
        overlaying='y',
        side='right',
        showgrid=False,
    )
})
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown(callout(
    "<strong>COVID-19 impact is stark:</strong> FY2020-21 saw deals collapse from 150 to just 29, "
    "with investment falling 64.8% year-on-year. The recovery was strong — FY2021-22 saw "
    "a 396% investment rebound. However, <strong>FY2023-24 is entirely absent</strong> from "
    "the source dashboard — a data provenance gap that breaks trend continuity.",
    "info"
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Accountability gap ─────────────────────────────────────────────────────────
st.markdown(section_rule("The accountability gap — IDC vs NEF"), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #C53030; padding:24px;">
  <div style="font-family:'Playfair Display',serif; font-size:16px; font-weight:700; color:#111110; margin-bottom:16px;">IDC — R65.9B deployed</div>
  <table class="info-card-table">
    <tr><td>Job creation data published</td><td class="no">None</td></tr>
    <tr><td>Cost per job metric</td><td class="no">None</td></tr>
    <tr><td>Provincial breakdown</td><td class="no">None</td></tr>
    <tr><td>Sector attribution (complete)</td><td class="no">43.5% only</td></tr>
    <tr><td>Missing fiscal year</td><td class="no">FY2023-24</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #0F6E56; padding:24px;">
  <div style="font-family:'Playfair Display',serif; font-size:16px; font-weight:700; color:#111110; margin-bottom:16px;">NEF — R3.6B deployed (18× smaller)</div>
  <table class="info-card-table">
    <tr><td>Job creation data published</td><td class="yes">31,654 jobs</td></tr>
    <tr><td>Cost per job metric</td><td class="yes">By province</td></tr>
    <tr><td>Provincial breakdown</td><td class="yes">All 9 provinces</td></tr>
    <tr><td>Grants vs loans breakdown</td><td class="yes">Published</td></tr>
    <tr><td>Data source</td><td>Parliamentary Q</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "<strong>The most important finding in this analysis:</strong> "
    "The IDC deployed <strong>18.3× more public money</strong> than the NEF — R65.9B vs R3.6B — "
    "yet publishes <strong>zero job creation metrics</strong>. The NEF, despite being far smaller, "
    "tracks every job, every province, and every cost-per-job ratio. "
    "There is no technical barrier to the IDC doing the same. "
    "The absence of this data is a <strong>policy choice, not a limitation</strong>. "
    "South Africans deserve to know what R65.9B of public money created.",
    "alert"
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Data quality register ──────────────────────────────────────────────────────
st.markdown(section_rule("Data quality & discrepancy register"), unsafe_allow_html=True)

issues = [
    ("IDC: No Job Data", "R65.9B deployed with zero published job creation metrics. This is a public accountability failure, not a data quality issue.", "red"),
    ("IDC Sector Coverage Gap", "56.5% of IDC investment (R37.3B) has no sector attribution in the public dashboard. Sector analysis covers only the named 43.5%.", "warn"),
    ("IDC Fiscal Year Gap", "FY2023-24 is absent from the dataset. The 7-year trend skips a year, breaking continuity and preventing accurate compound growth analysis.", "warn"),
    ("NEF Grants + Loans Discrepancy", "Grants (R194.8M) + Loans (R3,516.2M) = R3,710.9M — but total disbursed is R3,596.4M. Gap = R114.5M (3.2%). Likely: committed but not drawn-down facilities.", "warn"),
    ("IDC Deal Count Discrepancy", "Key metrics state 852 companies; fiscal year deal sum = 854. A minor 2-deal gap, possibly due to rounding or restatement.", "ok"),
    ("NEF Duplicate Entries", "KPML Group and Bibi Cash & Carry each appear twice in the top-10 job creators list with identical figures. Likely a data entry error in PQ705.", "warn"),
]

color_map = {
    "red":  ("#FDF0F0", "#C53030", "#7A1F1F"),
    "warn": ("#FDF6E8", "#BA7517", "#5C3A06"),
    "ok":   ("#E8F5EF", "#0F6E56", "#084D3A"),
}

for title, desc, level in issues:
    bg, border, text = color_map[level]
    st.markdown(f"""
<div style="background:{bg}; border-left:3px solid {border}; padding:14px 18px; margin-bottom:10px;">
  <div style="font-family:'Playfair Display',serif; font-size:14px; font-weight:700; color:{text}; margin-bottom:4px;">{title}</div>
  <div style="font-size:13px; color:#5F5E5A; line-height:1.6; font-family:'Source Serif 4',Georgia,serif;">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
