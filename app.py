import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Who Really Gets the Money?",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global styles ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Base ── */
  [data-testid="stAppViewContainer"] { background: #fafafa; }
  [data-testid="stSidebar"]          { background: #f1f5f9; border-right: 1px solid #e2e8f0; }
  [data-testid="stSidebar"] * { color: #1e293b !important; }

  /* ── Typography ── */
  h1, h2, h3 { color: #1e293b; font-family: 'Georgia', serif; }
  p, li       { color: #334155; font-size: 15px; line-height: 1.75; }

  /* ── Callout boxes ── */
  .finding-box {
    background: #fffbeb;
    border-left: 5px solid #f0a500;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 18px 0;
  }
  .finding-box p { color: #1e293b; font-size: 15px; margin: 0; }
  .finding-box strong { color: #b45309; }

  .alert-box {
    background: #fef2f2;
    border-left: 5px solid #e05c5c;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 18px 0;
  }
  .alert-box p { color: #7f1d1d; font-size: 15px; margin: 0; }

  .info-box {
    background: #f0fdfa;
    border-left: 5px solid #00c9a7;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 18px 0;
  }
  .info-box p { color: #134e4a; font-size: 15px; margin: 0; }

  /* ── Metric cards ── */
  .metric-row { display: flex; gap: 16px; flex-wrap: wrap; margin: 24px 0; }
  .metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 20px 24px;
    flex: 1;
    min-width: 160px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .metric-card .metric-label { font-size: 12px; color: #64748b; text-transform: uppercase;
                               letter-spacing: 0.05em; margin-bottom: 6px; }
  .metric-card .metric-value { font-size: 28px; font-weight: 800; color: #1e293b; }
  .metric-card .metric-sub   { font-size: 12px; color: #94a3b8; margin-top: 4px; }
  .metric-card.gold  { border-top: 3px solid #f0a500; }
  .metric-card.teal  { border-top: 3px solid #00c9a7; }
  .metric-card.red   { border-top: 3px solid #e05c5c; }
  .metric-card.blue  { border-top: 3px solid #4e8df5; }
  .metric-card.purple{ border-top: 3px solid #a78bfa; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px;
    padding: 48px 40px;
    margin-bottom: 32px;
  }
  .hero h1 { color: #f0a500 !important; font-size: 2.4em; margin-bottom: 10px; }
  .hero p  { color: #cbd5e1 !important; font-size: 16px; line-height: 1.8; max-width: 780px; }
  .hero .sub { color: #94a3b8 !important; font-size: 13px; margin-top: 16px; }

  /* ── Section divider ── */
  .section-divider {
    border: none; border-top: 1px solid #e2e8f0; margin: 32px 0;
  }

  /* ── Data source badge ── */
  .source-badge {
    display: inline-block;
    background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 20px; padding: 4px 12px;
    font-size: 12px; color: #64748b; margin: 4px 4px 4px 0;
  }

  /* ── Hide default Streamlit branding ── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💰 Who Really Gets the Money?")
    st.markdown("---")
    st.markdown("""
**A public interest analysis of South African development finance.**

Navigate the sections using the pages below to explore how R69.5 billion
of public money was allocated — and whether it reached those who need it most.
    """)
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("""
- 🏦 IDC Dashboard (FY2017–2025)
- 🏛️ NEF via PQ705, dtic.gov.za
- 📊 Stats SA QLFS Q3 2025
    """)
    st.markdown("---")
    st.caption("Analysis by Lindiwe Dube · Built with Streamlit")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Who Really Gets the Money?</h1>
  <p>
    South Africa has one of the highest unemployment rates in the world.
    Nearly 1 in 3 working-age South Africans is officially unemployed —
    by the expanded measure, it is closer to 1 in 2. Among youth aged 15–24, it exceeds 60%.
    Into this crisis, the government deploys billions of rands through two development finance
    institutions — the IDC and NEF — with a constitutional mandate to create jobs and
    transform the economy.
  </p>
  <p style="margin-top:14px;">
    This analysis interrogates the public record. <strong style="color:#f0a500;">
    Is the money working — and is it reaching the people who need it most?</strong>
  </p>
  <p class="sub">
    Sources: IDC Funding Dashboard · NEF Parliamentary Question PQ705 (dtic.gov.za) ·
    Stats SA QLFS Q3 2025
  </p>
</div>
""", unsafe_allow_html=True)

# ── The scale of the crisis ────────────────────────────────────────────────────
st.markdown("## The Scale of the Crisis")
st.markdown("*Before examining where the money goes, consider the scale of the problem the DFIs exist to solve.*")

st.markdown("""
<div class="metric-row">
  <div class="metric-card red">
    <div class="metric-label">Official Unemployment</div>
    <div class="metric-value">31.9%</div>
    <div class="metric-sub">13.3M underutilised persons · Stats SA Q3 2025</div>
  </div>
  <div class="metric-card red">
    <div class="metric-label">Expanded Unemployment (LU3)</div>
    <div class="metric-value">42.4%</div>
    <div class="metric-sub">Includes discouraged work-seekers</div>
  </div>
  <div class="metric-card red">
    <div class="metric-label">Youth Unemployment (15–34)</div>
    <div class="metric-value">46.1%</div>
    <div class="metric-sub">~4.8 million young people</div>
  </div>
  <div class="metric-card red">
    <div class="metric-label">Youth Unemployment (15–24)</div>
    <div class="metric-value">~60%</div>
    <div class="metric-sub">Nearly 10× the global average</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── The DFI response ───────────────────────────────────────────────────────────
st.markdown("## The Government's Response: Development Finance")
st.markdown("*Two institutions. R69.5 billion. One mandate: jobs and transformation.*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px;
            padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.06); height:100%;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">
    🏦 Industrial Development Corporation (IDC)
  </div>
  <div style="font-size:32px; font-weight:800; color:#f0a500;">R65.9B</div>
  <div style="font-size:13px; color:#94a3b8; margin-bottom:16px;">Total investment · FY2017–2025</div>
  <table style="width:100%; font-size:13.5px; border-collapse:collapse;">
    <tr><td style="color:#64748b; padding:4px 0;">Deals funded</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">852</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Avg deal size</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">R77M</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Sectors covered</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">25+</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Countries reached</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">6</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Job data published?</td>
        <td style="color:#e05c5c; font-weight:700; text-align:right;">✗ No</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px;
            padding:24px; box-shadow:0 1px 4px rgba(0,0,0,0.06); height:100%;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">
    🏛️ National Empowerment Fund (NEF)
  </div>
  <div style="font-size:32px; font-weight:800; color:#00c9a7;">R3.6B</div>
  <div style="font-size:13px; color:#94a3b8; margin-bottom:16px;">Total disbursed · All provinces</div>
  <table style="width:100%; font-size:13.5px; border-collapse:collapse;">
    <tr><td style="color:#64748b; padding:4px 0;">Companies funded</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">392</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Avg deal size</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">R9.2M</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Jobs supported</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">31,654</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Avg cost per job</td>
        <td style="color:#1e293b; font-weight:600; text-align:right;">R113,616</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">Job data published?</td>
        <td style="color:#00c9a7; font-weight:700; text-align:right;">✓ Yes</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Six key findings ───────────────────────────────────────────────────────────
st.markdown("## Six Key Findings")
st.markdown("*Use the sidebar to explore each finding in detail.*")

findings = [
    ("📍", "Geographic Concentration is Real",
     "Gauteng and KwaZulu-Natal received 55.9% of NEF disbursements and 65.6% of all deals — from just 2 of 9 provinces.",
     "gold"),
    ("📊", "Deal Size Inequality Mirrors Income Inequality",
     "0.5% of deals absorb 17% of all money. The bottom 12% of deals share just 0.7% of funding. Gini = 0.56.",
     "gold"),
    ("⚠️", "Biggest Recipients Are Not the Best Job Creators",
     "Zero overlap between top-10 disbursements and top-10 job creators. A 5,366× efficiency gap exists within the same programme.",
     "red"),
    ("🔍", "R65.9B Deployed With No Job Accountability Metrics",
     "The IDC publishes no cost-per-job data. The NEF — 18× smaller — tracks every job. This is the single most important accountability gap.",
     "red"),
    ("⛏️", "Mining Dominates IDC Sector Funding",
     "Mining and metals account for 56.5% of named-sector IDC investment — entrenching rather than diversifying SA's historical economic structure.",
     "gold"),
    ("🔎", "Multiple Data Quality Gaps Limit Full Accountability",
     "FY2023-24 missing from IDC data. 56.5% of IDC investment has no sector attribution. Duplicate entries in NEF's top-10 job creators.",
     "teal"),
]

for i in range(0, len(findings), 2):
    cols = st.columns(2)
    for j, col in enumerate(cols):
        if i + j < len(findings):
            icon, title, desc, colour = findings[i + j]
            border_color = {"gold": "#f0a500", "red": "#e05c5c", "teal": "#00c9a7"}[colour]
            with col:
                st.markdown(f"""
<div style="background:white; border:1px solid #e2e8f0; border-top:3px solid {border_color};
            border-radius:10px; padding:20px 22px; margin-bottom:16px;
            box-shadow:0 1px 4px rgba(0,0,0,0.06);">
  <div style="font-size:22px; margin-bottom:8px;">{icon}</div>
  <div style="font-size:14px; font-weight:700; color:#1e293b; margin-bottom:6px;">{title}</div>
  <div style="font-size:13px; color:#475569; line-height:1.6;">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:13px;">
  Data: IDC Funding Dashboard · NEF PQ705 (dtic.gov.za) · Stats SA QLFS Q3 2025<br>
  Dataset compiled by <a href="https://x.com/AfikaSoyamba" target="_blank" 
  style="color:#64748b;">@AfikaSoyamba</a> ·
  Analysis: Lindiwe Songewla · Built with Streamlit & Plotly · For public interest use
</div>
""", unsafe_allow_html=True)