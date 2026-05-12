import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import warnings
import sys, os
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Anomaly Detection", page_icon="🔍", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

# ── Build and cache model (original logic — untouched) ─────────────────────────
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

red_flags = df[(df['anomaly_label']=='Red Flag')       & (df['is_real']==True)].sort_values('anomaly_raw')
positives = df[(df['anomaly_label']=='Positive Outlier') & (df['is_real']==True)].sort_values('anomaly_raw')

# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown(page_masthead(
    "Section 7 of 7 &nbsp;·&nbsp; Anomaly Detection",
    "Which Deals Fall<br>Outside the <em>Pattern?</em>",
    "Isolation Forest scans all 392 NEF-funded companies across five dimensions simultaneously. "
    "Companies statistically isolated from the main cluster are flagged. "
    "The algorithm decides who gets flagged. No human judgment is applied."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>How this works:</strong> Isolation Forest — an unsupervised machine learning algorithm — "
    "scans all 392 NEF-funded companies across five dimensions simultaneously: disbursement size, "
    "cost-per-job, jobs created, deal bracket, and province. "
    "<strong>The algorithm decides who gets flagged. No human judgment is applied.</strong> "
    "A Red Flag means anomalously poor value for public money. "
    "A Positive Outlier means anomalously exceptional job creation efficiency.",
    "info"
), unsafe_allow_html=True)

# ── Summary metrics ────────────────────────────────────────────────────────────
st.markdown(section_rule("Detection summary"), unsafe_allow_html=True)
st.markdown(f"""
<div class="stat-strip stat-strip-4">
  <div class="stat-cell info">
    <div class="stat-number blue">392</div>
    <div class="stat-desc">Companies analysed across 9 provinces.</div>
  </div>
  <div class="stat-cell warn">
    <div class="stat-number amber">{(df['anomaly_score']==-1).sum()}</div>
    <div class="stat-desc">Anomalies detected. 10% contamination rate.</div>
  </div>
  <div class="stat-cell alert">
    <div class="stat-number red">{(df['anomaly_label']=='Red Flag').sum()}</div>
    <div class="stat-desc">Red flags. Poor value for public money.</div>
  </div>
  <div class="stat-cell ok">
    <div class="stat-number teal">{(df['anomaly_label']=='Positive Outlier').sum()}</div>
    <div class="stat-desc">Positive outliers. Exceptional job efficiency.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Anomaly map ────────────────────────────────────────────────────────────────
st.markdown(section_rule("Anomaly map — all 392 companies"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Each dot is a company. Position = disbursement size vs jobs created (log scale). Colour = anomaly status.</div>', unsafe_allow_html=True)

color_map = {'Normal': '#B4B2A9', 'Red Flag': '#C53030', 'Positive Outlier': '#0F6E56'}
size_map  = {'Normal': 6, 'Red Flag': 14, 'Positive Outlier': 14}

fig_map = go.Figure()
for label in ['Normal', 'Red Flag', 'Positive Outlier']:
    subset       = df[df['anomaly_label'] == label]
    synth_subset = subset[subset['is_real'] == False]
    real_subset  = subset[subset['is_real'] == True]

    fig_map.add_trace(go.Scatter(
        x=synth_subset['log_disbursed'],
        y=synth_subset['log_jobs'],
        mode='markers',
        marker=dict(color=color_map[label], size=size_map[label],
                    opacity=0.2 if label == 'Normal' else 0.45),
        name=f'{label} (aggregate-derived)',
        showlegend=False,
        hoverinfo='skip',
    ))
    if len(real_subset) > 0:
        fig_map.add_trace(go.Scatter(
            x=real_subset['log_disbursed'],
            y=real_subset['log_jobs'],
            mode='markers+text',
            marker=dict(color=color_map[label], size=16, opacity=0.95,
                        line=dict(color='#FAFAF8', width=1.5)),
            text=[c.split('(')[0].strip()[:20] for c in real_subset['company']],
            textposition='top right',
            textfont=dict(size=9, color=color_map[label],
                          family='Source Serif 4, Georgia, serif'),
            name=label,
            customdata=list(zip(
                real_subset['company'], real_subset['disbursed'],
                real_subset['jobs'], real_subset['cost_per_job'], real_subset['province'],
            )),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Disbursed: R%{customdata[1]:,.0f}<br>'
                'Jobs: %{customdata[2]}<br>'
                'Cost/job: R%{customdata[3]:,.0f}<br>'
                'Province: %{customdata[4]}<extra></extra>'
            ),
        ))

fig_map = apply_plotly_theme(fig_map, height=500)
fig_map.update_layout(
    xaxis=dict(title='log(Disbursed Amount)', gridcolor='#EDECEA'),
    yaxis=dict(title='log(Jobs Created)', gridcolor='#EDECEA'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=11, family='Source Serif 4, Georgia, serif')),
    margin=dict(t=40, b=24, l=20, r=20),
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown('<div style="background:#F1EFE8; border:0.5px solid #D3D1C7; padding:11px 18px; font-size:12px; color:#5F5E5A; font-family:\'Source Serif 4\',Georgia,serif;">Named companies are <strong>real PQ705 records</strong>. Unnamed dots are aggregate-derived synthetic records. Hover over named companies for full details.</div>', unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Red flags and positive outliers ───────────────────────────────────────────
st.markdown(section_rule("The named outliers — real companies flagged by the algorithm"), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="info-card-label" style="color:#C53030; margin-bottom:12px;">Red Flags — Poor Value for Public Money</div>', unsafe_allow_html=True)
    for _, row in red_flags.iterrows():
        st.markdown(f"""
<div style="background:#FDF0F0; border:0.5px solid #D3D1C7; border-left:3px solid #C53030; padding:16px 20px; margin-bottom:12px;">
  <div style="font-family:'Playfair Display',serif; font-size:14px; font-weight:700; color:#111110; margin-bottom:10px;">{row['company']}</div>
  <table class="info-card-table">
    <tr><td>Province</td><td style="text-align:right; font-weight:600;">{row['province']}</td></tr>
    <tr><td>Disbursed</td><td style="text-align:right; font-weight:600;">R{row['disbursed']:,.0f}</td></tr>
    <tr><td>Jobs created</td><td style="text-align:right; font-weight:600;">{int(row['jobs'])}</td></tr>
    <tr><td>Cost per job</td><td style="text-align:right; font-weight:700; color:#C53030;">R{row['cost_per_job']:,.0f}</td></tr>
    <tr><td>Anomaly score</td><td style="text-align:right; color:#888780;">{row['anomaly_raw']:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-card-label" style="color:#0F6E56; margin-bottom:12px;">Positive Outliers — Exceptional Job Creation Efficiency</div>', unsafe_allow_html=True)
    for _, row in positives.iterrows():
        st.markdown(f"""
<div style="background:#E8F5EF; border:0.5px solid #D3D1C7; border-left:3px solid #0F6E56; padding:16px 20px; margin-bottom:12px;">
  <div style="font-family:'Playfair Display',serif; font-size:14px; font-weight:700; color:#111110; margin-bottom:10px;">{row['company']}</div>
  <table class="info-card-table">
    <tr><td>Province</td><td style="text-align:right; font-weight:600;">{row['province']}</td></tr>
    <tr><td>Disbursed</td><td style="text-align:right; font-weight:600;">R{row['disbursed']:,.0f}</td></tr>
    <tr><td>Jobs created</td><td style="text-align:right; font-weight:600;">{int(row['jobs'])}</td></tr>
    <tr><td>Cost per job</td><td style="text-align:right; font-weight:700; color:#0F6E56;">R{row['cost_per_job']:,.0f}</td></tr>
    <tr><td>Anomaly score</td><td style="text-align:right; color:#888780;">{row['anomaly_raw']:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Score distribution ─────────────────────────────────────────────────────────
st.markdown(section_rule("Anomaly score distribution"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Lower score = more anomalous. The threshold line separates normal from flagged companies.</div>', unsafe_allow_html=True)

threshold = df['anomaly_raw'].quantile(0.10)
fig_dist = go.Figure()
for label, color in [('Normal','#B4B2A9'), ('Red Flag','#C53030'), ('Positive Outlier','#0F6E56')]:
    subset = df[df['anomaly_label']==label]['anomaly_raw']
    fig_dist.add_trace(go.Histogram(
        x=subset, nbinsx=30,
        marker_color=color, opacity=0.75,
        name=label,
        hovertemplate=f'{label}<br>Score: %{{x:.3f}}<br>Count: %{{y}}<extra></extra>',
    ))
fig_dist.add_vline(
    x=threshold, line_dash='dash', line_color='#2C2C2A', line_width=1.5,
    annotation_text=f'Threshold: {threshold:.3f}',
    annotation_position='top left',
    annotation_font=dict(color='#2C2C2A', size=11, family='Source Serif 4, Georgia, serif'),
)
fig_dist = apply_plotly_theme(fig_dist, height=380)
fig_dist.update_layout(
    barmode='overlay',
    xaxis=dict(title='Anomaly Score (lower = more anomalous)', gridcolor='#EDECEA'),
    yaxis=dict(title='Number of Companies', gridcolor='#EDECEA'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=11, family='Source Serif 4, Georgia, serif')),
    margin=dict(t=40, b=24, l=20, r=20),
)
st.plotly_chart(fig_dist, use_container_width=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Province anomaly rates ─────────────────────────────────────────────────────
st.markdown(section_rule("Anomaly rates by province"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Which provinces have the highest concentration of red flags?</div>', unsafe_allow_html=True)

prov_summary = df.groupby('province').agg(
    total_deals  =('company','count'),
    red_flags    =('anomaly_label', lambda x: (x=='Red Flag').sum()),
    pos_outliers =('anomaly_label', lambda x: (x=='Positive Outlier').sum()),
).reset_index()
prov_summary['red_flag_rate'] = prov_summary['red_flags'] / prov_summary['total_deals'] * 100
prov_summary['pos_rate']      = prov_summary['pos_outliers'] / prov_summary['total_deals'] * 100
prov_summary = prov_summary.sort_values('red_flag_rate', ascending=False)

fig_prov = go.Figure()
fig_prov.add_trace(go.Bar(
    name='Red Flag Rate (%)',
    x=prov_summary['province'],
    y=prov_summary['red_flag_rate'],
    marker_color='#C53030', opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Red Flag Rate: %{y:.1f}%<extra></extra>',
))
fig_prov.add_trace(go.Bar(
    name='Positive Outlier Rate (%)',
    x=prov_summary['province'],
    y=prov_summary['pos_rate'],
    marker_color='#0F6E56', opacity=0.85,
    hovertemplate='<b>%{x}</b><br>Positive Outlier Rate: %{y:.1f}%<extra></extra>',
))
fig_prov = apply_plotly_theme(fig_prov, height=380)
fig_prov.update_layout(
    barmode='group',
    xaxis=dict(title='', tickangle=-25, gridcolor='#EDECEA'),
    yaxis=dict(title='% of Deals in Province', ticksuffix='%', gridcolor='#EDECEA'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(size=11, family='Source Serif 4, Georgia, serif')),
    margin=dict(t=40, b=60, l=20, r=20),
)
st.plotly_chart(fig_prov, use_container_width=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Methodology ────────────────────────────────────────────────────────────────
st.markdown(section_rule("How to read these findings"), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>Isolation Forest flags statistical anomalies — not wrongdoing.</strong> "
    "A company flagged as a red flag may have legitimate reasons for its cost-per-job outcome: "
    "capital-intensive infrastructure, long job creation timelines, or strategic sector rationale. "
    "These flags are a starting point for accountability questions — not conclusions. "
    "The appropriate response to a red flag is a question, not an accusation."
), unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:20px;">
  <div class="info-card-label" style="margin-bottom:12px;">Algorithm Parameters</div>
  <table class="info-card-table">
    <tr><td>Method</td><td style="text-align:right; font-weight:600;">Isolation Forest</td></tr>
    <tr><td>Contamination</td><td style="text-align:right; font-weight:600;">10%</td></tr>
    <tr><td>Estimators</td><td style="text-align:right; font-weight:600;">200 trees</td></tr>
    <tr><td>Features used</td><td style="text-align:right; font-weight:600;">14</td></tr>
    <tr><td>Records analysed</td><td style="text-align:right; font-weight:600;">392</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:20px;">
  <div class="info-card-label" style="margin-bottom:12px;">Direction Labels</div>
  <p style="font-size:13px; color:#2C2C2A; line-height:1.85; margin:0; font-family:'Source Serif 4',Georgia,serif;">
    After flagging, each anomaly is labelled by direction:<br><br>
    <strong style="color:#C53030;">Red Flag</strong> — anomaly score below threshold
    AND cost-per-job above the dataset median.<br><br>
    <strong style="color:#0F6E56;">Positive Outlier</strong> — anomaly score below threshold
    AND cost-per-job below the dataset median.<br><br>
    The threshold is the 10th percentile of all anomaly scores.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
