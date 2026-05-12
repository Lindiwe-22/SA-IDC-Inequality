GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&display=swap');

/* ── Base ── */
[data-testid="stAppViewContainer"] { background: #FAFAF8 !important; }
[data-testid="stSidebar"] { background: #F1EFE8 !important; border-right: 0.5px solid #D3D1C7 !important; }
[data-testid="stSidebar"] * { color: #2C2C2A !important; font-family: 'Source Serif 4', Georgia, serif !important; }
[data-testid="stSidebar"] .stMarkdown p { font-size: 13px !important; color: #5F5E5A !important; line-height: 1.7 !important; }
[data-testid="stSidebar"] hr { border-color: #D3D1C7 !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; max-width: 900px !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; color: #111110 !important; }
p, li { font-family: 'Source Serif 4', Georgia, serif; color: #2C2C2A; font-size: 15px; line-height: 1.75; }

/* ── Landing masthead ── */
.masthead { border-bottom: 3px solid #111110; padding-bottom: 18px; margin-bottom: 0; }
.masthead-label { font-family: 'Source Serif 4', serif; font-size: 11px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 10px; }
.masthead-title { font-family: 'Playfair Display', Georgia, serif; font-size: 54px; font-weight: 900; line-height: 1.0; color: #111110; letter-spacing: -0.02em; }
.masthead-title em { font-style: italic; color: #BA7517; }
.masthead-deck { font-family: 'Source Serif 4', serif; font-size: 17px; font-weight: 300; line-height: 1.75; color: #444441; margin-top: 14px; max-width: 680px; border-left: 3px solid #BA7517; padding-left: 16px; }
.byline-row { display: flex; align-items: center; justify-content: space-between; padding: 11px 0; border-top: 0.5px solid #B4B2A9; border-bottom: 0.5px solid #B4B2A9; margin-top: 16px; flex-wrap: wrap; gap: 8px; }
.byline { font-size: 12px; color: #5F5E5A; letter-spacing: 0.04em; font-style: italic; font-family: 'Source Serif 4', serif; }
.byline strong { font-style: normal; font-weight: 600; color: #2C2C2A; }

/* ── Inner page masthead ── */
.page-masthead { border-bottom: 2px solid #111110; padding-bottom: 14px; margin-bottom: 28px; }
.page-eyebrow { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: #888780; margin-bottom: 8px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 900; line-height: 1.1; color: #111110; letter-spacing: -0.01em; }
.page-title em { font-style: italic; color: #BA7517; }
.page-deck { font-family: 'Source Serif 4', serif; font-size: 15px; font-weight: 300; line-height: 1.75; color: #444441; margin-top: 10px; border-left: 3px solid #BA7517; padding-left: 14px; max-width: 660px; }

/* ── Section rules ── */
.section-rule { display: flex; align-items: center; gap: 14px; margin: 32px 0 20px 0; }
.section-rule-label { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: #888780; white-space: nowrap; }
.section-rule-line { flex: 1; height: 0.5px; background: #D3D1C7; }

/* ── Stat strip ── */
.stat-strip { display: grid; border: 0.5px solid #D3D1C7; border-right: none; margin-bottom: 28px; }
.stat-strip-4 { grid-template-columns: repeat(4, 1fr); }
.stat-strip-3 { grid-template-columns: repeat(3, 1fr); }
.stat-strip-2 { grid-template-columns: repeat(2, 1fr); }
.stat-cell { padding: 18px 16px; border-right: 0.5px solid #D3D1C7; }
.stat-cell.alert { border-top: 2px solid #C53030; }
.stat-cell.warn  { border-top: 2px solid #BA7517; }
.stat-cell.ok    { border-top: 2px solid #0F6E56; }
.stat-cell.info  { border-top: 2px solid #185FA5; }
.stat-number { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 700; line-height: 1; margin-bottom: 5px; color: #111110; }
.stat-number.red   { color: #A32D2D; }
.stat-number.amber { color: #BA7517; }
.stat-number.teal  { color: #0F6E56; }
.stat-number.blue  { color: #185FA5; }
.stat-desc { font-size: 11px; color: #5F5E5A; line-height: 1.55; font-family: 'Source Serif 4', serif; }

/* ── Two-col info grid ── */
.info-grid { display: grid; grid-template-columns: 1fr 1fr; border: 0.5px solid #D3D1C7; margin-bottom: 28px; }
.info-card { padding: 22px; border-right: 0.5px solid #D3D1C7; }
.info-card:last-child { border-right: none; }
.info-card-label { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 8px; font-family: 'Source Serif 4', serif; }
.info-card-value { font-family: 'Playfair Display', serif; font-size: 40px; font-weight: 700; line-height: 1; margin-bottom: 3px; }
.info-card-value.amber { color: #BA7517; }
.info-card-value.teal  { color: #0F6E56; }
.info-card-sub { font-size: 11px; color: #888780; margin-bottom: 16px; font-family: 'Source Serif 4', serif; }
.info-card-table { width: 100%; border-collapse: collapse; }
.info-card-table tr { border-top: 0.5px solid #F1EFE8; }
.info-card-table td { font-size: 12px; padding: 6px 0; color: #5F5E5A; font-family: 'Source Serif 4', serif; }
.info-card-table td:last-child { text-align: right; font-weight: 600; color: #2C2C2A; }
.info-card-table .no  { color: #A32D2D !important; }
.info-card-table .yes { color: #0F6E56 !important; }

/* ── Findings grid ── */
.findings-grid { display: grid; grid-template-columns: 1fr 1fr; margin-bottom: 28px; }
.finding-cell { padding: 20px; border: 0.5px solid #D3D1C7; margin: -0.5px 0 0 -0.5px; }
.finding-num { font-family: 'Playfair Display', serif; font-size: 11px; font-weight: 700; color: #D3D1C7; letter-spacing: 0.12em; margin-bottom: 7px; }
.finding-head { font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 700; color: #111110; line-height: 1.35; margin-bottom: 7px; }
.finding-head.critical { color: #A32D2D; }
.finding-body { font-size: 12px; color: #5F5E5A; line-height: 1.65; font-family: 'Source Serif 4', serif; }
.finding-stat { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: #BA7517; margin-top: 10px; }

/* ── Callout boxes ── */
.callout { padding: 15px 20px; margin: 20px 0; border-left: 3px solid #BA7517; background: #FDF6E8; }
.callout p { font-size: 14px; color: #5C3A06; line-height: 1.7; margin: 0; font-family: 'Source Serif 4', serif; }
.callout.alert { border-left-color: #C53030; background: #FDF0F0; }
.callout.alert p { color: #7A1F1F; }
.callout.ok { border-left-color: #0F6E56; background: #E8F5EF; }
.callout.ok p { color: #084D3A; }
.callout.info { border-left-color: #185FA5; background: #E8F1FB; }
.callout.info p { color: #0C3F72; }

/* ── Metric cards (original app style, redesigned) ── */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; border: 0.5px solid #D3D1C7; border-right: none; margin: 20px 0 28px 0; }
.metric-card { padding: 18px 16px; border-right: 0.5px solid #D3D1C7; background: #FAFAF8; }
.metric-card.gold  { border-top: 2px solid #BA7517; }
.metric-card.teal  { border-top: 2px solid #0F6E56; }
.metric-card.red   { border-top: 2px solid #C53030; }
.metric-card.blue  { border-top: 2px solid #185FA5; }
.metric-label { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 7px; font-family: 'Source Serif 4', serif; }
.metric-value { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #111110; line-height: 1; margin-bottom: 5px; }
.metric-value.red   { color: #A32D2D; }
.metric-value.amber { color: #BA7517; }
.metric-value.teal  { color: #0F6E56; }
.metric-sub { font-size: 11px; color: #888780; line-height: 1.5; font-family: 'Source Serif 4', serif; }

/* ── Nav strip ── */
.nav-strip { background: #3A3A38; padding: 14px 20px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 28px; }
.nav-strip-label { font-size: 10px; color: #B4B2A9; letter-spacing: 0.18em; text-transform: uppercase; margin-right: 6px; font-family: 'Source Serif 4', serif; }
.nav-item { font-size: 11px; color: #111110; background: #FAFAF8; font-family: 'Source Serif 4', serif; font-weight: 600; letter-spacing: 0.04em; padding: 5px 11px; }

/* ── Acknowledgement + footer ── */
.ack-note { background: #FDF6E8; border-left: 3px solid #BA7517; padding: 13px 18px; margin-top: 22px; font-size: 12px; color: #5C3A06; line-height: 1.65; font-family: 'Source Serif 4', serif; }
.footer-strip { border-top: 0.5px solid #D3D1C7; padding-top: 16px; margin-top: 28px; font-size: 11px; color: #888780; line-height: 1.75; font-family: 'Source Serif 4', serif; }

/* ── Section divider ── */
.rule { border: none; border-top: 0.5px solid #D3D1C7; margin: 32px 0; }

/* ── Plotly chart wrapper ── */
.chart-caption { font-size: 12px; color: #888780; margin-top: -8px; margin-bottom: 20px; font-style: italic; font-family: 'Source Serif 4', serif; border-left: 2px solid #D3D1C7; padding-left: 10px; }
</style>
"""

PLOTLY_LAYOUT = dict(
    plot_bgcolor="#FAFAF8",
    paper_bgcolor="#FAFAF8",
    font=dict(family="Source Serif 4, Georgia, serif", color="#2C2C2A"),
    margin=dict(t=24, b=24, l=20, r=20),
    xaxis=dict(gridcolor="#EDECEA", zeroline=False),
    yaxis=dict(gridcolor="#EDECEA", zeroline=False),
)

FOOTER_HTML = """
<div class="footer-strip">
  Data: IDC Funding Dashboard &nbsp;·&nbsp; NEF Parliamentary Question PQ705 (dtic.gov.za)
  &nbsp;·&nbsp; Stats SA QLFS Q3 2025<br>
  Analysis &amp; code &copy; 2025 Lindiwe Songelwa &nbsp;·&nbsp; Open source
  &nbsp;·&nbsp; Built with Python, Streamlit &amp; Plotly
</div>
"""

def section_rule(label):
    return f"""<div class="section-rule">
  <span class="section-rule-label">{label}</span>
  <div class="section-rule-line"></div>
</div>"""

def callout(text, variant=""):
    return f'<div class="callout {variant}"><p>{text}</p></div>'

def page_masthead(eyebrow, title, deck):
    return f"""<div class="page-masthead">
  <div class="page-eyebrow">{eyebrow}</div>
  <div class="page-title">{title}</div>
  <div class="page-deck">{deck}</div>
</div>"""

def sidebar_content():
    import streamlit as st
    with st.sidebar:
        st.markdown("**Who Really Gets the Money?**")
        st.markdown("---")
        st.markdown(
            "A public interest analysis of South African development finance. "
            "Examining R69.5 billion of public money across the IDC and NEF."
        )
        st.markdown("---")
        st.markdown("**Data Sources**")
        st.markdown(
            "- IDC Funding Dashboard (FY2017–2025)\n"
            "- NEF via PQ705, dtic.gov.za\n"
            "- Stats SA QLFS Q3 2025"
        )
        st.markdown("---")
        st.caption("Analysis by Lindiwe Songelwa")

def apply_plotly_theme(fig, height=420):
    fig.update_layout(
        plot_bgcolor="#FAFAF8",
        paper_bgcolor="#FAFAF8",
        font=dict(family="Source Serif 4, Georgia, serif", color="#2C2C2A"),
        margin=dict(t=24, b=24, l=20, r=20),
        height=height,
    )
    fig.update_xaxes(gridcolor="#EDECEA", zeroline=False)
    fig.update_yaxes(gridcolor="#EDECEA", zeroline=False)
    return fig
