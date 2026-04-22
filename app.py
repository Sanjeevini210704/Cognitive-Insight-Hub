import streamlit as st
import pandas as pd
from datetime import datetime

from cogni_scan.auth import ensure_seed_users, login, register
from cogni_scan.db import analyses, users
from cogni_scan.analyzer import analyze
from cogni_scan.charts import (
    radar_chart, category_donut, emotional_trend_bar,
    engagement_area, risk_bar,
)
from cogni_scan.styles import CSS

st.set_page_config(page_title="CogniScan — Cognitive Insight Hub",
                   page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)

ensure_seed_users()

if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "landing"
if "current_analysis" not in st.session_state: st.session_state.current_analysis = None


def goto(page: str):
    st.session_state.page = page
    st.rerun()


def logout():
    st.session_state.user = None
    st.session_state.current_analysis = None
    goto("landing")


LOGO = """
<div class="cs-logo">
  <div class="mark"><div class="dot"></div></div>
  <span>CogniScan</span>
</div>
"""


def nav_public():
    c = st.container()
    with c:
        st.markdown('<div class="cs-nav">' + LOGO + '<div></div></div>', unsafe_allow_html=True)
        cols = st.columns([6, 1, 1])
        with cols[1]:
            if st.button("Sign In", key="nav_signin", type="secondary"):
                goto("login")
        with cols[2]:
            if st.button("Get Started", key="nav_start"):
                goto("login")


def nav_user(tag: str):
    st.markdown(
        '<div class="cs-nav">' + LOGO +
        f'<span class="cs-tag">{tag}</span><div style="flex:1"></div></div>',
        unsafe_allow_html=True
    )
    cols = st.columns([4, 1, 1, 1, 1])
    if st.session_state.user["role"] == "user":
        with cols[1]:
            if st.button("History", key="nav_hist", type="secondary"): goto("history")
        with cols[2]:
            if st.button("New Diagnostic", key="nav_new", type="secondary"):
                st.session_state.current_analysis = None; goto("dashboard")
        with cols[3]:
            if st.button("Print", key="nav_print", type="secondary"):
                st.components.v1.html("<script>window.parent.print()</script>", height=0)
        with cols[4]:
            if st.button("Logout", key="nav_logout", type="secondary"): logout()
    else:
        with cols[3]:
            if st.button("Dashboard", key="nav_admin_d", type="secondary"): goto("admin_dashboard")
        with cols[4]:
            if st.button("Logout", key="nav_logout", type="secondary"): logout()


# ---------- Landing ----------
def page_landing():
    nav_public()

    st.markdown(
        """
        <div class="cs-hero" style="text-align:center; padding: 30px 0 20px;">
          <div class="cs-badge"><span class="pulse"></span>COGNITIVE HEALTH ANALYSIS API v2.0</div>
          <h1>Quantify the psychological impact of <span class="grad">your digital diet.</span></h1>
          <p>CogniScan uses behavioral modeling to analyze your social media consumption patterns,
          identifying risk factors for anxiety, dopamine overstimulation, and information overload.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c = st.columns([2, 1, 1, 2])
    with c[1]:
        if st.button("Run Diagnostic", key="hero_run"): goto("login")
    with c[2]:
        if st.button("View Demo Report", key="hero_demo", type="secondary"): goto("login")

    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3, gap="large")
    steps = [
        ("01", "Input Data", "Securely paste your recent consumption history or export files from major platforms."),
        ("02", "AI Processing", "Our engine maps content categories against cognitive load models, detecting fragmented attention and emotional triggers."),
        ("03", "Clinical Report", "Receive a detailed breakdown of cognitive metrics, risk factors, and actionable preventive measures."),
    ]
    for col, (n, t, d) in zip([s1, s2, s3], steps):
        col.markdown(
            f'<div class="cs-step"><div class="num">{n}</div>'
            f'<h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True
        )

    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center; margin-bottom: 26px;">'
        '<h2 style="font-size:32px; font-weight:700; margin:0 0 8px;">Precision insights.</h2>'
        '<p style="color:var(--muted); max-width:520px; margin:0 auto;">'
        'Our dashboard translates chaotic social feeds into structured, understandable metrics.</p>'
        '</div>', unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cs-window">
          <div class="cs-window-bar">
            <div class="cs-dot r"></div><div class="cs-dot y"></div><div class="cs-dot g"></div>
            <div class="cs-window-url">cogniscan.app/report/demo</div>
          </div>
          <div style="padding: 28px; display:grid; grid-template-columns: 1fr 1fr; gap: 28px;">
            <div>
              <div style="color:var(--muted); font-family:'Space Mono',monospace; font-size:11px; text-transform:uppercase; letter-spacing:.1em;">Overall Risk</div>
              <div style="font-size:54px; font-weight:900; color:var(--destructive); line-height:1;">78.4
                <span style="font-size:18px; color:var(--muted); font-weight:500;">/100</span></div>
              <p style="color:var(--muted); margin:6px 0 18px;">Critical risk of dopamine loop dependency detected.</p>
              <div style="border-top:1px solid var(--border); padding-top:14px;">
                <div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;font-size:13px;"><span>Attention Fragmentation</span><span style="font-family:'Space Mono',monospace;">80%</span></div>
                  <div style="height:6px;background:#1A2148;border-radius:999px;overflow:hidden;margin-top:4px;"><div style="width:80%;height:100%;background:var(--primary);"></div></div></div>
                <div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;font-size:13px;"><span>Anxiety Index</span><span style="font-family:'Space Mono',monospace;">68%</span></div>
                  <div style="height:6px;background:#1A2148;border-radius:999px;overflow:hidden;margin-top:4px;"><div style="width:68%;height:100%;background:var(--primary);"></div></div></div>
                <div><div style="display:flex;justify-content:space-between;font-size:13px;"><span>Social Comparison</span><span style="font-family:'Space Mono',monospace;">56%</span></div>
                  <div style="height:6px;background:#1A2148;border-radius:999px;overflow:hidden;margin-top:4px;"><div style="width:56%;height:100%;background:var(--primary);"></div></div></div>
              </div>
            </div>
            <div style="background:rgba(139,93,219,0.06); border:1px solid var(--border); border-radius:12px; padding:20px;">
              <div style="font-weight:700; margin-bottom:14px;">Recommended Protocol</div>
              <ul style="list-style:none; padding:0; margin:0; color:var(--muted); font-size:13px; line-height:1.7;">
                <li style="margin-bottom:10px;">▸ Implement a 24-hour fast from short-form video content.</li>
                <li style="margin-bottom:10px;">▸ Enable grayscale mode on mobile device after 8 PM.</li>
                <li>▸ Replace infinite scroll platforms with long-form reading.</li>
              </ul>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="cs-foot">'
        '<div>© 2026 CogniScan Analytics. All rights reserved.</div>'
        '<div></div>'
        '</div>', unsafe_allow_html=True
    )
    cols = st.columns([4, 1])
    with cols[1]:
        if st.button("Admin Portal", key="foot_admin", type="secondary"): goto("admin_login")


# ---------- Login ----------
def _login_form(role: str, title: str, subtitle: str):
    nav_public()
    st.markdown('<div style="max-width:480px; margin: 30px auto;">', unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center; margin-bottom:24px;">'
        f'<h2 style="font-size:30px; font-weight:700; letter-spacing:-0.02em; margin:0;">{title}</h2>'
        f'<p style="color:var(--muted); margin-top:6px;">{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["Sign In", "Register"]) if role == "user" else st.tabs(["Sign In"])
    with tabs[0]:
        with st.form(f"login_{role}"):
            email = st.text_input("Email Address", placeholder="patient@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button(
                "Access Records" if role == "user" else "Authorize Clinical Access"
            )
            if submitted:
                u = login(email, password, role)
                if u:
                    st.session_state.user = u
                    goto("admin_dashboard" if role == "admin" else "dashboard")
                else:
                    st.error("Authentication failed. Check your credentials.")

    if role == "user":
        with tabs[1]:
            with st.form("register_user"):
                name = st.text_input("Name")
                email = st.text_input("Email Address", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_pw")
                submitted = st.form_submit_button("Create Account")
                if submitted:
                    if not (name and email and password):
                        st.error("All fields are required.")
                    else:
                        u = register(email, name, password, "user")
                        if u is None: st.error("That email is already registered.")
                        else:
                            st.session_state.user = u; goto("dashboard")

    other = "admin_login" if role == "user" else "login"
    label = "→ Switch to Clinical Admin Login" if role == "user" else "→ Patient Portal Login"
    st.markdown('<div style="text-align:center; margin-top: 18px;">', unsafe_allow_html=True)
    if st.button(label, key=f"switch_{role}", type="secondary"): goto(other)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center; color:var(--muted); font-family:Space Mono,monospace; '
        'font-size:11px; margin-top:18px;">'
        'DEMO &nbsp;·&nbsp; user: demo@cogniscan.ai / demo1234 &nbsp;·&nbsp; '
        'admin: admin@cogniscan.ai / admin1234</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def page_login():
    _login_form("user", "Patient Portal",
                "Sign in to access your cognitive health reports.")


def page_admin_login():
    _login_form("admin", "Clinical Admin Portal",
                "Authorized personnel only.")


# ---------- Analysis result ----------
def render_result(a: dict):
    risk = a["overall_risk_score"]
    risk_cls = "high" if risk >= 6 else "mid" if risk >= 3 else "low"

    left, right = st.columns([3, 1])
    with left:
        platform = a["platform"]
        aid = str(a.get("_id", "000000"))[-6:].zfill(6).upper()
        when = a["created_at"].strftime("%b %d, %Y · %H:%M")
        st.markdown(
            f'<div style="margin-bottom:6px;">'
            f'<span class="cs-pill">{platform} REPORT</span>'
            f'<span class="cs-meta">ID: #{aid} &nbsp;|&nbsp; {when}</span>'
            f'</div>'
            f'<h1 style="font-size:38px; font-weight:800; letter-spacing:-0.02em; margin:6px 0;">'
            f'Clinical Assessment</h1>'
            f'<p style="color:var(--muted); max-width:640px; margin:0;">{a["summary"]}</p>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f'<div class="cs-risk-box">'
            f'<div class="lbl">Overall Risk Score</div>'
            f'<div class="val {risk_cls}">{risk}</div>'
            f'<div class="lbl" style="margin-top:4px;">/ 10</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="cs-hr"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cs-impact">{a["impact"]}</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="cs-card"><h3>Cognitive Metrics Map</h3>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(a["metrics"]), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="cs-card"><h3>Identified Risk Factors</h3>', unsafe_allow_html=True)
        st.plotly_chart(risk_bar(a["risk_factors"]), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    c3, c4 = st.columns([1, 2], gap="large")
    with c3:
        st.markdown('<div class="cs-card"><h3>Content Breakdown</h3>', unsafe_allow_html=True)
        st.plotly_chart(category_donut(a["content_breakdown"]), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="cs-card"><h3>Emotional Volatility Trend</h3>', unsafe_allow_html=True)
        st.plotly_chart(emotional_trend_bar(a["emotional_trend"]), use_container_width=True,
                        config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="cs-card"><h3>Engagement Depth (Posts per hour)</h3>', unsafe_allow_html=True)
    st.plotly_chart(engagement_area(a["engagement_pattern"]), use_container_width=True,
                    config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="cs-card"><h3>Recommended Protocol</h3>'
                '<ul style="list-style:none; padding:0; margin:0; color:var(--text); line-height:1.8;">'
                + "".join(f'<li>▸ {m}</li>' for m in a["preventive_measures"]) +
                '</ul></div>', unsafe_allow_html=True)


# ---------- User Dashboard ----------
def page_dashboard():
    if st.session_state.user is None or st.session_state.user["role"] != "user":
        goto("login"); return
    nav_user("PATIENT VIEW")

    if st.session_state.current_analysis:
        render_result(st.session_state.current_analysis)
        return

    st.markdown(
        '<div style="max-width:780px; margin: 18px auto;">'
        '<h1 style="font-size:30px; font-weight:800; letter-spacing:-0.02em; margin:0 0 4px;">'
        'New Cognitive Analysis</h1>'
        '<p style="color:var(--muted); margin:0 0 22px;">Paste your recent social media history '
        'or browsing log for AI assessment.</p>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="cs-card">', unsafe_allow_html=True)
        with st.form("analyze_form"):
            platform = st.selectbox("Primary Platform",
                                    ["Mixed Platforms", "YouTube", "Twitter / X", "Instagram",
                                     "TikTok", "Facebook", "Reddit"])
            sample = st.checkbox("Use sample data")
            default_text = ""
            if sample:
                default_text = "\n".join([
                    "08:12 Breaking news: shocking scandal exposed in politics",
                    "09:30 lol that meme was hilarious haha",
                    "10:05 New python tutorial on async/await — great content",
                    "11:45 Everyone has the perfect body except me, ugh",
                    "12:20 War update: more tragedy overseas, feeling anxious",
                    "13:00 Amazing recipe for ramen, love this chef",
                    "14:30 Workout reminder: 5k run, feeling great",
                    "20:10 Doomscrolling again, can't sleep",
                    "22:45 Limited drop, exclusive sneakers, fomo kicking in",
                    "23:30 Gaming stream was so fun, joy",
                ])
            content = st.text_area(
                "Browsing Data / Log", value=default_text, height=240,
                placeholder="Paste text logs, raw JSON, or descriptive browsing history here...",
            )
            cols = st.columns([3, 1])
            with cols[1]:
                submitted = st.form_submit_button("Run Diagnostic")
            if submitted:
                if not content.strip() or len(content.strip()) < 10:
                    st.error("Please provide enough context for analysis (min 10 chars).")
                else:
                    res = analyze(platform, content)
                    res["user_id"] = st.session_state.user["_id"]
                    ins = analyses.insert_one(res)
                    res["_id"] = ins.inserted_id
                    st.session_state.current_analysis = res
                    st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)


# ---------- History ----------
def page_history():
    if st.session_state.user is None or st.session_state.user["role"] != "user":
        goto("login"); return
    nav_user("PATIENT VIEW")

    st.markdown(
        '<h1 style="font-size:30px; font-weight:800; letter-spacing:-0.02em; margin:18px 0 18px;">'
        'Past Diagnostics</h1>', unsafe_allow_html=True
    )

    rows = list(analyses.find({"user_id": st.session_state.user["_id"]}).sort("created_at", -1))
    if not rows:
        st.markdown('<div class="cs-card" style="color:var(--muted);">'
                    'No past analyses yet. Run your first diagnostic from the Dashboard.</div>',
                    unsafe_allow_html=True)
        return

    for a in rows:
        risk = a["overall_risk_score"]
        risk_color = "var(--destructive)" if risk >= 6 else "var(--accent)" if risk >= 3 else "var(--primary)"
        st.markdown(
            f'<div class="cs-card" style="margin-bottom:14px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
            f'<span class="cs-pill">{a["platform"]}</span>'
            f'<span class="cs-meta">{a["created_at"].strftime("%b %d, %Y · %H:%M")}</span>'
            f'</div>'
            f'<div style="font-size:14px; line-height:1.5; margin-bottom:10px;">{a["summary"]}</div>'
            f'<div class="cs-meta">Risk Score: '
            f'<span style="color:{risk_color}; font-weight:700;">{risk}/10</span></div>'
            f'</div>', unsafe_allow_html=True
        )
        cols = st.columns([5, 1])
        with cols[1]:
            if st.button("Open", key=f"open_{a['_id']}", type="secondary"):
                st.session_state.current_analysis = a
                goto("dashboard")


# ---------- Admin ----------
def page_admin_dashboard():
    if st.session_state.user is None or st.session_state.user["role"] != "admin":
        goto("admin_login"); return
    nav_user("CLINICAL ADMIN")

    total_users = users.count_documents({"role": "user"})
    total_analyses = analyses.count_documents({})
    all_analyses = list(analyses.find({}))
    avg_risk = round(sum(a["overall_risk_score"] for a in all_analyses) / len(all_analyses), 2) \
        if all_analyses else 0.0
    high_risk = sum(1 for a in all_analyses if a["overall_risk_score"] >= 6)

    st.markdown('<h1 style="font-size:30px; font-weight:800; letter-spacing:-0.02em; '
                'margin: 12px 0 18px;">Clinical Operations Dashboard</h1>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Patients", total_users)
    c2.metric("Diagnostics", total_analyses)
    c3.metric("Avg Risk", avg_risk)
    c4.metric("High-Risk Records", high_risk)

    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Patients", "All Diagnostics", "Platform Stats"])
    with tab1:
        u_rows = list(users.find({"role": "user"}))
        if u_rows:
            df = pd.DataFrame([{
                "Email": u["email"], "Name": u.get("name", ""),
                "Joined": u["created_at"].strftime("%Y-%m-%d"),
                "Diagnostics": analyses.count_documents({"user_id": u["_id"]}),
            } for u in u_rows])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No patients registered yet.")
    with tab2:
        if all_analyses:
            df = pd.DataFrame([{
                "When": a["created_at"].strftime("%Y-%m-%d %H:%M"),
                "Platform": a["platform"],
                "Risk": a["overall_risk_score"],
                "Summary": a["summary"][:120] + "...",
            } for a in sorted(all_analyses, key=lambda x: x["created_at"], reverse=True)])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No diagnostics yet.")
    with tab3:
        if all_analyses:
            df = pd.DataFrame(all_analyses)
            counts = df.groupby("platform").size().reset_index(name="count")
            st.bar_chart(counts, x="platform", y="count", use_container_width=True)
        else:
            st.info("No data yet.")


PAGES = {
    "landing": page_landing,
    "login": page_login,
    "admin_login": page_admin_login,
    "dashboard": page_dashboard,
    "history": page_history,
    "admin_dashboard": page_admin_dashboard,
}

PAGES.get(st.session_state.page, page_landing)()
