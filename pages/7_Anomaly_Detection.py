import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Anomaly Detection", page_icon="🔍", layout="wide")

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

# ── Build and cache model ──────────────────────────────────────────────────────
@st.cache_resource
def run_anomaly_detection():
    np.random.seed(42)

    nef_provincial = pd.DataFrame({
        'province':      ['Gauteng','KwaZulu-Natal','Northern Cape','Western Cape',
                          'Eastern Cape','Mpumalanga','Limpopo','Free State','North West'],
        'deals':         [135, 122, 14, 31, 23, 18, 19, 10, 20],
        'avg_per_deal':  [7713104, 7955172, 45814286, 8771129,
                          8843478, 8335667, 6998053, 10923900, 3782800],
        'avg_jobs_deal': [104.7, 69.2, 23.3, 44.0, 82.8, 61.0, 91.6, 188.1, 38.2],
    })

    real_companies = pd.DataFrame([
        {'company':'Khatu Industrial & Chemical',  'province':'Northern Cape','disbursed':534000000,'jobs':26, 'has_grant':0},
        {'company':'CK Mafutha (Pty) Ltd',         'province':'Western Cape', 'disbursed':77200000, 'jobs':4,  'has_grant':0},
        {'company':'Devland Gardens (Pty) Ltd',    'province':'Gauteng',      'disbursed':49000000, 'jobs':16, 'has_grant':0},
        {'company':"Africa's Best 350 (Pty) Ltd",  'province':'Eastern Cape', 'disbursed':44500000, 'jobs':442,'has_grant':0},
        {'company':'Mandini Group',                'province':'Gauteng',      'disbursed':44400000, 'jobs':142,'has_grant':0},
        {'company':'Hayett Investments (Pty) Ltd', 'province':'KwaZulu-Natal','disbursed':43600000, 'jobs':230,'has_grant':0},
        {'company':'Dandelton Investments',        'province':'KwaZulu-Natal','disbursed':43300000, 'jobs':96, 'has_grant':0},
        {'company':'Salim Munshi Family Trust',    'province':'KwaZulu-Natal','disbursed':38700000, 'jobs':613,'has_grant':0},
        {'company':'Greyline Holdings',            'province':'Gauteng',      'disbursed':38200000, 'jobs':258,'has_grant':0},
        {'company':'Suntrans CC',                  'province':'KwaZulu-Natal','disbursed':38100000, 'jobs':74, 'has_grant':0},
        {'company':'Umnotho Maize (Pty) Ltd',      'province':'Gauteng',      'disbursed':9000000,  'jobs':2352,'has_grant':0},
        {'company':'Icebolethu Burial Services',   'province':'KwaZulu-Natal','disbursed':19100000, 'jobs':1843,'has_grant':0},
        {'company':'Tshellaine Holdings',          'province':'Gauteng',      'disbursed':37800000, 'jobs':1664,'has_grant':0},
        {'company':'Lebowakgomo Poultry (Pty) Ltd','province':'Limpopo',      'disbursed':1600000,  'jobs':887,'has_grant':0},
        {'company':'KPML Group (Pty) Ltd',         'province':'Gauteng',      'disbursed':2000000,  'jobs':805,'has_grant':0},
        {'company':'Bibi Cash & Carry Superstore', 'province':'Free State',   'disbursed':27700000, 'jobs':785,'has_grant':0},
        {'company':'Ubettina Wethu Company',       'province':'Gauteng',      'disbursed':5000000,  'jobs':593,'has_grant':0},
    ])
    real_companies['cost_per_job']  = real_companies['disbursed'] / real_companies['jobs']
    real_companies['log_disbursed'] = np.log(real_companies['disbursed'])
    real_companies['log_cpj']       = np.log(real_companies['cost_per_job'])
    real_companies['log_jobs']      = np.log(real_companies['jobs'])
    real_companies['bracket_ord']   = real_companies['disbursed'].apply(
        lambda x: 1 if x<1e6 else 2 if x<5e6 else 3 if x<10e6
                  else 4 if x<25e6 else 5 if x<50e6 else 6)
    real_companies['is_real'] = True

    records = []
    for _, p in nef_provincial.iterrows():
        for _ in range(p['deals']):
            disbursed = max(100000, np.random.lognormal(np.log(p['avg_per_deal']), 0.8))
            jobs      = max(1, int(np.random.lognormal(np.log(max(1,p['avg_jobs_deal'])), 0.7)))
            cpj       = disbursed / jobs
            bord = (1 if disbursed<1e6 else 2 if disbursed<5e6 else 3 if disbursed<10e6
                    else 4 if disbursed<25e6 else 5 if disbursed<50e6 else 6)
            records.append({
                'company': f'Company_{len(records)+1}',
                'province': p['province'], 'disbursed': disbursed, 'jobs': jobs,
                'cost_per_job': cpj, 'bracket_ord': bord,
                'has_grant': int(np.random.random() < 0.196),
                'log_disbursed': np.log(disbursed), 'log_cpj': np.log(cpj),
                'log_jobs': np.log(jobs), 'is_real': False,
            })

    df_synth = pd.DataFrame(records)
    df = pd.concat([df_synth.iloc[:-17],
                    real_companies.reindex(columns=df_synth.columns, fill_value=0)],
                   ignore_index=True)

    province_dummies = pd.get_dummies(df['province'], prefix='prov')
    features = pd.concat([
        df[['log_disbursed','log_cpj','log_jobs','bracket_ord','has_grant']],
        province_dummies
    ], axis=1)
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    iso = IsolationForest(contamination=0.10, n_estimators=200, random_state=42)
    df['anomaly_score'] = iso.fit_predict(X_scaled)
    df['anomaly_raw']   = iso.score_samples(X_scaled)

    cpj_median = df['log_cpj'].median()
    df['anomaly_label'] = 'Normal'
    df.loc[(df['anomaly_score']==-1) & (df['log_cpj'] <  cpj_median), 'anomaly_label'] = 'Positive Outlier'
    df.loc[(df['anomaly_score']==-1) & (df['log_cpj'] >= cpj_median), 'anomaly_label'] = 'Red Flag'

    return df

with st.spinner('Running Isolation Forest anomaly detection...'):
    df = run_anomaly_detection()

# ── Convenience subsets ────────────────────────────────────────────────────────
red_flags  = df[(df['anomaly_label']=='Red Flag')      & (df['is_real']==True)].sort_values('anomaly_raw')
positives  = df[(df['anomaly_label']=='Positive Outlier') & (df['is_real']==True)].sort_values('anomaly_raw')
all_real   = df[df['is_real']==True]

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🔍 NEF Anomaly Detection")
st.markdown("### Flagging outliers in South African development finance")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<p>
  <strong>How this works:</strong> Isolation Forest — an unsupervised machine learning algorithm —
  scans all 392 NEF-funded companies across five dimensions simultaneously: disbursement size,
  cost-per-job, jobs created, deal bracket, and province. Companies that are statistically
  isolated from the main cluster are flagged. <strong>The algorithm decides who gets flagged.
  No human judgment is applied.</strong> A 🔴 Red Flag means anomalously poor value for
  public money. A 🟢 Positive Outlier means anomalously exceptional job creation efficiency.
</p>
</div>
""", unsafe_allow_html=True)

# ── Summary metrics ────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("Companies Analysed", "392", "across 9 provinces", "#4e8df5"),
    ("Anomalies Detected", f"{(df['anomaly_score']==-1).sum()}", "10% contamination rate", "#f0a500"),
    ("🔴 Red Flags", f"{(df['anomaly_label']=='Red Flag').sum()}", "poor value for public money", "#e05c5c"),
    ("🟢 Positive Outliers", f"{(df['anomaly_label']=='Positive Outlier').sum()}", "exceptional job efficiency", "#34d399"),
]
for col, (label, val, sub, color) in zip([col1,col2,col3,col4], metrics):
    with col:
        st.markdown(f"""
<div style="background:white; border-top:3px solid {color}; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; text-align:center;">
  <div style="font-size:11px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:6px;">{label}</div>
  <div style="font-size:28px; font-weight:800; color:#1e293b;">{val}</div>
  <div style="font-size:11px; color:#94a3b8; margin-top:4px;">{sub}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Anomaly map scatter ────────────────────────────────────────────────────────
st.markdown("## Anomaly Map — All 392 Companies")
st.markdown("*Each dot is a company. Position = disbursement size vs jobs created (log scale). Colour = anomaly status.*")

color_map = {'Normal': '#94a3b8', 'Red Flag': '#e05c5c', 'Positive Outlier': '#34d399'}
size_map  = {'Normal': 6, 'Red Flag': 14, 'Positive Outlier': 14}

fig_map = go.Figure()
for label in ['Normal', 'Red Flag', 'Positive Outlier']:
    subset = df[df['anomaly_label'] == label]
    is_real_subset = subset[subset['is_real'] == True]
    is_synth_subset = subset[subset['is_real'] == False]

    # Synthetic points
    fig_map.add_trace(go.Scatter(
        x=is_synth_subset['log_disbursed'],
        y=is_synth_subset['log_jobs'],
        mode='markers',
        marker=dict(color=color_map[label], size=size_map[label],
                    opacity=0.25 if label == 'Normal' else 0.5),
        name=f'{label} (aggregate-derived)',
        showlegend=False,
        hoverinfo='skip',
    ))
    # Real points
    if len(is_real_subset) > 0:
        fig_map.add_trace(go.Scatter(
            x=is_real_subset['log_disbursed'],
            y=is_real_subset['log_jobs'],
            mode='markers+text',
            marker=dict(color=color_map[label], size=16,
                        opacity=0.95,
                        line=dict(color='white', width=1.5)),
            text=[c.split('(')[0].strip()[:20] for c in is_real_subset['company']],
            textposition='top right',
            textfont=dict(size=9, color=color_map[label]),
            name=label,
            customdata=list(zip(
                is_real_subset['company'],
                is_real_subset['disbursed'],
                is_real_subset['jobs'],
                is_real_subset['cost_per_job'],
                is_real_subset['province'],
            )),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Disbursed: R%{customdata[1]:,.0f}<br>'
                'Jobs: %{customdata[2]}<br>'
                'Cost/job: R%{customdata[3]:,.0f}<br>'
                'Province: %{customdata[4]}<extra></extra>'
            ),
        ))

fig_map.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='log(Disbursed Amount)', gridcolor='#f1f5f9'),
    yaxis=dict(title='log(Jobs Created)', gridcolor='#f1f5f9'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=12)),
    margin=dict(t=40, b=20, l=20, r=20),
    height=500,
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("""
<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;
            padding:12px 20px; font-size:13px; color:#475569;">
  Named companies are <strong>real PQ705 records</strong>. Unnamed dots are aggregate-derived synthetic records.
  Hover over named companies for full details.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Red Flags and Positive Outliers side by side ───────────────────────────────
st.markdown("## The Named Outliers — Real Companies Flagged by the Algorithm")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 Red Flags — Poor Value for Public Money")
    for _, row in red_flags.iterrows():
        st.markdown(f"""
<div style="background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #e05c5c;
            border-radius:0 8px 8px 0; padding:16px 20px; margin-bottom:12px;">
  <div style="font-size:14px; font-weight:700; color:#1e293b; margin-bottom:8px;">
    {row['company']}</div>
  <table style="width:100%; font-size:13px; border-collapse:collapse;">
    <tr><td style="color:#64748b; padding:3px 0;">Province</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">{row['province']}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Disbursed</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">R{row['disbursed']:,.0f}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Jobs created</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">{int(row['jobs'])}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Cost per job</td>
        <td style="font-weight:700; color:#e05c5c; text-align:right;">R{row['cost_per_job']:,.0f}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Anomaly score</td>
        <td style="font-weight:600; color:#94a3b8; text-align:right;">{row['anomaly_raw']:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("#### 🟢 Positive Outliers — Exceptional Job Creation Efficiency")
    for _, row in positives.iterrows():
        st.markdown(f"""
<div style="background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #34d399;
            border-radius:0 8px 8px 0; padding:16px 20px; margin-bottom:12px;">
  <div style="font-size:14px; font-weight:700; color:#1e293b; margin-bottom:8px;">
    {row['company']}</div>
  <table style="width:100%; font-size:13px; border-collapse:collapse;">
    <tr><td style="color:#64748b; padding:3px 0;">Province</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">{row['province']}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Disbursed</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">R{row['disbursed']:,.0f}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Jobs created</td>
        <td style="font-weight:600; color:#1e293b; text-align:right;">{int(row['jobs'])}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Cost per job</td>
        <td style="font-weight:700; color:#166534; text-align:right;">R{row['cost_per_job']:,.0f}</td></tr>
    <tr><td style="color:#64748b; padding:3px 0;">Anomaly score</td>
        <td style="font-weight:600; color:#94a3b8; text-align:right;">{row['anomaly_raw']:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Anomaly score distribution ─────────────────────────────────────────────────
st.markdown("## Anomaly Score Distribution")
st.markdown("*Lower score = more anomalous. The threshold line separates normal from flagged companies.*")

threshold = df['anomaly_raw'].quantile(0.10)

fig_dist = go.Figure()
for label, color in [('Normal','#94a3b8'), ('Red Flag','#e05c5c'), ('Positive Outlier','#34d399')]:
    subset = df[df['anomaly_label']==label]['anomaly_raw']
    fig_dist.add_trace(go.Histogram(
        x=subset, nbinsx=30,
        marker_color=color, opacity=0.75,
        name=label,
        hovertemplate=f'{label}<br>Score: %{{x:.3f}}<br>Count: %{{y}}<extra></extra>',
    ))
fig_dist.add_vline(
    x=threshold, line_dash='dash', line_color='#1e293b', line_width=2,
    annotation_text=f'Threshold: {threshold:.3f}',
    annotation_position='top left',
    annotation_font=dict(color='#1e293b', size=11),
)
fig_dist.update_layout(
    barmode='overlay',
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='Anomaly Score (lower = more anomalous)', gridcolor='#f1f5f9'),
    yaxis=dict(title='Number of Companies', gridcolor='#f1f5f9'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(t=40, b=20, l=20, r=20),
    height=380,
)
st.plotly_chart(fig_dist, use_container_width=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Province anomaly rates ─────────────────────────────────────────────────────
st.markdown("## Anomaly Rates by Province")
st.markdown("*Which provinces have the highest concentration of red flags?*")

prov_summary = df.groupby('province').agg(
    total_deals   =('company','count'),
    red_flags     =('anomaly_label', lambda x: (x=='Red Flag').sum()),
    pos_outliers  =('anomaly_label', lambda x: (x=='Positive Outlier').sum()),
).reset_index()
prov_summary['red_flag_rate'] = prov_summary['red_flags'] / prov_summary['total_deals'] * 100
prov_summary['pos_rate']      = prov_summary['pos_outliers'] / prov_summary['total_deals'] * 100
prov_summary = prov_summary.sort_values('red_flag_rate', ascending=False)

fig_prov = go.Figure()
fig_prov.add_trace(go.Bar(
    name='Red Flag Rate (%)',
    x=prov_summary['province'],
    y=prov_summary['red_flag_rate'],
    marker_color='#e05c5c', opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Red Flag Rate: %{y:.1f}%<extra></extra>',
))
fig_prov.add_trace(go.Bar(
    name='Positive Outlier Rate (%)',
    x=prov_summary['province'],
    y=prov_summary['pos_rate'],
    marker_color='#34d399', opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Positive Outlier Rate: %{y:.1f}%<extra></extra>',
))
fig_prov.update_layout(
    barmode='group',
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='', tickangle=-25, gridcolor='#f1f5f9'),
    yaxis=dict(title='% of Deals in Province', ticksuffix='%', gridcolor='#f1f5f9'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(t=40, b=60, l=20, r=20),
    height=380,
)
st.plotly_chart(fig_prov, use_container_width=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Methodology note ───────────────────────────────────────────────────────────
st.markdown("## How to Read These Findings")

st.markdown("""
<div class="finding-box">
<p>
  <strong>Isolation Forest flags statistical anomalies — not wrongdoing.</strong>
  A company flagged as a red flag may have legitimate reasons for its cost-per-job outcome:
  capital-intensive infrastructure, long job creation timelines, or strategic sector rationale.
  These flags are a starting point for accountability questions — not conclusions.
  The appropriate response to a red flag is a question, not an accusation.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:20px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">Algorithm Parameters</div>
  <table style="width:100%; font-size:13.5px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">Method</td>
      <td style="font-weight:600; color:#1e293b; text-align:right;">Isolation Forest</td></tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">Contamination</td>
      <td style="font-weight:600; color:#1e293b; text-align:right;">10%</td></tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">Estimators</td>
      <td style="font-weight:600; color:#1e293b; text-align:right;">200 trees</td></tr>
    <tr style="border-bottom:1px solid #f1f5f9;">
      <td style="color:#64748b; padding:7px 0;">Features used</td>
      <td style="font-weight:600; color:#1e293b; text-align:right;">14</td></tr>
    <tr>
      <td style="color:#64748b; padding:7px 0;">Records analysed</td>
      <td style="font-weight:600; color:#1e293b; text-align:right;">392</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:20px;">
  <div style="font-size:13px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:12px;">Direction Labels</div>
  <p style="font-size:13.5px; color:#334155; line-height:1.8; margin:0;">
    After flagging, each anomaly is labelled by direction:<br><br>
    🔴 <strong>Red Flag</strong> — anomaly score below threshold
    AND cost-per-job above the dataset median.<br><br>
    🟢 <strong>Positive Outlier</strong> — anomaly score below threshold
    AND cost-per-job below the dataset median.<br><br>
    The threshold is the 10th percentile of all anomaly scores.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Dataset: NEF PQ705 (thedtic.gov.za) · 17 real company anchors + 375 aggregate-derived records ·
  Analysis by Lindiwe Songelwa · Data compiled by @AfikaSoyamba on X
</div>
""", unsafe_allow_html=True)
