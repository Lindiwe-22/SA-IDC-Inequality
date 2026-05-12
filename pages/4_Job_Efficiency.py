import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Job Creation Efficiency", page_icon="⚠️", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

st.markdown(page_masthead(
    "Section 4 of 5 &nbsp;·&nbsp; Job Creation Efficiency",
    "Biggest Recipients Are<br>Not the Best <em>Job Creators</em>",
    "There is zero overlap between the top-10 NEF recipients and the top-10 job creators. "
    "The efficiency gap between the most and least effective deals is 5,366×. "
    "This is the central finding of this analysis."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>The central finding:</strong> There is <strong>zero overlap</strong> between the "
    "top-10 companies that received the most NEF money and the top-10 companies that created "
    "the most jobs. The single largest recipient — Khatu Industrial & Chemical — received "
    "<strong>R534 million</strong> and created <strong>26 jobs</strong>. "
    "Meanwhile, Umnotho Maize received <strong>R9 million</strong> and created "
    "<strong>2,352 jobs</strong>. Against 13.3 million underutilised workers, "
    "this allocation pattern cannot be justified on job-creation grounds alone.",
    "alert"
), unsafe_allow_html=True)

# ── Original hardcoded data ────────────────────────────────────────────────────
top_disbursed = pd.DataFrame({
    'Company':     ['Khatu Industrial & Chemical','CK Mafutha (Pty) Ltd',
                    'Devland Gardens (Pty) Ltd',"Africa's Best 350 (Pty) Ltd",
                    'Mandini Group','Hayett Investments (Pty) Ltd',
                    'Dandelton Investments (Pty) Ltd','Salim Munshi Family Trust',
                    'Greyline Holdings','Suntrans CC'],
    'Province':    ['Northern Cape','Western Cape','Gauteng','Eastern Cape',
                    'Gauteng','KwaZulu-Natal','KwaZulu-Natal','KwaZulu-Natal',
                    'Gauteng','KwaZulu-Natal'],
    'Disbursed_M': [534.0, 77.2, 49.0, 44.5, 44.4, 43.6, 43.3, 38.7, 38.2, 38.1],
    'Jobs':        [26, 4, 16, 442, 142, 230, 96, 613, 258, 74],
    'CostPerJob':  [20538462, 19300000, 3062500, 100679, 312676,
                    189565, 451042, 63132, 148062, 514865],
})

top_jobs = pd.DataFrame({
    'Company':     ['Umnotho Maize (Pty) Ltd','Icebolethu Burial Services',
                    'Tshellaine Holdings','Lebowakgomo Poultry (Pty) Ltd',
                    'KPML Group (Pty) Ltd','Bibi Cash & Carry Superstore',
                    'Salim Munshi Family Trust','Ubettina Wethu Company'],
    'Province':    ['Gauteng','KwaZulu-Natal','Gauteng','Limpopo',
                    'Gauteng','Free State','KwaZulu-Natal','Gauteng'],
    'Jobs':        [2352, 1843, 1664, 887, 805, 785, 613, 593],
    'Disbursed_M': [9.0, 19.1, 37.8, 1.6, 2.0, 27.7, 38.7, 5.0],
    'CostPerJob':  [3827, 10364, 22716, 1804, 2484, 35287, 63132, 8432],
})

# ── Headline stats ─────────────────────────────────────────────────────────────
st.markdown(section_rule("The headline numbers"), unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:#FDF0F0; border:0.5px solid #D3D1C7; border-top:2px solid #C53030; padding:20px; text-align:center;">
  <div class="info-card-label" style="color:#7A1F1F; margin-bottom:8px;">Worst Cost per Job (NEF)</div>
  <div style="font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#7A1F1F;">R20.5M</div>
  <div style="font-size:12px; color:#C53030; margin-top:4px; font-family:'Source Serif 4',serif;">Khatu Industrial · 26 jobs on R534M</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FDF6E8; border:0.5px solid #D3D1C7; border-top:2px solid #BA7517; padding:20px; text-align:center;">
  <div class="info-card-label" style="color:#5C3A06; margin-bottom:8px;">National Average Cost per Job</div>
  <div style="font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#5C3A06;">R113,616</div>
  <div style="font-size:12px; color:#BA7517; margin-top:4px; font-family:'Source Serif 4',serif;">Across all 392 NEF companies</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:#E8F5EF; border:0.5px solid #D3D1C7; border-top:2px solid #0F6E56; padding:20px; text-align:center;">
  <div class="info-card-label" style="color:#084D3A; margin-bottom:8px;">Best Cost per Job (NEF)</div>
  <div style="font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#084D3A;">R1,804</div>
  <div style="font-size:12px; color:#0F6E56; margin-top:4px; font-family:'Source Serif 4',serif;">Lebowakgomo Poultry · 887 jobs on R1.6M</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 1: Scatter ───────────────────────────────────────────────────────────
st.markdown(section_rule("Deal size vs job creation efficiency"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Each bubble = one company. Bubble size = number of jobs. Higher on the y-axis = worse efficiency.</div>', unsafe_allow_html=True)

fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(
    x=top_disbursed['Disbursed_M'],
    y=top_disbursed['CostPerJob'] / 1e6,
    mode='markers+text',
    marker=dict(
        size=[max(j / 15, 10) for j in top_disbursed['Jobs']],
        color=top_disbursed['CostPerJob'],
        colorscale='RdYlGn_r',
        showscale=True,
        colorbar=dict(
            title='Cost per Job (R)',
            tickformat='R,.0f',
            title_font=dict(family='Source Serif 4, Georgia, serif', size=11),
        ),
        line=dict(color='#FAFAF8', width=1.5),
    ),
    text=[c.split('(')[0].strip()[:20] for c in top_disbursed['Company']],
    textposition='top center',
    textfont=dict(size=10, color='#2C2C2A', family='Source Serif 4, Georgia, serif'),
    customdata=list(zip(top_disbursed['Company'], top_disbursed['Jobs'],
                        top_disbursed['CostPerJob'], top_disbursed['Province'])),
    hovertemplate=(
        '<b>%{customdata[0]}</b><br>'
        'Disbursed: R%{x:.1f}M<br>'
        'Jobs: %{customdata[1]}<br>'
        'Cost per Job: R%{customdata[2]:,.0f}<br>'
        'Province: %{customdata[3]}<extra></extra>'
    ),
))
fig_scatter = apply_plotly_theme(fig_scatter, height=460)
fig_scatter.update_layout(
    xaxis=dict(title='Total Disbursed (R millions)', gridcolor='#EDECEA'),
    yaxis=dict(title='Cost per Job (R millions)', gridcolor='#EDECEA'),
    margin=dict(t=24, b=24, l=20, r=20),
    showlegend=False,
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown(callout(
    "<strong>No correlation between deal size and job efficiency.</strong> "
    "The two most expensive job-creation deals both received over R70M. "
    "Africa's Best 350 received R44.5M and created 442 jobs at R100,679/job — "
    "10× more efficient than Khatu Industrial which received 12× more money."
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Chart 2: Top 10 comparison ─────────────────────────────────────────────────
st.markdown(section_rule("Who got the most money vs who created the most jobs"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">These two lists should overlap significantly — in a well-functioning programme, they do not.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""<div class="info-card-label" style="margin-bottom:10px; padding-left:4px;">Top 10 Largest Disbursements</div>""", unsafe_allow_html=True)
    sorted_d = top_disbursed.sort_values('Disbursed_M', ascending=True)
    bar_colors_d = ['#C53030' if v > 1_000_000 else '#BA7517' for v in sorted_d['CostPerJob']]
    fig_d = go.Figure()
    fig_d.add_trace(go.Bar(
        y=[c.split('(')[0].strip()[:28] for c in sorted_d['Company']],
        x=sorted_d['Disbursed_M'],
        orientation='h',
        marker_color=bar_colors_d,
        customdata=list(zip(sorted_d['Jobs'], sorted_d['CostPerJob'])),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Disbursed: R%{x:.1f}M<br>'
            'Jobs: %{customdata[0]}<br>'
            'Cost/job: R%{customdata[1]:,.0f}<extra></extra>'
        ),
        text=[f"{j} jobs" for j in sorted_d['Jobs']],
        textposition='outside',
        textfont=dict(size=10, color='#888780', family='Source Serif 4, Georgia, serif'),
    ))
    fig_d = apply_plotly_theme(fig_d, height=380)
    fig_d.update_layout(
        xaxis=dict(title='Disbursed (R millions)', gridcolor='#EDECEA'),
        yaxis=dict(title=''),
        margin=dict(t=10, b=24, l=10, r=80),
        showlegend=False,
    )
    st.plotly_chart(fig_d, use_container_width=True)
    st.markdown('<div style="font-size:11px; color:#888780; font-family:\'Source Serif 4\',serif; padding-left:4px;">Red = cost per job &gt; R1M &nbsp;·&nbsp; Amber = cost per job under R1M</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="info-card-label" style="margin-bottom:10px; padding-left:4px;">Top 10 Job Creators</div>""", unsafe_allow_html=True)
    sorted_j = top_jobs.sort_values('Jobs', ascending=True)
    fig_j = go.Figure()
    fig_j.add_trace(go.Bar(
        y=[c.split('(')[0].strip()[:28] for c in sorted_j['Company']],
        x=sorted_j['Jobs'],
        orientation='h',
        marker_color='#0F6E56',
        customdata=list(zip(sorted_j['Disbursed_M'], sorted_j['CostPerJob'])),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Jobs: %{x}<br>'
            'Disbursed: R%{customdata[0]:.1f}M<br>'
            'Cost/job: R%{customdata[1]:,.0f}<extra></extra>'
        ),
        text=[f"R{c:,.0f}/job" for c in sorted_j['CostPerJob']],
        textposition='outside',
        textfont=dict(size=10, color='#888780', family='Source Serif 4, Georgia, serif'),
    ))
    fig_j = apply_plotly_theme(fig_j, height=380)
    fig_j.update_layout(
        xaxis=dict(title='Jobs Created', gridcolor='#EDECEA'),
        yaxis=dict(title=''),
        margin=dict(t=10, b=24, l=10, r=120),
        showlegend=False,
    )
    st.plotly_chart(fig_j, use_container_width=True)
    st.markdown('<div style="font-size:11px; color:#888780; font-family:\'Source Serif 4\',serif; padding-left:4px;">Note: KPML Group and Bibi Cash &amp; Carry appear as duplicates in source data (PQ705)</div>', unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── 5,366× finding ────────────────────────────────────────────────────────────
st.markdown(section_rule("The 5,366× gap — a public accountability failure"), unsafe_allow_html=True)

st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:32px;">
  <div style="display:flex; gap:32px; flex-wrap:wrap; align-items:flex-start;">
    <div style="flex:1; min-width:220px;">
      <div style="font-size:10px; color:#C53030; text-transform:uppercase; letter-spacing:0.18em; margin-bottom:10px; font-family:'Source Serif 4',serif; font-weight:600;">Worst Outcome</div>
      <div style="font-family:'Playfair Display',serif; font-size:18px; font-weight:700; color:#111110; margin-bottom:4px;">Khatu Industrial &amp; Chemical</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">Northern Cape</div>
      <div style="margin-top:14px; font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#A32D2D;">R534,000,000</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">disbursed</div>
      <div style="margin-top:8px; font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#A32D2D;">26 jobs</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">created</div>
      <div style="margin-top:10px; font-size:15px; font-weight:700; color:#A32D2D; font-family:'Playfair Display',serif;">= R20,538,462 per job</div>
    </div>
    <div style="display:flex; align-items:center; padding:0 8px;">
      <div style="font-family:'Playfair Display',serif; font-size:28px; color:#D3D1C7; font-weight:300;">vs</div>
    </div>
    <div style="flex:1; min-width:220px;">
      <div style="font-size:10px; color:#0F6E56; text-transform:uppercase; letter-spacing:0.18em; margin-bottom:10px; font-family:'Source Serif 4',serif; font-weight:600;">Best Outcome</div>
      <div style="font-family:'Playfair Display',serif; font-size:18px; font-weight:700; color:#111110; margin-bottom:4px;">Umnotho Maize (Pty) Ltd</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">Gauteng</div>
      <div style="margin-top:14px; font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#0F6E56;">R9,000,000</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">disbursed</div>
      <div style="margin-top:8px; font-family:'Playfair Display',serif; font-size:24px; font-weight:700; color:#0F6E56;">2,352 jobs</div>
      <div style="font-size:12px; color:#888780; font-family:'Source Serif 4',serif;">created</div>
      <div style="margin-top:10px; font-size:15px; font-weight:700; color:#0F6E56; font-family:'Playfair Display',serif;">= R3,827 per job</div>
    </div>
    <div style="flex:1; min-width:200px; background:#FDF0F0; border-left:3px solid #C53030; padding:22px;">
      <div style="font-size:10px; color:#7A1F1F; text-transform:uppercase; letter-spacing:0.18em; margin-bottom:10px; font-family:'Source Serif 4',serif; font-weight:600;">The Gap</div>
      <div style="font-family:'Playfair Display',serif; font-size:48px; font-weight:900; color:#7A1F1F; line-height:1;">5,366×</div>
      <div style="font-size:13px; color:#7A1F1F; margin-top:10px; line-height:1.7; font-family:'Source Serif 4',serif;">
        Khatu Industrial costs <strong>5,366 times more</strong> per job than Umnotho Maize.
        Both received public NEF money. Neither outcome is an error — they are a policy choice.
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
