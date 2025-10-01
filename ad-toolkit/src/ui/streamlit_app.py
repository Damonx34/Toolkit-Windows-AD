# src/ui/streamlit_app.py
import sys
from pathlib import Path
import json
import tempfile
import streamlit as st

# make src importable
ROOT = Path(__file__).resolve().parents[2]
src_path = ROOT / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from enumeration.ldap_enum import ldap_enumerate
from checks.config_checks import run_all_checks
from reporting.report import save_json_report, save_html_report

# Page config
st.set_page_config(page_title="AD Toolkit - DAMONX", layout="wide", initial_sidebar_state="collapsed")

# ---- CSS hacker / Matrix style ----
st.markdown("""
<style>
/* page background and font */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #000000;
    color: #00FF41;
    font-family: "Courier New", Courier, monospace;
}

/* big title glow */
.matrix-title {
    font-size: 48px;
    font-weight: 900;
    color: #00FF41;
    text-shadow: 0 0 8px rgba(0,255,65,0.85), 0 0 20px rgba(0,255,65,0.25);
    margin-bottom: 4px;
}

/* subtitle */
.matrix-sub {
    font-size: 14px;
    color: rgba(0,255,65,0.7);
    margin-bottom: 18px;
}

/* container box */
.matrix-box {
    background: rgba(0,0,0,0.75);
    border: 1px solid rgba(0,255,65,0.1);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
}

/* inputs and buttons */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, [data-baseweb="button"] {
    background-color: rgba(0,0,0,0.3);
    color: #b9ffbf;
    border: 1px solid rgba(0,255,65,0.1);
}

/* small helper */
.matrix-small { color: rgba(0,255,65,0.6); font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown("""
<div class="matrix-title">CRÉÉ PAR : DAMONX</div>
<div class="matrix-sub">AD Toolkit — enum & checks · hackers éthiques only</div>
""", unsafe_allow_html=True)

# ---- Main UI container ----
st.markdown('<div class="matrix-box">', unsafe_allow_html=True)

with st.form("enum_form"):
    cols = st.columns([2,2,1])
    with cols[0]:
        target = st.text_input("Target (domain / DC hostname / IP)", value="", placeholder="ex: dc01.corp.lab ou 10.0.2.15")
        user = st.text_input("Bind user (DOMAIN\\user or user@domain)", value="", help="optionnel")
    with cols[1]:
        password = st.text_input("Bind password", value="", type="password", help="optionnel")
        out_html = st.text_input("Save HTML report as", value="report.html")
    with cols[2]:
        run = st.form_submit_button("▶ RUN", help="Lancer l'énumération")
        download_now = st.form_submit_button("⤓ Télécharger dernier JSON")

st.markdown('</div>', unsafe_allow_html=True)

# storage for last JSON temp file path
if "last_json" not in st.session_state:
    st.session_state["last_json"] = None

if run:
    if not target:
        st.error("Renseigne un target (ex: dc01.corp.lab ou 10.0.2.15).")
    else:
        st.info(f"Lancement de l'énum sur **{target}**")
        with st.spinner("Exécution..."):
            try:
                results = ldap_enumerate(target, user or None, password or None)
                findings = run_all_checks(results)
                results["findings"] = findings

                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
                save_json_report(results, tmp.name)
                st.session_state["last_json"] = tmp.name

                try:
                    save_html_report(results, out_html)
                    st.success(f"HTML report written to {out_html}")
                except Exception as e:
                    st.warning(f"Impossible d'écrire le HTML: {e}")

                st.markdown('<div class="matrix-box">', unsafe_allow_html=True)
                st.subheader("Résultats (extrait)")
                users = results.get("ldap", {}).get("users", [])
                if users:
                    st.table([{k:v for k,v in u.items()} for u in users])
                else:
                    st.info("Aucun utilisateur listé (LDAP non reachable ou bind anonym non autorisé).")

                st.subheader("Findings")
                if findings:
                    st.table(findings)
                else:
                    st.success("Aucun finding automatique détecté.")
                st.markdown('</div>', unsafe_allow_html=True)

                st.success(f"JSON sauvegardé: {tmp.name}")
                with open(tmp.name,"rb") as f:
                    st.download_button("Télécharger results.json", f, file_name="results.json", mime="application/json")
            except Exception as e:
                st.error(f"Erreur pendant l'énumération : {e}")

if download_now and st.session_state.get("last_json"):
    try:
        with open(st.session_state["last_json"], "rb") as f:
            st.download_button("Télécharger results.json", f, file_name="results.json", mime="application/json")
    except Exception as e:
        st.warning(f"Impossible de fournir le fichier: {e}")

st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
st.markdown('<div class="matrix-small">Note: utiliser uniquement dans un cadre légal et autorisé. Aucun acte illégal n\'est toléré.</div>', unsafe_allow_html=True)
