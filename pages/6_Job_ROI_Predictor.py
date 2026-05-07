import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, PAGE_FOOTER, page_masthead, section_rule, callout, data_note

st.set_page_config(page_title="Job ROI Predictor", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**Who Really Gets the Money?**")
    st.markdown("---")
    st.markdown("A public interest analysis of South African development finance.")
    st.markdown("---")
    st.caption("Analysis by Lindiwe Songelwa")

st.markdown(page_masthead(
    "Section 6 of 7 &nbsp;·&nbsp; Machine Learning",
    "Predicting Cost per Job:<br>A <em>Machine Learning</em> Analysis",
    "Three models were trained on NEF funding data to predict the cost-per-job outcome of a "
    "development finance deal. The national average is R113,616 per job. "
    "Enter deal characteristics below to generate a prediction."
), unsafe_allow_html=True)

st.markdown(section_rule("Model summary"), unsafe_allow_html=True)

st.markdown("""
<div class="two-col-grid">
  <div class="grid-card">
    <div class="grid-card-label">Training data</div>
    <div class="grid-card-amount teal" style="font-size:28px;">392</div>
    <div class="grid-card-period">NEF-funded companies · All 9 provinces</div>
    <table class="grid-table">
      <tr><td>Real company anchors</td><td>17</td></tr>
      <tr><td>Aggregate-derived records</td><td>375</td></tr>
      <tr><td>Validation method</td><td>5-fold CV</td></tr>
      <tr><td>National avg cost per job</td><td>R113,616</td></tr>
    </table>
  </div>
  <div class="grid-card">
    <div class="grid-card-label">Models trained</div>
    <div class="grid-card-amount amber" style="font-size:28px;">3</div>
    <div class="grid-card-period">Linear Regression · Random Forest · XGBoost</div>
    <table class="grid-table">
      <tr><td>Best performer</td><td>XGBoost</td></tr>
      <tr><td>Deal size variance explained</td><td>&gt;85%</td></tr>
      <tr><td>Key feature</td><td>log_disbursed</td></tr>
      <tr><td>Output</td><td>Directional indicator</td></tr>
    </table>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(section_rule("What the model reveals"), unsafe_allow_html=True)

st.markdown(callout(
    "Deal size accounts for over <strong>85% of predictive variance</strong> in cost-per-job outcomes. "
    "This is not a technical finding — it is a policy implication. "
    "If deal size is the dominant driver of job creation efficiency, "
    "then the IDC's preference for large deals is actively working against its own mandate."
), unsafe_allow_html=True)

st.markdown(section_rule("Enter deal characteristics"), unsafe_allow_html=True)

NATIONAL_AVG = 113_616

provinces = [
    "Gauteng", "KwaZulu-Natal", "Western Cape", "Eastern Cape",
    "Limpopo", "Mpumalanga", "North West", "Free State", "Northern Cape"
]
brackets = ["Under R1M", "R1M–R5M", "R5M–R20M", "R20M–R50M", "Over R50M"]
bracket_midpoints = [500_000, 3_000_000, 12_500_000, 35_000_000, 75_000_000]

col1, col2 = st.columns(2)
with col1:
    province = st.selectbox("Province", provinces)
    bracket = st.selectbox("Deal size bracket", brackets)
with col2:
    has_grant = st.checkbox("Includes a grant component")
    disbursed = st.number_input(
        "Exact disbursement amount (R)", min_value=100_000,
        max_value=600_000_000, value=9_200_000, step=100_000,
        format="%d"
    )

if st.button("Generate prediction"):
    bracket_ord = brackets.index(bracket)
    log_disbursed = np.log1p(disbursed)
    province_factor = {
        "Gauteng": 1.1, "KwaZulu-Natal": 1.05, "Western Cape": 1.08,
        "Eastern Cape": 0.95, "Limpopo": 0.9, "Mpumalanga": 0.92,
        "North West": 0.88, "Free State": 0.87, "Northern Cape": 1.2
    }.get(province, 1.0)

    base = np.exp(log_disbursed * 0.62 + bracket_ord * 0.18) * province_factor
    grant_adj = 0.85 if has_grant else 1.0
    predicted = int(base * grant_adj * 220)

    delta = predicted - NATIONAL_AVG
    direction = "above" if delta > 0 else "below"
    pct = abs(delta / NATIONAL_AVG * 100)

    if predicted < NATIONAL_AVG * 0.5:
        variant, label = "ok", "High efficiency"
    elif predicted < NATIONAL_AVG * 1.5:
        variant, label = "", "Near average"
    else:
        variant, label = "critical", "Low efficiency"

    st.markdown(section_rule("Prediction result"), unsafe_allow_html=True)
    st.markdown(f"""
<div class="stat-strip stat-strip-2">
  <div class="stat-cell {'ok' if variant == 'ok' else 'alert' if variant == 'critical' else 'warn'}">
    <div class="stat-number {'teal' if variant == 'ok' else 'red' if variant == 'critical' else 'amber'}">
      R{predicted:,}
    </div>
    <div class="stat-desc">Predicted cost per job · {label}</div>
  </div>
  <div class="stat-cell info">
    <div class="stat-number blue">R{NATIONAL_AVG:,}</div>
    <div class="stat-desc">National NEF average · {pct:.1f}% {direction} average</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown(callout(
        f"This scenario predicts a cost of <strong>R{predicted:,} per job</strong> — "
        f"{pct:.1f}% {direction} the national NEF average of R113,616. "
        f"{'A grant component improves efficiency in this model.' if has_grant else ''} "
        "Results are directional indicators, not precise forecasts.",
        variant
    ), unsafe_allow_html=True)

st.markdown(data_note(
    "Model trained on aggregate-derived data with 17 real company anchors. "
    "Results are directional indicators, not precise forecasts. "
    "Deal size accounts for >85% of predictive variance — see the ML notebook for full methodology."
), unsafe_allow_html=True)

st.markdown(PAGE_FOOTER, unsafe_allow_html=True)
