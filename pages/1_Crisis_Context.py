import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Crisis Context", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 1 of 7 &nbsp;·&nbsp; Context",
    "The Crisis the DFIs<br>Exist to <em>Solve</em>",
    "Before interrogating where the money goes, the scale of the problem must be established. "
    "South Africa's unemployment crisis is not a statistical abstraction — it is the moral "
    "benchmark against which every rand of development finance must be measured."
), unsafe_allow_html=True)

st.markdown(section_rule("National unemployment — Stats SA QLFS Q3 2025"), unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip stat-strip-4">
  <div class="stat-cell alert">
    <div class="stat-number red">31.9%</div>
    <div class="stat-desc">Official unemployment rate. 13.3M underutilised persons.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">42.4%</div>
    <div class="stat-desc">Expanded unemployment (LU3). Includes discouraged work-seekers.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">46.1%</div>
    <div class="stat-desc">Youth unemployment, age 15–34. Approximately 4.8 million people.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">~60%</div>
    <div class="stat-desc">Youth aged 15–24 unemployed. Nearly 10× the global average.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(callout(
    "Nearly 1 in 2 working-age South Africans is effectively excluded from the formal economy. "
    "Into this crisis, the government deploys billions of rands through development finance "
    "institutions with a constitutional mandate to create jobs and transform the economy. "
    "This analysis asks a single question: <strong>is the money working?</strong>",
    "critical"
), unsafe_allow_html=True)

st.markdown(section_rule("The DFI mandate"), unsafe_allow_html=True)

st.markdown("""
<div class="two-col-grid">
  <div class="grid-card">
    <div class="grid-card-label">Industrial Development Corporation</div>
    <div class="grid-card-amount amber">Est. 1940</div>
    <div class="grid-card-period">Act of Parliament · Fully government-owned</div>
    <table class="grid-table">
      <tr><td>Mandate</td><td>Job-rich industrialisation</td></tr>
      <tr><td>Priority</td><td>Black-owned &amp; empowered companies</td></tr>
      <tr><td>Policy alignment</td><td>NDP, IPAP, Master Plans</td></tr>
      <tr><td>Capital deployed (FY2017–25)</td><td>R65.9B</td></tr>
    </table>
  </div>
  <div class="grid-card">
    <div class="grid-card-label">National Empowerment Fund</div>
    <div class="grid-card-amount teal">Est. 1998</div>
    <div class="grid-card-period">NEF Act 105 of 1998 · DTIC oversight</div>
    <table class="grid-table">
      <tr><td>Mandate</td><td>Broad-based black economic empowerment</td></tr>
      <tr><td>Priority</td><td>Women, youth, rural enterprises</td></tr>
      <tr><td>Policy alignment</td><td>B-BBEE Act, BUSA frameworks</td></tr>
      <tr><td>Capital deployed</td><td>R3.6B</td></tr>
    </table>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(section_rule("Why this analysis exists"), unsafe_allow_html=True)

st.markdown("""
<p>
Both institutions are publicly owned and constitutionally mandated to serve South Africans.
Yet neither publishes a consistent, accessible public record of job creation outcomes per rand deployed.
The IDC — which manages <strong>18.3× more capital</strong> than the NEF — publishes no cost-per-job data at all.
</p>
<p style="margin-top:14px;">
This analysis was built from public-facing dashboard exports, a parliamentary question response,
and official Stats SA data. It does not rely on information the institutions chose to share.
It relies on what they could not avoid publishing.
</p>
""", unsafe_allow_html=True)

st.markdown(data_note(
    "Source: Stats SA Quarterly Labour Force Survey Q3 2025 · IDC Funding Dashboard (FY2017–2025) · "
    "NEF Parliamentary Question PQ705 via dtic.gov.za · Dataset compiled by @AfikaSoyamba"
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
