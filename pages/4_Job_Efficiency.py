import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Job Creation Efficiency", page_icon="⚠️", layout="wide")

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

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# ⚠️ Job Creation Efficiency")
st.markdown("### The most important metric nobody talks about: cost per job")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="alert-box">
<p>
  <strong>The central finding of this analysis:</strong> There is <strong>zero overlap</strong>
  between the top-10 companies that received the most NEF money and the top-10 companies
  that created the most jobs. The single largest recipient — Khatu Industrial & Chemical —
  received <strong>R534 million</strong> and created <strong>26 jobs</strong>.
  Meanwhile, Umnotho Maize received <strong>R9 million</strong> and created
  <strong>2,352 jobs</strong>. Against a backdrop of 13.3 million underutilised workers,
  this allocation pattern cannot be justified on job-creation grounds alone.
</p>
</div>
""", unsafe_allow_html=True)

# ── The headline numbers ───────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
<div style="background:#fef2f2; border:1px solid #fecaca; border-radius:10px;
            padding:20px; text-align:center;">
  <div style="font-size:11px; color:#991b1b; text-transform:uppercase; margin-bottom:6px;">
    Worst Cost per Job (NEF)</div>
  <div style="font-size:24px; font-weight:800; color:#7f1d1d;">R20.5M</div>
  <div style="font-size:12px; color:#b91c1c; margin-top:4px;">Khatu Industrial · 26 jobs on R534M</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#fffbeb; border:1px solid #fde68a; border-radius:10px;
            padding:20px; text-align:center;">
  <div style="font-size:11px; color:#92400e; text-transform:uppercase; margin-bottom:6px;">
    National Average Cost per Job</div>
  <div style="font-size:24px; font-weight:800; color:#92400e;">R113,616</div>
  <div style="font-size:12px; color:#b45309; margin-top:4px;">Across all 392 NEF companies</div>
</div>
""", unsafe_allow_html=True)
with col3:
    st.markdown("""
<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
            padding:20px; text-align:center;">
  <div style="font-size:11px; color:#166534; text-transform:uppercase; margin-bottom:6px;">
    Best Cost per Job (NEF)</div>
  <div style="font-size:24px; font-weight:800; color:#14532d;">R1,804</div>
  <div style="font-size:12px; color:#15803d; margin-top:4px;">Lebowakgomo Poultry · 887 jobs on R1.6M</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 1: Scatter — deal size vs cost per job ───────────────────────────────
st.markdown("## Deal Size vs Job Creation Efficiency")
st.markdown("*Each bubble = one company. Bubble size = number of jobs. Higher on the y-axis = worse efficiency.*")

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
        colorbar=dict(title='Cost per Job (R)', tickformat='R,.0f'),
        line=dict(color='white', width=1.5),
    ),
    text=[c.split('(')[0].strip()[:20] for c in top_disbursed['Company']],
    textposition='top center',
    textfont=dict(size=10, color='#334155'),
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
fig_scatter.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='Total Disbursed (R millions)', gridcolor='#f1f5f9'),
    yaxis=dict(title='Cost per Job (R millions)', gridcolor='#f1f5f9'),
    margin=dict(t=20, b=20, l=20, r=20),
    height=460,
    showlegend=False,
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>No correlation between deal size and job efficiency.</strong>
  The two most expensive job-creation deals both received more than R70M.
  Africa's Best 350 received R44.5M and created 442 jobs at R100,679/job —
  10× more efficient than Khatu Industrial which received 12× more money.
  Within the same programme, a <strong>200× cost-per-job gap</strong> exists.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Chart 2: Top 10 disbursed vs top 10 job creators ──────────────────────────
st.markdown("## Who Got the Most Money vs Who Created the Most Jobs")
st.markdown("*These two lists should overlap significantly — in a well-functioning programme, they don't.*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💰 Top 10 Largest Disbursements")
    sorted_d = top_disbursed.sort_values('Disbursed_M', ascending=True)
    bar_colors_d = ['#e05c5c' if v > 1_000_000 else '#f0a500'
                    for v in sorted_d['CostPerJob']]
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
        textfont=dict(size=10, color='#64748b'),
    ))
    fig_d.update_layout(
        plot_bgcolor='white', paper_bgcolor='#fafafa',
        xaxis=dict(title='Disbursed (R millions)', gridcolor='#f1f5f9'),
        yaxis=dict(title=''),
        margin=dict(t=10, b=20, l=10, r=80),
        height=380, showlegend=False,
        font=dict(color='#334155', size=11),
    )
    st.plotly_chart(fig_d, use_container_width=True)
    st.markdown("""
<div style="font-size:11px; color:#64748b; padding:4px 8px;">
  🔴 Red = cost per job > R1M &nbsp;·&nbsp; 🟡 Gold = cost per job under R1M
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("#### 👷 Top 10 Job Creators")
    sorted_j = top_jobs.sort_values('Jobs', ascending=True)
    fig_j = go.Figure()
    fig_j.add_trace(go.Bar(
        y=[c.split('(')[0].strip()[:28] for c in sorted_j['Company']],
        x=sorted_j['Jobs'],
        orientation='h',
        marker_color='#00c9a7',
        customdata=list(zip(sorted_j['Disbursed_M'], sorted_j['CostPerJob'])),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Jobs: %{x}<br>'
            'Disbursed: R%{customdata[0]:.1f}M<br>'
            'Cost/job: R%{customdata[1]:,.0f}<extra></extra>'
        ),
        text=[f"R{c:,.0f}/job" for c in sorted_j['CostPerJob']],
        textposition='outside',
        textfont=dict(size=10, color='#64748b'),
    ))
    fig_j.update_layout(
        plot_bgcolor='white', paper_bgcolor='#fafafa',
        xaxis=dict(title='Jobs Created', gridcolor='#f1f5f9'),
        yaxis=dict(title=''),
        margin=dict(t=10, b=20, l=10, r=120),
        height=380, showlegend=False,
        font=dict(color='#334155', size=11),
    )
    st.plotly_chart(fig_j, use_container_width=True)
    st.markdown("""
<div style="font-size:11px; color:#64748b; padding:4px 8px;">
  Note: KPML Group and Bibi Cash & Carry appear as duplicates in source data (PQ705)
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── The 5,366× finding ────────────────────────────────────────────────────────
st.markdown("## The 5,366× Gap — A Public Accountability Failure")

st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:12px;
            padding:28px 32px; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
  <div style="display:flex; gap:32px; flex-wrap:wrap;">
    <div style="flex:1; min-width:240px;">
      <div style="font-size:12px; color:#e05c5c; text-transform:uppercase;
                  letter-spacing:0.05em; margin-bottom:8px;">❌ Worst Outcome</div>
      <div style="font-size:18px; font-weight:700; color:#1e293b; margin-bottom:4px;">
        Khatu Industrial & Chemical</div>
      <div style="font-size:13px; color:#64748b;">Northern Cape</div>
      <div style="margin-top:12px; font-size:22px; font-weight:800; color:#e05c5c;">R534,000,000</div>
      <div style="font-size:13px; color:#64748b;">disbursed</div>
      <div style="margin-top:8px; font-size:22px; font-weight:800; color:#e05c5c;">26 jobs</div>
      <div style="font-size:13px; color:#64748b;">created</div>
      <div style="margin-top:8px; font-size:15px; font-weight:700; color:#991b1b;">
        = R20,538,462 per job</div>
    </div>
    <div style="flex:0; display:flex; align-items:center;">
      <div style="font-size:32px; color:#94a3b8;">vs</div>
    </div>
    <div style="flex:1; min-width:240px;">
      <div style="font-size:12px; color:#00c9a7; text-transform:uppercase;
                  letter-spacing:0.05em; margin-bottom:8px;">✓ Best Outcome</div>
      <div style="font-size:18px; font-weight:700; color:#1e293b; margin-bottom:4px;">
        Umnotho Maize (Pty) Ltd</div>
      <div style="font-size:13px; color:#64748b;">Gauteng</div>
      <div style="margin-top:12px; font-size:22px; font-weight:800; color:#00c9a7;">R9,000,000</div>
      <div style="font-size:13px; color:#64748b;">disbursed</div>
      <div style="margin-top:8px; font-size:22px; font-weight:800; color:#00c9a7;">2,352 jobs</div>
      <div style="font-size:13px; color:#64748b;">created</div>
      <div style="margin-top:8px; font-size:15px; font-weight:700; color:#166534;">
        = R3,827 per job</div>
    </div>
    <div style="flex:1; min-width:200px; background:#fef2f2; border-radius:8px; padding:20px;">
      <div style="font-size:12px; color:#991b1b; text-transform:uppercase;
                  letter-spacing:0.05em; margin-bottom:8px;">The Gap</div>
      <div style="font-size:40px; font-weight:900; color:#7f1d1d;">5,366×</div>
      <div style="font-size:13px; color:#991b1b; margin-top:6px; line-height:1.6;">
        Khatu Industrial costs <strong>5,366 times more</strong> per job than Umnotho Maize.
        Both received public NEF money. Neither outcome is an error — they are a policy choice.
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Source: NEF Parliamentary Question PQ705 
  Dataset compiled by <a href="https://x.com/AfikaSoyamba" target="_blank" 
  style="color:#64748b;">@AfikaSoyamba</a> ·
</div>
""", unsafe_allow_html=True)