import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Job ROI Predictor", page_icon="🤖", layout="wide")

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
def build_models():
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
        {'province':'Northern Cape','disbursed':534000000,'jobs':26, 'has_grant':0},
        {'province':'Western Cape', 'disbursed':77200000, 'jobs':4,  'has_grant':0},
        {'province':'Gauteng',      'disbursed':49000000, 'jobs':16, 'has_grant':0},
        {'province':'Eastern Cape', 'disbursed':44500000, 'jobs':442,'has_grant':0},
        {'province':'Gauteng',      'disbursed':44400000, 'jobs':142,'has_grant':0},
        {'province':'KwaZulu-Natal','disbursed':43600000, 'jobs':230,'has_grant':0},
        {'province':'KwaZulu-Natal','disbursed':43300000, 'jobs':96, 'has_grant':0},
        {'province':'KwaZulu-Natal','disbursed':38700000, 'jobs':613,'has_grant':0},
        {'province':'Gauteng',      'disbursed':38200000, 'jobs':258,'has_grant':0},
        {'province':'KwaZulu-Natal','disbursed':38100000, 'jobs':74, 'has_grant':0},
        {'province':'Gauteng',      'disbursed':9000000,  'jobs':2352,'has_grant':0},
        {'province':'KwaZulu-Natal','disbursed':19100000, 'jobs':1843,'has_grant':0},
        {'province':'Gauteng',      'disbursed':37800000, 'jobs':1664,'has_grant':0},
        {'province':'Limpopo',      'disbursed':1600000,  'jobs':887,'has_grant':0},
        {'province':'Gauteng',      'disbursed':2000000,  'jobs':805,'has_grant':0},
        {'province':'Free State',   'disbursed':27700000, 'jobs':785,'has_grant':0},
        {'province':'Gauteng',      'disbursed':5000000,  'jobs':593,'has_grant':0},
    ])
    real_companies['cost_per_job']  = real_companies['disbursed'] / real_companies['jobs']
    real_companies['log_disbursed'] = np.log(real_companies['disbursed'])
    real_companies['log_cpj']       = np.log(real_companies['cost_per_job'])
    real_companies['bracket_ord']   = real_companies['disbursed'].apply(
        lambda x: 1 if x<1e6 else 2 if x<5e6 else 3 if x<10e6
                  else 4 if x<25e6 else 5 if x<50e6 else 6)

    records = []
    for _, p in nef_provincial.iterrows():
        for _ in range(p['deals']):
            disbursed = max(100000, np.random.lognormal(np.log(p['avg_per_deal']), 0.8))
            jobs      = max(1, int(np.random.lognormal(np.log(max(1,p['avg_jobs_deal'])), 0.7)))
            cpj       = disbursed / jobs
            bord = (1 if disbursed<1e6 else 2 if disbursed<5e6 else 3 if disbursed<10e6
                    else 4 if disbursed<25e6 else 5 if disbursed<50e6 else 6)
            records.append({
                'province': p['province'], 'disbursed': disbursed, 'jobs': jobs,
                'cost_per_job': cpj, 'bracket_ord': bord,
                'has_grant': int(np.random.random() < 0.196),
                'log_disbursed': np.log(disbursed), 'log_cpj': np.log(cpj),
            })

    df = pd.DataFrame(records)
    df = pd.concat([df.iloc[:-17], real_companies[df.columns]], ignore_index=True)

    province_dummies = pd.get_dummies(df['province'], prefix='prov', drop_first=True)
    X = pd.concat([df[['log_disbursed','bracket_ord','has_grant']], province_dummies], axis=1)
    y = df['log_cpj']
    feature_cols = X.columns.tolist()
    all_provinces = sorted(df['province'].unique().tolist())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_r2   = r2_score(y_test, lr.predict(X_test))
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr.predict(X_test)))
    lr_cv   = cross_val_score(lr, X, y, cv=kf, scoring='r2').mean()

    rf = RandomForestRegressor(n_estimators=200, max_depth=8,
                                min_samples_leaf=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_r2   = r2_score(y_test, rf.predict(X_test))
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf.predict(X_test)))
    rf_cv   = cross_val_score(rf, X, y, cv=kf, scoring='r2').mean()

    try:
        from xgboost import XGBRegressor
        xgb = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=4,
                           subsample=0.8, colsample_bytree=0.8,
                           random_state=42, verbosity=0)
        xgb.fit(X_train, y_train)
        xgb_r2   = r2_score(y_test, xgb.predict(X_test))
        xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb.predict(X_test)))
        xgb_cv   = cross_val_score(xgb, X, y, cv=kf, scoring='r2').mean()
        xgb_available = True
    except ImportError:
        xgb = None
        xgb_r2 = xgb_rmse = xgb_cv = None
        xgb_available = False

    fi = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)

    return {
        'lr': lr, 'rf': rf, 'xgb': xgb,
        'lr_r2': lr_r2, 'rf_r2': rf_r2, 'xgb_r2': xgb_r2,
        'lr_rmse': lr_rmse, 'rf_rmse': rf_rmse, 'xgb_rmse': xgb_rmse,
        'lr_cv': lr_cv, 'rf_cv': rf_cv, 'xgb_cv': xgb_cv,
        'feature_cols': feature_cols,
        'all_provinces': all_provinces,
        'feature_importance': fi,
        'xgb_available': xgb_available,
        'X_test': X_test, 'y_test': y_test,
        'X': X, 'y': y, 'df': df,
    }

with st.spinner('Training models on NEF dataset...'):
    bundle = build_models()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🤖 Job Creation ROI Predictor")
st.markdown("### Predict cost-per-job from NEF deal characteristics")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<p>
  <strong>How this works:</strong> Three machine learning models were trained on NEF funding data
  (392 companies across 9 provinces) to predict the cost-per-job outcome of a development
  finance deal. Enter deal characteristics below to get a prediction — and see how your
  scenario compares to the national average of <strong>R113,616 per job</strong>.
  <br><br>
  <strong>Data note:</strong> This model is trained on aggregate-derived data with 17 real
  company anchors. Results are directional indicators, not precise forecasts.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Model performance summary ──────────────────────────────────────────────────
st.markdown("## Model Performance")

cols = st.columns(3)
models_meta = [
    ("Linear Regression", bundle['lr_r2'], bundle['lr_rmse'], bundle['lr_cv'], "#f0a500"),
    ("Random Forest",     bundle['rf_r2'], bundle['rf_rmse'], bundle['rf_cv'], "#00c9a7"),
    ("XGBoost",
     bundle['xgb_r2'] if bundle['xgb_available'] else None,
     bundle['xgb_rmse'] if bundle['xgb_available'] else None,
     bundle['xgb_cv'] if bundle['xgb_available'] else None,
     "#a78bfa"),
]

best_r2 = max([m[1] for m in models_meta if m[1] is not None])

for col, (name, r2, rmse, cv, color) in zip(cols, models_meta):
    with col:
        if r2 is None:
            st.markdown(f"""
<div style="background:white; border-top:3px solid #e2e8f0; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px; opacity:0.5;">
  <div style="font-size:13px; font-weight:700; color:#1e293b; margin-bottom:10px;">{name}</div>
  <div style="font-size:13px; color:#94a3b8;">Not available<br>(pip install xgboost)</div>
</div>
""", unsafe_allow_html=True)
        else:
            badge = " 🏆 Best" if r2 == best_r2 else ""
            st.markdown(f"""
<div style="background:white; border-top:3px solid {color}; border:1px solid #e2e8f0;
            border-radius:10px; padding:18px 20px;">
  <div style="font-size:13px; font-weight:700; color:#1e293b; margin-bottom:10px;">
    {name}{badge}</div>
  <table style="width:100%; font-size:13px; border-collapse:collapse;">
    <tr><td style="color:#64748b; padding:4px 0;">Test R²</td>
        <td style="font-weight:700; color:#1e293b; text-align:right;">{r2:.4f}</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">RMSE (log)</td>
        <td style="font-weight:700; color:#1e293b; text-align:right;">{rmse:.4f}</td></tr>
    <tr><td style="color:#64748b; padding:4px 0;">CV R² mean</td>
        <td style="font-weight:700; color:#1e293b; text-align:right;">{cv:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Predictor ──────────────────────────────────────────────────────────────────
st.markdown("## 🔮 Predict Cost-Per-Job for a New Deal")

col_input, col_result = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("#### Enter Deal Characteristics")

    province = st.selectbox(
        "Province",
        options=bundle['all_provinces'],
        help="The province where the funded business operates"
    )
    disbursed_m = st.number_input(
        "Disbursed Amount (R millions)",
        min_value=0.1, max_value=600.0, value=9.0, step=0.5,
        help="Total amount disbursed to the company in R millions"
    )
    has_grant = st.radio(
        "Funding Type",
        options=["Loan only", "Includes a grant"],
        horizontal=True,
        help="Does the funding include a non-repayable grant component?"
    )
    model_choice = st.selectbox(
        "Model to use",
        options=(["Linear Regression", "Random Forest", "XGBoost"]
                 if bundle['xgb_available']
                 else ["Linear Regression", "Random Forest"]),
        index=0,
        help="Linear Regression generally performs best on this dataset"
    )

    predict_btn = st.button("🔮 Predict", type="primary", use_container_width=True)

with col_result:
    st.markdown("#### Prediction Result")

    if predict_btn:
        disbursed  = disbursed_m * 1e6
        has_grant_val = 1 if has_grant == "Includes a grant" else 0
        bracket_ord = (1 if disbursed<1e6 else 2 if disbursed<5e6 else
                       3 if disbursed<10e6 else 4 if disbursed<25e6 else
                       5 if disbursed<50e6 else 6)
        log_disbursed = np.log(disbursed)

        # Build input row matching training feature columns
        input_data = {col: 0 for col in bundle['feature_cols']}
        input_data['log_disbursed'] = log_disbursed
        input_data['bracket_ord']   = bracket_ord
        input_data['has_grant']     = has_grant_val
        prov_col = f"prov_{province}"
        if prov_col in input_data:
            input_data[prov_col] = 1

        X_pred = pd.DataFrame([input_data])[bundle['feature_cols']]

        model = {'Linear Regression': bundle['lr'],
                 'Random Forest':     bundle['rf'],
                 'XGBoost':           bundle['xgb']}.get(model_choice)

        log_pred       = model.predict(X_pred)[0]
        predicted_cpj  = np.exp(log_pred)
        predicted_jobs = int(disbursed / predicted_cpj)
        national_avg   = 113616
        pct_vs_avg     = (predicted_cpj - national_avg) / national_avg * 100

        # Efficiency label
        if predicted_cpj < 50000:
            eff_label = "🟢 Excellent efficiency"
            eff_color = "#166534"
            eff_bg    = "#f0fdf4"
            eff_border= "#00c9a7"
        elif predicted_cpj < 113616:
            eff_label = "🟡 Above average efficiency"
            eff_color = "#92400e"
            eff_bg    = "#fffbeb"
            eff_border= "#f0a500"
        elif predicted_cpj < 500000:
            eff_label = "🟠 Below average efficiency"
            eff_color = "#9a3412"
            eff_bg    = "#fff7ed"
            eff_border= "#f97316"
        else:
            eff_label = "🔴 Poor efficiency"
            eff_color = "#7f1d1d"
            eff_bg    = "#fef2f2"
            eff_border= "#e05c5c"

        st.markdown(f"""
<div style="background:{eff_bg}; border:2px solid {eff_border}; border-radius:12px;
            padding:24px 28px; margin-bottom:16px;">
  <div style="font-size:13px; color:{eff_color}; font-weight:700;
              text-transform:uppercase; letter-spacing:0.05em; margin-bottom:12px;">
    {eff_label}
  </div>
  <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:4px;">
    R{predicted_cpj:,.0f}
  </div>
  <div style="font-size:14px; color:#64748b; margin-bottom:16px;">
    predicted cost per job
  </div>
  <table style="width:100%; font-size:13.5px; border-collapse:collapse;">
    <tr style="border-bottom:1px solid #e2e8f0;">
      <td style="color:#64748b; padding:7px 0;">Estimated jobs created</td>
      <td style="font-weight:700; color:#1e293b; text-align:right;">
        ~{predicted_jobs:,} jobs</td>
    </tr>
    <tr style="border-bottom:1px solid #e2e8f0;">
      <td style="color:#64748b; padding:7px 0;">vs national average (R113,616)</td>
      <td style="font-weight:700; color:{eff_color}; text-align:right;">
        {'+' if pct_vs_avg > 0 else ''}{pct_vs_avg:.1f}%</td>
    </tr>
    <tr style="border-bottom:1px solid #e2e8f0;">
      <td style="color:#64748b; padding:7px 0;">Province</td>
      <td style="font-weight:700; color:#1e293b; text-align:right;">{province}</td>
    </tr>
    <tr style="border-bottom:1px solid #e2e8f0;">
      <td style="color:#64748b; padding:7px 0;">Deal size</td>
      <td style="font-weight:700; color:#1e293b; text-align:right;">R{disbursed_m:.1f}M</td>
    </tr>
    <tr>
      <td style="color:#64748b; padding:7px 0;">Model used</td>
      <td style="font-weight:700; color:#1e293b; text-align:right;">{model_choice}</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

        # Contextual comparison
        st.markdown(f"""
<div style="background:white; border:1px solid #e2e8f0; border-radius:10px; padding:16px 20px;">
  <div style="font-size:12px; color:#64748b; text-transform:uppercase;
              letter-spacing:0.05em; margin-bottom:10px;">How this compares</div>
  <div style="font-size:13px; color:#334155; line-height:1.8;">
    🟢 Best ever: <strong>R1,804/job</strong> — Lebowakgomo Poultry (Limpopo)<br>
    🟡 National avg: <strong>R113,616/job</strong> — NEF portfolio<br>
    🔴 Worst ever: <strong>R20,538,462/job</strong> — Khatu Industrial (N. Cape)
  </div>
</div>
""", unsafe_allow_html=True)

    else:
        st.markdown("""
<div style="background:white; border:2px dashed #e2e8f0; border-radius:12px;
            padding:40px 28px; text-align:center; color:#94a3b8;">
  <div style="font-size:32px; margin-bottom:12px;">🔮</div>
  <div style="font-size:14px;">Set deal characteristics and click Predict</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Feature importance chart ───────────────────────────────────────────────────
st.markdown("## What Drives Cost-Per-Job? Feature Importance")
st.markdown("*Based on Random Forest — shows which deal characteristics most influence job creation efficiency.*")

fi = bundle['feature_importance'].sort_values(ascending=True)
fi_colors = ['#e05c5c' if v > 0.5 else '#f0a500' if v > 0.05 else '#00c9a7'
             for v in fi]

fig_fi = go.Figure()
fig_fi.add_trace(go.Bar(
    y=fi.index,
    x=fi.values,
    orientation='h',
    marker_color=fi_colors,
    text=[f"{v:.3f}" for v in fi.values],
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
))
fig_fi.update_layout(
    plot_bgcolor='white', paper_bgcolor='#fafafa',
    font=dict(family='sans-serif', color='#334155'),
    xaxis=dict(title='Feature Importance', gridcolor='#f1f5f9'),
    yaxis=dict(title=''),
    margin=dict(t=20, b=20, l=20, r=80),
    height=380, showlegend=False,
)
st.plotly_chart(fig_fi, use_container_width=True)

st.markdown("""
<div class="finding-box">
<p>
  <strong>Key insight:</strong> Deal size (log_disbursed) accounts for over 85% of predictive
  power. <strong>Smaller deals create jobs more cheaply.</strong> Yet the deal size inequality
  analysis showed small deals (under R1m) receive just 0.7% of NEF funding.
  The model confirms: the current allocation pattern systematically funds
  the least efficient job creation outcomes.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Predicted vs Actual chart ──────────────────────────────────────────────────
st.markdown("## Predicted vs Actual — Model Fit")
st.markdown("*Points close to the diagonal line = accurate predictions. Spread indicates variance.*")

tab1, tab2 = st.tabs(["Linear Regression", "Random Forest"])

for tab, model_key, name in [(tab1, 'lr', 'Linear Regression'),
                              (tab2, 'rf', 'Random Forest')]:
    with tab:
        y_pred = bundle[model_key].predict(bundle['X_test'])
        fig_pva = go.Figure()
        fig_pva.add_trace(go.Scatter(
            x=bundle['y_test'], y=y_pred,
            mode='markers',
            marker=dict(color='#4e8df5', size=7, opacity=0.6,
                        line=dict(color='white', width=0.5)),
            hovertemplate='Actual: %{x:.2f}<br>Predicted: %{y:.2f}<extra></extra>',
            name='Predictions',
        ))
        min_val = min(bundle['y_test'].min(), y_pred.min())
        max_val = max(bundle['y_test'].max(), y_pred.max())
        fig_pva.add_trace(go.Scatter(
            x=[min_val, max_val], y=[min_val, max_val],
            mode='lines', line=dict(color='#e05c5c', dash='dash', width=2),
            name='Perfect fit', hoverinfo='skip',
        ))
        r2 = bundle[f'{model_key}_r2']
        fig_pva.update_layout(
            plot_bgcolor='white', paper_bgcolor='#fafafa',
            font=dict(family='sans-serif', color='#334155'),
            xaxis=dict(title='Actual log(Cost per Job)', gridcolor='#f1f5f9'),
            yaxis=dict(title='Predicted log(Cost per Job)', gridcolor='#f1f5f9'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(t=30, b=20, l=20, r=20),
            height=380,
            title=dict(text=f'{name} — R² = {r2:.4f}',
                       font=dict(size=13, color='#1e293b')),
        )
        st.plotly_chart(fig_pva, use_container_width=True)

st.markdown("""
<div style="text-align:center; padding:24px 0 8px; color:#94a3b8; font-size:12px; margin-top:24px;">
  Model trained on NEF PQ705 data (392 companies, 17 real anchors + 375 aggregate-derived) ·
  Source: IDC Funding Dashboard · NEF Parliamentary Question PQ705
  Dataset compiled by <a href="https://x.com/AfikaSoyamba" target="_blank" 
  style="color:#64748b;">@AfikaSoyamba</a> · 
  Results are directional indicators · Analysis by Lindiwe Songelwa
</div>
""", unsafe_allow_html=True)