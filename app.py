import streamlit as st
 
st.set_page_config(
    page_title="Who Really Gets the Money?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ── Shared design system ────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&display=swap');
 
/* ── Reset & base ── */
[data-testid="stAppViewContainer"] { background: #FAFAF8; }
[data-testid="stSidebar"] { background: #F1EFE8; border-right: 0.5px solid #D3D1C7; }
[data-testid="stSidebar"] * { color: #2C2C2A !important; }
[data-testid="stSidebar"] .stMarkdown p { font-family: 'Source Serif 4', Georgia, serif; font-size: 13px; color: #5F5E5A !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 860px; }
 
/* ── Typography ── */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif; color: #111110; }
p, li { font-family: 'Source Serif 4', Georgia, serif; color: #2C2C2A; font-size: 15px; line-height: 1.75; }
 
/* ── Masthead ── */
.masthead { border-bottom: 3px solid #111110; padding-bottom: 16px; margin-bottom: 0; }
.masthead-label { font-family: 'Source Serif 4', serif; font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 10px; }
.masthead-title { font-family: 'Playfair Display', Georgia, serif; font-size: 52px; font-weight: 900; line-height: 1.0; color: #111110; letter-spacing: -0.02em; }
.masthead-title em { font-style: italic; color: #BA7517; }
.masthead-deck { font-family: 'Source Serif 4', serif; font-size: 17px; font-weight: 300; line-height: 1.7; color: #444441; margin-top: 14px; max-width: 680px; border-left: 3px solid #BA7517; padding-left: 16px; }
.byline-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-top: 0.5px solid #B4B2A9; border-bottom: 0.5px solid #B4B2A9; margin-top: 18px; }
.byline { font-size: 12px; color: #5F5E5A; letter-spacing: 0.04em; font-style: italic; }
.byline strong { font-style: normal; font-weight: 600; color: #2C2C2A; }
.app-link { font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: #BA7517; text-decoration: none; font-style: normal; font-family: 'Source Serif 4', serif; font-weight: 600; border-bottom: 1px solid #BA7517; padding-bottom: 1px; }
 
/* ── Page masthead (inner pages) ── */
.page-masthead { border-bottom: 2px solid #111110; padding-bottom: 14px; margin-bottom: 28px; }
.page-section-label { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #888780; margin-bottom: 8px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 900; line-height: 1.1; color: #111110; letter-spacing: -0.01em; }
.page-title em { font-style: italic; color: #BA7517; }
.page-deck { font-family: 'Source Serif 4', serif; font-size: 15px; font-weight: 300; line-height: 1.7; color: #444441; margin-top: 10px; border-left: 3px solid #BA7517; padding-left: 14px; max-width: 640px; }
 
/* ── Section rules ── */
.section-rule { display: flex; align-items: baseline; gap: 14px; margin: 28px 0 18px 0; }
.section-label { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #888780; white-space: nowrap; }
.section-line { flex: 1; height: 0.5px; background: #D3D1C7; }
 
/* ── Stat strip ── */
.stat-strip { display: grid; grid-template-columns: repeat(4, 1fr); border: 0.5px solid #D3D1C7; border-right: none; margin-bottom: 28px; }
.stat-cell { padding: 16px 14px; border-right: 0.5px solid #D3D1C7; }
.stat-cell.alert { border-top: 2px solid #E24B4A; }
.stat-cell.warn  { border-top: 2px solid #BA7517; }
.stat-cell.ok    { border-top: 2px solid #0F6E56; }
.stat-cell.info  { border-top: 2px solid #185FA5; }
.stat-number { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #111110; line-height: 1; margin-bottom: 4px; }
.stat-number.red    { color: #A32D2D; }
.stat-number.amber  { color: #BA7517; }
.stat-number.teal   { color: #0F6E56; }
.stat-number.blue   { color: #185FA5; }
.stat-desc { font-size: 11px; color: #5F5E5A; line-height: 1.5; }
 
/* ── Two-col grid (DFI cards) ── */
.two-col-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 0.5px solid #D3D1C7; margin-bottom: 28px; }
.grid-card { padding: 20px; border-right: 0.5px solid #D3D1C7; }
.grid-card:last-child { border-right: none; }
.grid-card-label { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 8px; }
.grid-card-amount { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 700; line-height: 1; margin-bottom: 2px; }
.grid-card-amount.amber { color: #BA7517; }
.grid-card-amount.teal  { color: #0F6E56; }
.grid-card-period { font-size: 11px; color: #888780; margin-bottom: 14px; }
.grid-table { width: 100%; border-collapse: collapse; }
.grid-table tr { border-top: 0.5px solid #F1EFE8; }
.grid-table td { font-size: 12px; padding: 5px 0; color: #5F5E5A; }
.grid-table td:last-child { text-align: right; font-weight: 600; color: #2C2C2A; }
.grid-table .no  { color: #A32D2D !important; }
.grid-table .yes { color: #0F6E56 !important; }
 
/* ── Findings grid ── */
.findings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; margin-bottom: 28px; }
.finding-item { padding: 18px; border: 0.5px solid #D3D1C7; margin: -0.5px 0 0 -0.5px; }
.finding-number { font-family: 'Playfair Display', serif; font-size: 11px; font-weight: 700; color: #D3D1C7; letter-spacing: 0.1em; margin-bottom: 6px; }
.finding-title { font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 700; color: #111110; line-height: 1.35; margin-bottom: 6px; }
.finding-title.critical { color: #A32D2D; }
.finding-desc { font-size: 12px; color: #5F5E5A; line-height: 1.6; }
.finding-stat { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #BA7517; margin-top: 8px; }
 
/* ── Callout boxes ── */
.callout { padding: 14px 18px; margin: 18px 0; border-left: 3px solid #BA7517; background: #FAEEDA; }
.callout p { font-size: 14px; color: #633806; line-height: 1.65; margin: 0; }
.callout.critical { border-left-color: #E24B4A; background: #FCEBEB; }
.callout.critical p { color: #791F1F; }
.callout.ok { border-left-color: #0F6E56; background: #E1F5EE; }
.callout.ok p { color: #085041; }
.callout.info { border-left-color: #185FA5; background: #E6F1FB; }
.callout.info p { color: #0C447C; }
 
/* ── Data note ── */
.data-note { font-size: 11px; color: #888780; border-top: 0.5px solid #D3D1C7; padding-top: 10px; margin-top: 20px; line-height: 1.6; }
 
/* ── Nav strip ── */
.nav-strip { background: #444441; padding: 14px 20px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 28px; }
.nav-label { font-size: 10px; color: #B4B2A9; letter-spacing: 0.15em; text-transform: uppercase; margin-right: 8px; font-family: 'Source Serif 4', serif; }
.nav-item { font-size: 11px; color: #111110; background: #FAFAF8; font-family: 'Source Serif 4', serif; font-weight: 600; letter-spacing: 0.04em; padding: 4px 10px; }
 
/* ── Acknowledgement ── */
.ack-note { background: #FAEEDA; border-left: 3px solid #BA7517; padding: 12px 16px; margin-top: 20px; font-size: 12px; color: #633806; line-height: 1.6; }
 
/* ── Footer ── */
.footer-strip { border-top: 0.5px solid #D3D1C7; padding-top: 16px; margin-top: 28px; font-size: 11px; color: #888780; line-height: 1.7; }
.footer-strip a { color: #BA7517; }
</style>
"""
 
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
 
# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("""
A public interest analysis of South African development finance institutions — the IDC and NEF —
and whether R69.5 billion of public money is reaching those who need it most.
    """)
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("""
- IDC Funding Dashboard (FY2017–2025)
- NEF via PQ705, dtic.gov.za
- Stats SA QLFS Q3 2025
    """)
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")
 
# ── Landing page ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-label">Public Interest Data Analysis &nbsp;·&nbsp; South African Development Finance</div>
  <div class="masthead-title">Who Really<br>Gets the <em>Money?</em></div>
  <div class="masthead-deck">
    South Africa deploys billions through development finance institutions mandated to create jobs
    and build an inclusive economy. This analysis interrogates the public record — and asks whether
    the money is working.
  </div>
  <div class="byline-row">
    <div class="byline">By <strong>Lindiwe Songelwa</strong> &nbsp;·&nbsp; IDC Dashboard · NEF PQ705 · Stats SA QLFS Q3 2025 &nbsp;·&nbsp; 2025</div>
    <a class="app-link" href="https://sa-idc-inequality.streamlit.app" target="_blank">Explore the data &rarr;</a>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ── Crisis context ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-rule">
  <span class="section-label">The crisis the DFIs exist to solve</span>
  <div class="section-line"></div>
</div>
<div class="stat-strip">
  <div class="stat-cell alert">
    <div class="stat-number red">31.9%</div>
    <div class="stat-desc">Official unemployment. 13.3M underutilised persons.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">42.4%</div>
    <div class="stat-desc">Expanded unemployment. Includes discouraged seekers.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">46.1%</div>
    <div class="stat-desc">Youth unemployment. 15–34 age group.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">~60%</div>
    <div class="stat-desc">Youth aged 15–24. Nearly 10× the global average.</div>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ── DFI response ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-rule">
  <span class="section-label">The government's response</span>
  <div class="section-line"></div>
</div>
<div class="two-col-grid">
  <div class="grid-card">
    <div class="grid-card-label">Industrial Development Corporation (IDC)</div>
    <div class="grid-card-amount amber">R65.9B</div>
    <div class="grid-card-period">Total investment · FY2017–2025</div>
    <table class="grid-table">
      <tr><td>Deals funded</td><td>852</td></tr>
      <tr><td>Average deal size</td><td>R77M</td></tr>
      <tr><td>Sectors covered</td><td>25+</td></tr>
      <tr><td>Job data published?</td><td class="no">No</td></tr>
    </table>
  </div>
  <div class="grid-card">
    <div class="grid-card-label">National Empowerment Fund (NEF)</div>
    <div class="grid-card-amount teal">R3.6B</div>
    <div class="grid-card-period">Total disbursed · All 9 provinces</div>
    <table class="grid-table">
      <tr><td>Companies funded</td><td>392</td></tr>
      <tr><td>Average deal size</td><td>R9.2M</td></tr>
      <tr><td>Jobs supported</td><td>31,654</td></tr>
      <tr><td>Job data published?</td><td class="yes">Yes</td></tr>
    </table>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ── Six findings ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-rule">
  <span class="section-label">Six key findings</span>
  <div class="section-line"></div>
</div>
<div class="findings-grid">
  <div class="finding-item">
    <div class="finding-number">01</div>
    <div class="finding-title">Geographic concentration is real and measurable</div>
    <div class="finding-desc">Gauteng and KZN received 55.9% of NEF disbursements from just 2 of 9 provinces.</div>
    <div class="finding-stat">Gini 0.469</div>
  </div>
  <div class="finding-item">
    <div class="finding-number">02</div>
    <div class="finding-title">Deal size inequality mirrors income inequality</div>
    <div class="finding-desc">The top 0.5% of deals absorb 17% of all money. The bottom 12% share just 0.7%.</div>
    <div class="finding-stat">Gini 0.56</div>
  </div>
  <div class="finding-item">
    <div class="finding-number">03</div>
    <div class="finding-title critical">Biggest recipients are not the best job creators</div>
    <div class="finding-desc">Zero overlap between top-10 disbursements and top-10 job creators. R20.5M per job vs R3,827 per job within the same programme.</div>
    <div class="finding-stat">5,366&times; gap</div>
  </div>
  <div class="finding-item">
    <div class="finding-number">04</div>
    <div class="finding-title critical">R65.9B deployed with no job accountability metrics</div>
    <div class="finding-desc">The IDC publishes no cost-per-job data. The NEF — 18× smaller — tracks every job. The absence is a policy choice.</div>
    <div class="finding-stat">0 metrics</div>
  </div>
  <div class="finding-item">
    <div class="finding-number">05</div>
    <div class="finding-title">Mining dominates IDC sector funding</div>
    <div class="finding-desc">56.5% of named-sector IDC investment goes to mining and metals. New industries received just 1.3%.</div>
    <div class="finding-stat">R16.2B</div>
  </div>
  <div class="finding-item">
    <div class="finding-number">06</div>
    <div class="finding-title">Data quality gaps limit full accountability</div>
    <div class="finding-desc">FY2023–24 absent from IDC data. 56.5% of investment has no sector attribution. Duplicate entries in NEF records.</div>
    <div class="finding-stat">Multiple gaps</div>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ── Nav strip ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-strip">
  <span class="nav-label">Explore</span>
  <span class="nav-item">1. Crisis Context</span>
  <span class="nav-item">2. Geographic Inequality</span>
  <span class="nav-item">3. Deal Size</span>
  <span class="nav-item">4. Job Efficiency</span>
  <span class="nav-item">5. Sector Concentration</span>
  <span class="nav-item">6. ROI Predictor</span>
  <span class="nav-item">7. Anomaly Detection</span>
</div>
""", unsafe_allow_html=True)
 
# ── Acknowledgement ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="ack-note">
  The underlying dataset was compiled by <strong>@AfikaSoyamba</strong> — a database of 1,248
  South African businesses funded by the IDC and NEF, including every company name, amount, and
  province. This analysis would not exist without that work.
</div>
<div class="footer-strip">
  Data: IDC Funding Dashboard &nbsp;·&nbsp; NEF Parliamentary Question PQ705 (dtic.gov.za)
  &nbsp;·&nbsp; Stats Sa QLFS Q3 2025<br>
  Analysis &amp; code &copy; 2025 Lindiwe Songelwa &nbsp;·&nbsp; Open source
  &nbsp;·&nbsp; Built with Python, Streamlit &amp; Plotly
</div>
""", unsafe_allow_html=True)
