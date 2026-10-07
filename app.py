"""SHIFT Vendor Sourcing & Risk Check: search, shortlist, then screen."""
import hmac
import os

import streamlit as st

from data.sectors import SECTORS
from services.search import find_vendors
from services.screening import risk_for_many
from services.sector import sector_of
from utils.formatting import CSS, HEADER, esc, section
from utils.helpers import get_api_key

st.set_page_config(page_title="SHIFT | Vendor Sourcing & Risk Check", layout="wide",
                   initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(HEADER, unsafe_allow_html=True)


def _secret(name: str):
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def gate() -> None:
    """Optional shared password (APP_PASSWORD in secrets or environment)."""
    pw = _secret("APP_PASSWORD") or os.environ.get("APP_PASSWORD")
    if not pw or st.session_state.get("authed"):
        return
    entered = st.text_input("Password", type="password")
    if entered and hmac.compare_digest(entered.encode(), str(pw).encode()):
        st.session_state["authed"] = True
        st.rerun()
    if entered:
        st.error("Wrong password.")
    st.stop()


gate()

with st.sidebar:
    st.header("Configuration")
    key_in = st.text_input("Google Places API Key", type="password", help="Optional. Empty = free OpenStreetMap search.")
    st.subheader("Screening Scope")
    st.markdown("- Vendor search and profile\n- Adverse media\n- Preliminary risk indicator")
    st.caption("This tool provides preliminary screening only. It does not replace formal due diligence, "
               "legal review, sanctions screening, or financial analysis.")


@st.cache_data(ttl=3600, show_spinner=False)
def cached_search(q: str, loc: str, key: str | None):
    return find_vendors(q, loc or None, key)


@st.cache_data(ttl=600, show_spinner=False)
def cached_risk(names: tuple) -> dict:
    """10-minute cache: avoids repeat calls but keeps news current."""
    return risk_for_many(list(names))


# ---------- 1. Search ----------
st.markdown(section("1. Search"), unsafe_allow_html=True)
with st.form("search"):
    q = st.text_input("Company name, or what you are looking for",
                      placeholder="PT Astra International  |  percetakan packaging")
    city = st.text_input("City / location (optional)", placeholder="Bekasi")
    submitted = st.form_submit_button("SEARCH", use_container_width=True)

if submitted:
    if not q.strip():
        st.warning("Enter a company name or a category to search.")
    else:
        with st.spinner("Searching map data..."):
            res, warn = cached_search(q.strip(), city.strip(), get_api_key(key_in, st.secrets))
        for k in [k for k in st.session_state if k.startswith(("sel_", "sec_"))]:
            del st.session_state[k]
        st.session_state.update(results=list(res), warn=warn, query=q.strip(), risk=None)

results = st.session_state.get("results")
if results is not None:
    if st.session_state.get("warn"):
        st.markdown(f'<div class="warn">{esc(st.session_state["warn"])}</div>', unsafe_allow_html=True)

    with st.expander("Not on the map? Add a vendor manually"):
        with st.form("manual", clear_on_submit=True):
            m_name = st.text_input("Company name")
            m_city = st.text_input("City")
            m_sec = st.selectbox("Sector", SECTORS, index=len(SECTORS) - 1)
            if st.form_submit_button("ADD TO LIST") and m_name.strip():
                vid = f"manual-{len(results)}"
                results.append({"id": vid, "name": m_name.strip(), "rating": None, "total_reviews": None,
                                "address": m_city.strip() or None, "phone": None, "website": None,
                                "business_status": None, "verification_status": "Manual entry",
                                "maps_url": None, "primary_type": None, "types": [], "source": "Manual entry"})
                st.session_state[f"sec_{vid}"] = m_sec

    # ---------- 2. Shortlist ----------
    st.markdown(section("2. Shortlist"), unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    has_rating = any(v["rating"] is not None for v in results)
    min_rating = f1.slider("Minimum rating", 0.0, 5.0, 0.0, 0.1) if has_rating else 0.0
    only_op = f2.checkbox("Operational only", value=False)
    shown = [v for v in results
             if (v["rating"] is None or v["rating"] >= min_rating) and (not only_op or v["business_status"] in (None, "OPERATIONAL"))]
    st.caption(f"{len(shown)} of {len(results)} result(s). Tick the vendors to screen.")

    for v in shown:
        st.session_state.setdefault(f"sec_{v['id']}", sector_of(v)[0])
        mock = v["source"] == "Mock Data"
        with st.container(border=True):
            st.checkbox(v["name"], key=f"sel_{v['id']}")
            tag = "MOCK" if mock else v["source"].upper()
            bits = [f"Rating {v['rating']} ({v['total_reviews']} reviews)" if v["rating"] is not None else None,
                    v["business_status"], v["address"]]
            st.markdown(f'<span class="tag-pill {"mock" if mock else ""}">{esc(tag)}</span> '
                        f'<span class="meta">{esc(" · ".join(b for b in bits if b))}</span>', unsafe_allow_html=True)
            if v["website"]:
                st.markdown(f'<a class="meta" href="{esc(v["website"])}" target="_blank" rel="noopener">{esc(v["website"])}</a>',
                            unsafe_allow_html=True)
            st.selectbox("Sector", SECTORS, key=f"sec_{v['id']}",
                         help=f"Default from Google Maps type: {v.get('primary_type') or 'none'}. Change if wrong.")

    selected = [v for v in shown if st.session_state.get(f"sel_{v['id']}")]
    if st.button(f"RUN RISK CHECK ({len(selected)})", disabled=not selected, use_container_width=True):
        names = {v["id"]: (st.session_state.get("query", v["name"]) if v["source"] == "Mock Data" else v["name"])
                 for v in selected}
        with st.spinner("Checking Google News... Assessing preliminary risk..."):
            out = cached_risk(tuple(dict.fromkeys(names.values())))
        st.session_state["risk"] = [{"v": v, "sector": st.session_state[f"sec_{v['id']}"],
                                     "res": out[names[v["id"]]]} for v in selected]

# ---------- 3. Risk ----------
rows = st.session_state.get("risk")
if rows:
    st.markdown(section("3. Preliminary Risk Assessment"), unsafe_allow_html=True)
    st.markdown('<div class="warn">Evidence, finding, risk, procurement implication, recommended action. '
                'Search results are based on the vendor name and may include unrelated entities. '
                'Confirm company identity before relying on an article.</div>', unsafe_allow_html=True)
    body = "".join(
        f'<tr><td><b>{esc(r["v"]["name"])}</b></td><td>{esc(r["sector"])}</td>'
        f'<td>{esc(r["v"]["rating"])}</td><td><span class="rk {r["res"]["risk"]["level"]}">'
        f'{r["res"]["risk"]["level"]}</span></td><td>{len(r["res"]["risk"]["flagged"])}</td>'
        f'<td>{len(r["res"]["articles"])}</td></tr>' for r in rows)
    st.markdown('<div class="cmpwrap"><table class="cmp"><tr><th>Vendor</th><th>Sector</th><th>Rating</th>'
                f'<th>Risk</th><th>Flagged</th><th>Articles</th></tr>{body}</table></div>', unsafe_allow_html=True)
    st.caption("Sector is context only and never changes the risk level.")

    for r in rows:
        res, risk = r["res"], r["res"]["risk"]
        with st.expander(f'{r["v"]["name"]}  ·  {risk["level"]}'):
            st.markdown("**Key findings**")
            st.markdown("\n".join(f"- {x}" for x in risk["findings"]))
            st.markdown("**Recommended procurement action**")
            st.markdown(f'<div class="warn">{esc(risk["action"])}</div>', unsafe_allow_html=True)
            st.caption("Source: Google News RSS")
            if res["news_error"]:
                st.error(res["news_error"])
            elif not res["articles"]:
                st.info("No recent articles found for this name.")
            for a in res["articles"]:
                st.markdown(f'<div class="news"><a href="{esc(a["link"])}" target="_blank" rel="noopener">'
                            f'{esc(a["title"])}</a><br><span class="meta">{esc(a["source"])} · {esc(a["published"])}'
                            f'</span></div>', unsafe_allow_html=True)
    st.markdown("**Screening limitations**")
    st.markdown("- News coverage may be incomplete.\n- Similar company names may produce unrelated results.\n"
                "- Absence of adverse media does not indicate absence of risk.\n"
                "- Results require human verification before procurement decisions.")

st.markdown('<div class="foot">SHIFT Commercial Advisory · Preliminary screening only. Not compliance clearance.</div>',
            unsafe_allow_html=True)
