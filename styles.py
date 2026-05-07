GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,400&display=swap');

[data-testid="stAppViewContainer"] { background: #FAFAF8; }
[data-testid="stSidebar"] { background: #F1EFE8; border-right: 0.5px solid #D3D1C7; }
[data-testid="stSidebar"] * { color: #2C2C2A !important; }
[data-testid="stSidebar"] .stMarkdown p { font-family: 'Source Serif 4', Georgia, serif; font-size: 13px; color: #5F5E5A !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 860px; }

h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif; color: #111110; }
p, li { font-family: 'Source Serif 4', Georgia, serif; color: #2C2C2A; font-size: 15px; line-height: 1.75; }

.page-masthead { border-bottom: 2px solid #111110; padding-bottom: 14px; margin-bottom: 28px; }
.page-section-label { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #888780; margin-bottom: 8px; }
.page-title { font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 900; line-height: 1.1; color: #111110; letter-spacing: -0.01em; }
.page-title em { font-style: italic; color: #BA7517; }
.page-deck { font-family: 'Source Serif 4', serif; font-size: 15px; font-weight: 300; line-height: 1.7; color: #444441; margin-top: 10px; border-left: 3px solid #BA7517; padding-left: 14px; max-width: 640px; }

.section-rule { display: flex; align-items: baseline; gap: 14px; margin: 28px 0 18px 0; }
.section-label { font-family: 'Source Serif 4', serif; font-size: 10px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: #888780; white-space: nowrap; }
.section-line { flex: 1; height: 0.5px; background: #D3D1C7; }

.stat-strip { display: grid; border: 0.5px solid #D3D1C7; border-right: none; margin-bottom: 28px; }
.stat-strip-4 { grid-template-columns: repeat(4, 1fr); }
.stat-strip-3 { grid-template-columns: repeat(3, 1fr); }
.stat-strip-2 { grid-template-columns: repeat(2, 1fr); }
.stat-cell { padding: 16px 14px; border-right: 0.5px solid #D3D1C7; }
.stat-cell.alert { border-top: 2px solid #E24B4A; }
.stat-cell.warn  { border-top: 2px solid #BA7517; }
.stat-cell.ok    { border-top: 2px solid #0F6E56; }
.stat-cell.info  { border-top: 2px solid #185FA5; }
.stat-number { font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 700; color: #111110; line-height: 1; margin-bottom: 4px; }
.stat-number.red   { color: #A32D2D; }
.stat-number.amber { color: #BA7517; }
.stat-number.teal  { color: #0F6E56; }
.stat-number.blue  { color: #185FA5; }
.stat-desc { font-size: 11px; color: #5F5E5A; line-height: 1.5; }

.two-col-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 0.5px solid #D3D1C7; margin-bottom: 28px; }
.grid-card { padding: 20px; border-right: 0.5px solid #D3D1C7; }
.grid-card:last-child { border-right: none; }
.grid-card-label { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: #888780; margin-bottom: 8px; }
.grid-card-amount { font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 700; line-height: 1; margin-bottom: 2px; }
.grid-card-amount.amber { color: #BA7517; }
.grid-card-amount.teal  { color: #0F6E56; }
.grid-card-period { font-size: 11px; color: #888780; margin-bottom: 14px; }
.grid-table { width: 100%; border-collapse: collapse; }
.grid-table tr { border-top: 0.5px solid #F1EFE8; }
.grid-table td { font-size: 12px; padding: 5px 0; color: #5F5E5A; }
.grid-table td:last-child { text-align: right; font-weight: 600; color: #2C2C2A; }
.grid-table .no  { color: #A32D2D !important; }
.grid-table .yes { color: #0F6E56 !important; }

.findings-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; margin-bottom: 28px; }
.finding-item { padding: 18px; border: 0.5px solid #D3D1C7; margin: -0.5px 0 0 -0.5px; }
.finding-number { font-family: 'Playfair Display', serif; font-size: 11px; font-weight: 700; color: #D3D1C7; letter-spacing: 0.1em; margin-bottom: 6px; }
.finding-title { font-family: 'Playfair Display', serif; font-size: 14px; font-weight: 700; color: #111110; line-height: 1.35; margin-bottom: 6px; }
.finding-title.critical { color: #A32D2D; }
.finding-desc { font-size: 12px; color: #5F5E5A; line-height: 1.6; }
.finding-stat { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; color: #BA7517; margin-top: 8px; }

.callout { padding: 14px 18px; margin: 18px 0; border-left: 3px solid #BA7517; background: #FAEEDA; }
.callout p { font-size: 14px; color: #633806; line-height: 1.65; margin: 0; }
.callout.critical { border-left-color: #E24B4A; background: #FCEBEB; }
.callout.critical p { color: #791F1F; }
.callout.ok { border-left-color: #0F6E56; background: #E1F5EE; }
.callout.ok p { color: #085041; }
.callout.info { border-left-color: #185FA5; background: #E6F1FB; }
.callout.info p { color: #0C447C; }

.data-note { font-size: 11px; color: #888780; border-top: 0.5px solid #D3D1C7; padding-top: 10px; margin-top: 20px; line-height: 1.6; }

.footer-strip { border-top: 0.5px solid #D3D1C7; padding-top: 16px; margin-top: 28px; font-size: 11px; color: #888780; line-height: 1.7; }
.footer-strip a { color: #BA7517; }
</style>
"""

PAGE_FOOTER = """
<div class="footer-strip">
  Data: IDC Funding Dashboard &nbsp;·&nbsp; NEF Parliamentary Question PQ705 (dtic.gov.za)
  &nbsp;·&nbsp; Stats SA QLFS Q3 2025<br>
  Analysis &amp; code &copy; 2025 Lindiwe Songelwa &nbsp;·&nbsp; Open source
  &nbsp;·&nbsp; Built with Python, Streamlit &amp; Plotly
</div>
"""

def page_masthead(section_label, title, deck):
    return f"""
<div class="page-masthead">
  <div class="page-section-label">{section_label}</div>
  <div class="page-title">{title}</div>
  <div class="page-deck">{deck}</div>
</div>
"""

def section_rule(label):
    return f"""
<div class="section-rule">
  <span class="section-label">{label}</span>
  <div class="section-line"></div>
</div>
"""

def callout(text, variant=""):
    return f'<div class="callout {variant}"><p>{text}</p></div>'

def data_note(text):
    return f'<div class="data-note">{text}</div>'
