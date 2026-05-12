import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, sidebar_content

st.set_page_config(
    page_title="Who Really Gets the Money?",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": "Who Really Gets the Money? — A public interest analysis of South African development finance by Lindiwe Songelwa."
    }
)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-label">Public Interest Data Analysis &nbsp;·&nbsp; South African Development Finance</div>
  <div class="masthead-title">Who Really<br>Gets the <em>Money?</em></div>
  <div class="masthead-deck">
    South Africa has one of the highest unemployment rates in the world.
    Nearly 1 in 3 working-age South Africans is officially unemployed —
    by the expanded measure, closer to 1 in 2. Into this crisis, the government deploys
    billions of rands through two institutions with a constitutional mandate to create jobs.
    This analysis asks whether the money is working.
  </div>
  <div class="byline-row">
    <div class="byline">
      By <strong>Lindiwe Songelwa</strong> &nbsp;·&nbsp;
      IDC Dashboard · NEF PQ705 · Stats SA QLFS Q3 2025 &nbsp;·&nbsp; 2026
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Crisis numbers ─────────────────────────────────────────────────────────────
st.markdown(section_rule("The crisis the DFIs exist to solve"), unsafe_allow_html=True)
st.markdown("""
<div class="stat-strip stat-strip-4">
  <div class="stat-cell alert">
    <div class="stat-number red">31.9%</div>
    <div class="stat-desc">Official unemployment. 13.3M underutilised persons.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">42.4%</div>
    <div class="stat-desc">Expanded unemployment. Includes discouraged work-seekers.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">46.1%</div>
    <div class="stat-desc">Youth unemployment, 15–34. Approximately 4.8 million people.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">~60%</div>
    <div class="stat-desc">Youth aged 15–24. Nearly 10× the global average.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── DFI response ───────────────────────────────────────────────────────────────
st.markdown(section_rule("The government's response"), unsafe_allow_html=True)
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="info-card-label">Industrial Development Corporation (IDC)</div>
    <div class="info-card-value amber">R65.9B</div>
    <div class="info-card-sub">Total investment · FY2017–2025</div>
    <table class="info-card-table">
      <tr><td>Deals funded</td><td>852</td></tr>
      <tr><td>Average deal size</td><td>R77M</td></tr>
      <tr><td>Sectors covered</td><td>25+</td></tr>
      <tr><td>Countries reached</td><td>6</td></tr>
      <tr><td>Job data published?</td><td class="no">No</td></tr>
    </table>
  </div>
  <div class="info-card">
    <div class="info-card-label">National Empowerment Fund (NEF)</div>
    <div class="info-card-value teal">R3.6B</div>
    <div class="info-card-sub">Total disbursed · All 9 provinces</div>
    <table class="info-card-table">
      <tr><td>Companies funded</td><td>392</td></tr>
      <tr><td>Average deal size</td><td>R9.2M</td></tr>
      <tr><td>Jobs supported</td><td>31,654</td></tr>
      <tr><td>Average cost per job</td><td>R113,616</td></tr>
      <tr><td>Job data published?</td><td class="yes">Yes</td></tr>
    </table>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Six findings ───────────────────────────────────────────────────────────────
st.markdown(section_rule("Six key findings"), unsafe_allow_html=True)
st.markdown("""
<div class="findings-grid">
  <div class="finding-cell">
    <div class="finding-num">01</div>
    <div class="finding-head">Geographic concentration is real and measurable</div>
    <div class="finding-body">Gauteng and KZN received 55.9% of NEF disbursements and 65.6% of all deals — from just 2 of 9 provinces.</div>
    <div class="finding-stat">Gini 0.469</div>
  </div>
  <div class="finding-cell">
    <div class="finding-num">02</div>
    <div class="finding-head">Deal size inequality mirrors income inequality</div>
    <div class="finding-body">The top 0.5% of deals absorb 17% of all money. The bottom 12% share just 0.7% of funding.</div>
    <div class="finding-stat">Gini 0.56</div>
  </div>
  <div class="finding-cell">
    <div class="finding-num">03</div>
    <div class="finding-head critical">Biggest recipients are not the best job creators</div>
    <div class="finding-body">Zero overlap between top-10 disbursements and top-10 job creators. R20.5M per job vs R3,827 per job — same programme.</div>
    <div class="finding-stat">5,366× gap</div>
  </div>
  <div class="finding-cell">
    <div class="finding-num">04</div>
    <div class="finding-head critical">R65.9B deployed with no job accountability metrics</div>
    <div class="finding-body">The IDC publishes no cost-per-job data. The NEF — 18× smaller — tracks every job. The absence is a policy choice.</div>
    <div class="finding-stat">0 metrics</div>
  </div>
  <div class="finding-cell">
    <div class="finding-num">05</div>
    <div class="finding-head">Mining dominates IDC sector funding</div>
    <div class="finding-body">56.5% of named-sector IDC investment goes to mining and metals. New industries received just 1.3%.</div>
    <div class="finding-stat">R16.2B</div>
  </div>
  <div class="finding-cell">
    <div class="finding-num">06</div>
    <div class="finding-head">Data quality gaps limit full accountability</div>
    <div class="finding-body">FY2023–24 absent from IDC data. 56.5% of IDC investment has no sector attribution. Duplicate NEF entries.</div>
    <div class="finding-stat">Multiple gaps</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Nav strip — functional page navigation ─────────────────────────────────────
st.markdown(section_rule("Explore the analysis"), unsafe_allow_html=True)

st.markdown("""
<style>
/* Style the page_link buttons to match the editorial design */
[data-testid="stPageLink"] a {
    display: inline-block;
    font-family: 'Source Serif 4', Georgia, serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    color: #111110 !important;
    background: #FAFAF8 !important;
    border: 0.5px solid #D3D1C7 !important;
    padding: 6px 12px !important;
    text-decoration: none !important;
    margin: 0 4px 6px 0 !important;
}
[data-testid="stPageLink"] a:hover {
    background: #F1EFE8 !important;
    border-color: #BA7517 !important;
    color: #BA7517 !important;
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(7)
pages = [
    ("pages/1_Crisis_Context.py",        "1. Crisis Context"),
    ("pages/2_Geographic_Inequality.py", "2. Geographic Inequality"),
    ("pages/3_Deal_Size_Inequality.py",  "3. Deal Size"),
    ("pages/4_Job_Efficiency.py",        "4. Job Efficiency"),
    ("pages/5_Sector_Concentration.py",  "5. Sector Concentration"),
    ("pages/6_Job_ROI_Predictor.py",     "6. Job ROI Predictor"),
    ("pages/7_Anomaly_Detection.py",     "7. Anomaly Detection"),
]
for col, (path, label) in zip(cols, pages):
    with col:
        st.page_link(path, label=label)

st.markdown("""
<div class="ack-note">
  The underlying dataset was compiled by <strong>@AfikaSoyamba</strong>
  (<a href="https://x.com/AfikaSoyamba" target="_blank" style="color:#BA7517;">find him on X, formerly Twitter</a>) —
  a database of 1,248 South African businesses funded by the IDC and NEF,
  including every company name, amount, and province.
  This analysis would not exist without that work.
</div>
""", unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)