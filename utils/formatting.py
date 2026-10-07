"""SHIFT Commercial Advisory look: Foundation Black #000, Precision White #FFF, Pivot Gray #737373."""
import html

LOGO = ('<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#fff"/>'
        '<rect x="7" y="10" width="19" height="8" rx="4" fill="#000"/><rect x="14" y="22" width="19" height="8" rx="4" fill="#000"/>'
        '<rect x="14" y="10" width="12" height="8" rx="4" fill="none" stroke="#737373" stroke-width="1.5"/></svg>')

HEADER = f"""<div class="shift-bar"><div class="brand">{LOGO}<div><div class="wm">SHIFT</div>
<div class="desc">COMMERCIAL ADVISORY</div></div></div><div class="tag">Strict Rules. Flexible Results</div></div>
<h1 class="ttl">Vendor Sourcing &amp; Risk Check</h1>
<div class="sub">Find suppliers, then screen them. Preliminary supplier due diligence.</div>"""

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,900&display=swap');
html, body, [class*="css"], .stApp {font-family:'Inter','Helvetica Neue',Arial,sans-serif;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:1rem; max-width:1100px;}
.shift-bar {background:#000; color:#fff; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; margin:0 0 18px;}
.brand {display:flex; gap:12px; align-items:center;}
.wm {font-weight:900; font-style:italic; font-size:1.5rem; letter-spacing:-1px; line-height:1;}
.desc {font-size:.55rem; letter-spacing:.38em; color:#737373; margin-top:3px;}
.tag {font-size:.78rem; color:#fff; letter-spacing:.5px;}
.ttl {font-weight:800; letter-spacing:-.5px; font-size:1.9rem; margin:0; padding:0;}
.sub {color:#737373; margin:2px 0 14px;}
.stButton>button, .stFormSubmitButton>button {background:#000; color:#fff; border-radius:0; border:1px solid #000; font-weight:700; letter-spacing:1px;}
.stButton>button:hover, .stFormSubmitButton>button:hover {background:#fff; color:#000; border:1px solid #000;}
.stButton>button:disabled {background:#d9d9d9; color:#737373; border-color:#d9d9d9;}
div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:0;}
.sec {border-bottom:3px solid #000; font-weight:800; text-transform:uppercase; letter-spacing:1px; padding-bottom:4px; margin:1.4rem 0 .7rem; font-size:.95rem;}
.tag-pill {display:inline-block; border:1px solid #000; padding:1px 8px; font-size:.7rem; font-weight:700; letter-spacing:1px;}
.tag-pill.mock {background:#000; color:#fff;}
.meta {color:#737373; font-size:.82rem;}
.news {border-bottom:1px solid #ddd; padding:.45rem 0;}
.news a {color:#000; font-weight:600; text-decoration:underline;}
.warn {background:#f2f2f2; border-left:4px solid #000; padding:.5rem .8rem; font-size:.85rem; margin:.5rem 0;}
.rk {display:inline-block; padding:1px 10px; font-weight:800; letter-spacing:1px; border:2px solid #000; font-size:.8rem;}
.rk.LOW {background:#fff; color:#000;} .rk.MEDIUM {background:#737373; color:#fff; border-color:#737373;} .rk.HIGH {background:#000; color:#fff;}
.cmpwrap {overflow-x:auto;}
.cmp {width:100%; border-collapse:collapse; font-size:.9rem;}
.cmp th {text-align:left; border-bottom:2px solid #000; padding:6px 8px; font-size:.75rem; text-transform:uppercase; letter-spacing:1px;}
.cmp td {border-bottom:1px solid #ddd; padding:8px;}
.foot {margin-top:2rem; padding-top:.6rem; border-top:1px solid #ddd; color:#737373; font-size:.78rem;}
</style>"""


def esc(v) -> str:
    return html.escape(str(v)) if v not in (None, "") else "—"


def section(title: str) -> str:
    return f'<div class="sec">{esc(title)}</div>'
