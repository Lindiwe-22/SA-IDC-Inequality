import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Crisis Context", page_icon="📉", layout="wide")

# ── Shared styles ──────────────────────────────────────────────────────────────
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

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📉 The Crisis Context")
st.markdown("### Unemployment as the moral benchmark for every rand spent")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box">
<p>
  <strong>Why this matters:</strong> Development finance institutions exist to solve unemployment.
  Every cost-per-job figure, every provincial allocation, and every sector decision in this analysis
  must be read against one number — <strong>31.9%</strong>. That is the share of South Africans
  who want to work and cannot find work. By the expanded definition, it is 42.4%.
  Among youth aged 15–24, it exceeds 60%.
</p>
</div>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
unemployment = pd.DataFrame({
    'Category': [
        'Official Unemployment',
        'Expanded Unemployment (LU3)',
        'Youth Unemployment (15–34)',
        'Youth Unemployment (15–24)',
    ],
    'Rate': [31.9, 42.4, 46.1, 60.0],
    'Color': ['#e05c5c', '#e05c5c', '#c0392b', '#a31515'],
})

global_comparisons = pd.DataFrame({
    'Country': ['South Africa', 'Nigeria', 'Kenya', 'Brazil', 'India', 'USA', 'Germany', 'Global Avg'],
    'Rate':    [31.9, 5.3, 5.7, 7.8, 8.0, 3.7, 3.0, 6.5],
    'Color':   ['#e05c5c','#f0a500','#f0a500','#4e8df5','#4e8df5','#00c9a7','#00c9a7','#94a3b8'],
})

# ── Chart 1: SA unemployment breakdown ────────────────────────────────────────
st.markdown("## South Africa's Unemployment — Four Measures")

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=unemployment['Category'],
    y=unemployment['Rate'],
    marker_color=unemployment['Color'],
    text=[f"{v}%" for v in unemployment['Rate']],
    textposition='outside',
    textfont=dict(size=14, color='#1e293b'),
    hovertemplate='<b>%{x}</b><br>Rate: %{y}%<extra></extra>',
))
fig1.add_hline(
    y=6.5, line_dash='dash', line_color='#94a3b8', line_width=1.5,
    annotation_text='Global average ~6.5%',
    annotation_position='top right',
    annotation_font=dict(color='#64748b', size=12),
)
fig1.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    yaxis=dict(
        title='Unemployment Rate (%)', range=[0, 75],
        gridcolor='#f1f5f9', ticksuffix='%',
    ),
    xaxis=dict(title='', tickfont=dict(size=13)),
    margin=dict(t=20, b=20, l=20, r=20),
    height=400,
    showlegend=False,
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>Finding:</strong> South Africa's official unemployment rate is nearly
  <strong>5× the global average</strong>. For youth aged 15–24, it is nearly
  <strong>10× the global benchmark</strong>. These are not temporary fluctuations —
  Stats SA has recorded unemployment above 25% consistently since 2008.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 2: Global comparison ────────────────────────────────────────────────
st.markdown("## Global Comparison — SA vs Peer Economies")
st.markdown("*South Africa's unemployment rate is not just high by African standards — it is exceptional globally.*")

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=global_comparisons['Country'],
    y=global_comparisons['Rate'],
    marker_color=global_comparisons['Color'],
    text=[f"{v}%" for v in global_comparisons['Rate']],
    textposition='outside',
    textfont=dict(size=13, color='#1e293b'),
    hovertemplate='<b>%{x}</b><br>Unemployment: %{y}%<extra></extra>',
))
fig2.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    yaxis=dict(
        title='Unemployment Rate (%)', range=[0, 40],
        gridcolor='#f1f5f9', ticksuffix='%',
    ),
    xaxis=dict(title='', tickfont=dict(size=13)),
    margin=dict(t=20, b=20, l=20, r=20),
    height=380,
    showlegend=False,
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── DFI mandate explainer ──────────────────────────────────────────────────────
st.markdown("## The DFI Mandate")
st.markdown("*Into this crisis, the government deploys development finance as its primary economic intervention.*")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px;
            padding:22px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:10px;">What DFIs are supposed to do</div>
  <ul style="color:#334155; font-size:14px; line-height:2; padding-left:18px;">
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
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px;
            padding:22px; box-shadow:0 1px 4px rgba(0,0,0,0.05);">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:10px;">The benchmark question</div>
  <p style="color:#334155; font-size:14px; line-height:1.8;">
    If the IDC and NEF together deployed <strong>R69.5 billion</strong> of public money
    over the period examined, and South Africa still has <strong>13.3 million
    underutilised workers</strong> — what is the cost per job created?
    And more importantly: <strong>who received the money, and did it reach
    those who need it most?</strong>
  </p>
  <p style="color:#94a3b8; font-size:12px; margin-top:12px;">
    Use the sidebar to explore the evidence across four analytical lenses →
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Key stats row ──────────────────────────────────────────────────────────────
st.markdown("## At a Glance — The Numbers Behind the Crisis")

cols = st.columns(4)
stats = [
    ("13.3M", "Underutilised persons in SA labour market", "#e05c5c"),
    ("R69.5B", "Total IDC + NEF funding in this dataset", "#f0a500"),
    ("31,654", "Jobs the NEF claims to have supported", "#00c9a7"),
    ("0", "Jobs the IDC has publicly reported creating", "#e05c5c"),
]
for col, (val, label, color) in zip(cols, stats):
    with col:
        st.markdown(f"""
<div style="background:white; border-top:3px solid {color}; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; text-align:center;
            box-shadow:0 1px 4px rgba(0,0,0,0.05);">
  <div style="font-size:28px; font-weight:800; color:#1e293b;">{val}</div>
  <div style="font-size:12px; color:#64748b; margin-top:6px; line-height:1.5;">{label}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Sources: Stats SA QLFS Q3 2025 · IDC Dashboard · NEF PQ705
  Dataset compiled by <a href="https://x.com/AfikaSoyamba" target="_blank" 
  style="color:#64748b;">@AfikaSoyamba</a> ·
</div>
""", unsafe_allow_html=True)