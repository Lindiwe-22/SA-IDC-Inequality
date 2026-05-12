import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go
import warnings
import sys, os
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import GLOBAL_CSS, FOOTER_HTML, section_rule, callout, page_masthead, sidebar_content, apply_plotly_theme

st.set_page_config(page_title="Job ROI Predictor", page_icon="🤖", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
sidebar_content()

# ── Build and cache model (original logic — untouched) ─────────────────────────
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
    feature_cols  = X.columns.tolist()
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

# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown(page_masthead(
    "Section 6 of 7 &nbsp;·&nbsp; Machine Learning",
    "Predicting Cost per Job:<br>A <em>Machine Learning</em> Analysis",
    "Three models were trained on NEF funding data (392 companies across 9 provinces) "
    "to predict the cost-per-job outcome of a development finance deal. "
    "The national average is R113,616 per job. Enter deal characteristics to generate a prediction."
), unsafe_allow_html=True)

st.markdown(callout(
    "<strong>How this works:</strong> Three machine learning models were trained on NEF funding data "
    "(392 companies across 9 provinces) to predict the cost-per-job outcome of a development "
    "finance deal. Enter deal characteristics below to get a prediction — and see how your "
    "scenario compares to the national average of <strong>R113,616 per job</strong>.<br><br>"
    "<strong>Data note:</strong> This model is trained on aggregate-derived data with 17 real "
    "company anchors. Results are directional indicators, not precise forecasts.",
    "info"
), unsafe_allow_html=True)

# ── Model performance ──────────────────────────────────────────────────────────
st.markdown(section_rule("Model performance"), unsafe_allow_html=True)

cols = st.columns(3)
models_meta = [
    ("Linear Regression", bundle['lr_r2'], bundle['lr_rmse'], bundle['lr_cv'], "#BA7517"),
    ("Random Forest",     bundle['rf_r2'], bundle['rf_rmse'], bundle['rf_cv'], "#0F6E56"),
    ("XGBoost",
     bundle['xgb_r2'] if bundle['xgb_available'] else None,
     bundle['xgb_rmse'] if bundle['xgb_available'] else None,
     bundle['xgb_cv'] if bundle['xgb_available'] else None,
     "#185FA5"),
]
best_r2 = max([m[1] for m in models_meta if m[1] is not None])

for col, (name, r2, rmse, cv, color) in zip(cols, models_meta):
    with col:
        if r2 is None:
            st.markdown(f"""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid #D3D1C7; padding:18px 20px; opacity:0.5;">
  <div class="info-card-label" style="margin-bottom:10px;">{name}</div>
  <div style="font-size:13px; color:#888780; font-family:'Source Serif 4',serif;">Not available<br>(pip install xgboost)</div>
</div>
""", unsafe_allow_html=True)
        else:
            badge = " — Best" if r2 == best_r2 else ""
            st.markdown(f"""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; border-top:2px solid {color}; padding:18px 20px;">
  <div class="info-card-label" style="margin-bottom:10px; color:{color};">{name}{badge}</div>
  <table class="info-card-table">
    <tr><td>Test R²</td><td style="text-align:right; font-weight:700; color:#111110;">{r2:.4f}</td></tr>
    <tr><td>RMSE (log)</td><td style="text-align:right; font-weight:700; color:#111110;">{rmse:.4f}</td></tr>
    <tr><td>CV R² mean</td><td style="text-align:right; font-weight:700; color:#111110;">{cv:.4f}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Predictor ──────────────────────────────────────────────────────────────────
st.markdown(section_rule("Predict cost-per-job for a new deal"), unsafe_allow_html=True)

col_input, col_result = st.columns([1, 1], gap="large")

with col_input:
    st.markdown('<div class="page-eyebrow" style="margin-bottom:12px;">Enter deal characteristics</div>', unsafe_allow_html=True)
    province = st.selectbox("Province", options=bundle['all_provinces'])
    disbursed_m = st.number_input(
        "Disbursed Amount (R millions)",
        min_value=0.1, max_value=600.0, value=9.0, step=0.5,
    )
    has_grant = st.radio(
        "Funding Type",
        options=["Loan only", "Includes a grant"],
        horizontal=True,
    )
    model_choice = st.selectbox(
        "Model to use",
        options=(["Linear Regression", "Random Forest", "XGBoost"]
                 if bundle['xgb_available']
                 else ["Linear Regression", "Random Forest"]),
        index=0,
    )
    predict_btn = st.button("Predict", type="primary", use_container_width=True)

with col_result:
    st.markdown('<div class="page-eyebrow" style="margin-bottom:12px;">Prediction result</div>', unsafe_allow_html=True)

    if predict_btn:
        disbursed     = disbursed_m * 1e6
        has_grant_val = 1 if has_grant == "Includes a grant" else 0
        bracket_ord   = (1 if disbursed<1e6 else 2 if disbursed<5e6 else
                         3 if disbursed<10e6 else 4 if disbursed<25e6 else
                         5 if disbursed<50e6 else 6)
        log_disbursed = np.log(disbursed)

        input_data = {col: 0 for col in bundle['feature_cols']}
        input_data['log_disbursed'] = log_disbursed
        input_data['bracket_ord']   = bracket_ord
        input_data['has_grant']     = has_grant_val
        prov_col = f"prov_{province}"
        if prov_col in input_data:
            input_data[prov_col] = 1

        X_pred = pd.DataFrame([input_data])[bundle['feature_cols']]
        model  = {'Linear Regression': bundle['lr'],
                  'Random Forest':     bundle['rf'],
                  'XGBoost':           bundle['xgb']}.get(model_choice)

        log_pred      = model.predict(X_pred)[0]
        predicted_cpj = np.exp(log_pred)
        predicted_jobs = int(disbursed / predicted_cpj)
        national_avg  = 113616
        pct_vs_avg    = (predicted_cpj - national_avg) / national_avg * 100

        if predicted_cpj < 50000:
            eff_label, border_color, bg_color, text_color = "Excellent efficiency", "#0F6E56", "#E8F5EF", "#084D3A"
        elif predicted_cpj < 113616:
            eff_label, border_color, bg_color, text_color = "Above average efficiency", "#0F6E56", "#E8F5EF", "#084D3A"
        elif predicted_cpj < 500000:
            eff_label, border_color, bg_color, text_color = "Below average efficiency", "#BA7517", "#FDF6E8", "#5C3A06"
        else:
            eff_label, border_color, bg_color, text_color = "Poor efficiency", "#C53030", "#FDF0F0", "#7A1F1F"

        st.markdown(f"""
<div style="background:{bg_color}; border:0.5px solid #D3D1C7; border-left:3px solid {border_color}; padding:24px 28px; margin-bottom:16px;">
  <div style="font-size:10px; color:{text_color}; font-weight:600; text-transform:uppercase; letter-spacing:0.18em; margin-bottom:12px; font-family:'Source Serif 4',serif;">{eff_label}</div>
  <div style="font-family:'Playfair Display',serif; font-size:40px; font-weight:700; color:#111110; line-height:1; margin-bottom:4px;">R{predicted_cpj:,.0f}</div>
  <div style="font-size:13px; color:#888780; margin-bottom:18px; font-family:'Source Serif 4',serif;">predicted cost per job</div>
  <table class="info-card-table">
    <tr><td>Estimated jobs created</td><td style="text-align:right; font-weight:700;">~{predicted_jobs:,} jobs</td></tr>
    <tr><td>vs national average (R113,616)</td><td style="text-align:right; font-weight:700; color:{text_color};">{'+' if pct_vs_avg > 0 else ''}{pct_vs_avg:.1f}%</td></tr>
    <tr><td>Province</td><td style="text-align:right; font-weight:700;">{province}</td></tr>
    <tr><td>Deal size</td><td style="text-align:right; font-weight:700;">R{disbursed_m:.1f}M</td></tr>
    <tr><td>Model used</td><td style="text-align:right; font-weight:700;">{model_choice}</td></tr>
  </table>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:14px 18px;">
  <div class="info-card-label" style="margin-bottom:10px;">How this compares</div>
  <div style="font-size:13px; color:#2C2C2A; line-height:1.9; font-family:'Source Serif 4',serif;">
    Best ever: <strong style="color:#0F6E56;">R1,804/job</strong> — Lebowakgomo Poultry (Limpopo)<br>
    National avg: <strong style="color:#BA7517;">R113,616/job</strong> — NEF portfolio<br>
    Worst ever: <strong style="color:#C53030;">R20,538,462/job</strong> — Khatu Industrial (N. Cape)
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown("""
<div style="background:#FAFAF8; border:0.5px solid #D3D1C7; padding:40px 28px; text-align:center; color:#888780;">
  <div style="font-family:'Playfair Display',serif; font-size:28px; font-weight:700; color:#D3D1C7; margin-bottom:12px;">—</div>
  <div style="font-size:13px; font-family:'Source Serif 4',serif;">Set deal characteristics and click Predict</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Feature importance ─────────────────────────────────────────────────────────
st.markdown(section_rule("What drives cost-per-job? Feature importance"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Based on Random Forest — shows which deal characteristics most influence job creation efficiency.</div>', unsafe_allow_html=True)

fi = bundle['feature_importance'].sort_values(ascending=True)
fi_colors = ['#C53030' if v > 0.5 else '#BA7517' if v > 0.05 else '#0F6E56' for v in fi]

fig_fi = go.Figure()
fig_fi.add_trace(go.Bar(
    y=fi.index,
    x=fi.values,
    orientation='h',
    marker_color=fi_colors,
    text=[f"{v:.3f}" for v in fi.values],
    textposition='outside',
    textfont=dict(size=10, family='Source Serif 4, Georgia, serif'),
    hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>',
))
fig_fi = apply_plotly_theme(fig_fi, height=380)
fig_fi.update_layout(
    xaxis=dict(title='Feature Importance', gridcolor='#EDECEA'),
    yaxis=dict(title=''),
    margin=dict(t=20, b=24, l=20, r=80),
    showlegend=False,
)
st.plotly_chart(fig_fi, use_container_width=True)

st.markdown(callout(
    "<strong>Key insight:</strong> Deal size (log_disbursed) accounts for over 85% of predictive "
    "power. <strong>Smaller deals create jobs more cheaply.</strong> Yet the deal size inequality "
    "analysis showed small deals (under R1m) receive just 0.7% of NEF funding. "
    "The model confirms: the current allocation pattern systematically funds "
    "the least efficient job creation outcomes."
), unsafe_allow_html=True)

st.markdown('<hr class="rule">', unsafe_allow_html=True)

# ── Predicted vs Actual ────────────────────────────────────────────────────────
st.markdown(section_rule("Predicted vs actual — model fit"), unsafe_allow_html=True)
st.markdown('<div class="chart-caption">Points close to the diagonal line = accurate predictions. Spread indicates variance.</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Linear Regression", "Random Forest"])

for tab, model_key, name in [(tab1, 'lr', 'Linear Regression'),
                              (tab2, 'rf', 'Random Forest')]:
    with tab:
        y_pred = bundle[model_key].predict(bundle['X_test'])
        fig_pva = go.Figure()
        fig_pva.add_trace(go.Scatter(
            x=bundle['y_test'], y=y_pred,
            mode='markers',
            marker=dict(color='#185FA5', size=7, opacity=0.6,
                        line=dict(color='#FAFAF8', width=0.5)),
            hovertemplate='Actual: %{x:.2f}<br>Predicted: %{y:.2f}<extra></extra>',
            name='Predictions',
        ))
        min_val = min(bundle['y_test'].min(), y_pred.min())
        max_val = max(bundle['y_test'].max(), y_pred.max())
        fig_pva.add_trace(go.Scatter(
            x=[min_val, max_val], y=[min_val, max_val],
            mode='lines', line=dict(color='#C53030', dash='dash', width=1.5),
            name='Perfect fit', hoverinfo='skip',
        ))
        r2 = bundle[f'{model_key}_r2']
        fig_pva = apply_plotly_theme(fig_pva, height=380)
        fig_pva.update_layout(
            xaxis=dict(title='Actual log(Cost per Job)', gridcolor='#EDECEA'),
            yaxis=dict(title='Predicted log(Cost per Job)', gridcolor='#EDECEA'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(size=11, family='Source Serif 4, Georgia, serif')),
            margin=dict(t=30, b=24, l=20, r=20),
            title=dict(text=f'{name} — R² = {r2:.4f}',
                       font=dict(size=13, color='#111110',
                                 family='Playfair Display, Georgia, serif')),
        )
        st.plotly_chart(fig_pva, use_container_width=True)

st.markdown(FOOTER_HTML, unsafe_allow_html=True)
