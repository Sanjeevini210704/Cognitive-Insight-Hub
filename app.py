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

st.set_page_config(page_title="CogniScan — Cognitive Insight Hub",
                   page_icon="🧠", layout="wide")

ensure_seed_users()

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None


def goto(page: str):
    st.session_state.page = page
    st.rerun()


def logout():
    st.session_state.user = None
    st.session_state.current_analysis = None
    goto("landing")


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧠 CogniScan")
    st.caption("Cognitive Insight Hub")
    st.divider()
    if st.session_state.user is None:
        if st.button("Home", use_container_width=True):
            goto("landing")
        if st.button("User Login", use_container_width=True):
            goto("login")
        if st.button("Admin Login", use_container_width=True):
            goto("admin_login")
    else:
        u = st.session_state.user
        st.markdown(f"**{u['name']}**  \n`{u['email']}`  \nRole: `{u['role']}`")
        st.divider()
        if u["role"] == "admin":
            if st.button("Admin Dashboard", use_container_width=True):
                goto("admin_dashboard")
        else:
            if st.button("Dashboard", use_container_width=True):
                goto("dashboard")
            if st.button("New Analysis", use_container_width=True):
                st.session_state.current_analysis = None
                goto("dashboard")
            if st.button("History", use_container_width=True):
                goto("history")
        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()

    st.divider()
    st.caption("Demo accounts")
    st.code("user:  demo@cogniscan.ai / demo1234\nadmin: admin@cogniscan.ai / admin1234",
            language="text")


# ---------- Pages ----------
def page_landing():
    st.title("CogniScan")
    st.subheader("Understand how your social media diet shapes your mind.")
    st.write(
        "CogniScan analyzes your social-media consumption patterns and surfaces the "
        "cognitive and emotional signals hiding in them — attention drift, anxiety load, "
        "dopamine seeking, social comparison, and information overload."
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 🔎 Analyze")
        st.write("Paste your feed history. We tag categories, sentiment, and risk patterns.")
    with c2:
        st.markdown("### 📊 Visualize")
        st.write("Five interactive charts give you a complete cognitive profile at a glance.")
    with c3:
        st.markdown("### 🛡️ Improve")
        st.write("Get a personalized impact summary and preventive measures you can act on.")
    st.divider()
    a, b = st.columns(2)
    with a:
        if st.button("Get Started — User Login", use_container_width=True, type="primary"):
            goto("login")
    with b:
        if st.button("Admin Login", use_container_width=True):
            goto("admin_login")


def _login_form(role: str, title: str):
    st.title(title)
    tabs = st.tabs(["Login", "Register"]) if role == "user" else st.tabs(["Login"])
    with tabs[0]:
        with st.form(f"login_{role}"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", type="primary")
            if submitted:
                user = login(email, password, role)
                if user:
                    st.session_state.user = user
                    goto("admin_dashboard" if role == "admin" else "dashboard")
                else:
                    st.error("Invalid credentials.")
    if role == "user":
        with tabs[1]:
            with st.form("register_user"):
                name = st.text_input("Name")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_pw")
                submitted = st.form_submit_button("Create Account", type="primary")
                if submitted:
                    if not (name and email and password):
                        st.error("All fields are required.")
                    else:
                        u = register(email, name, password, "user")
                        if u is None:
                            st.error("That email is already registered.")
                        else:
                            st.session_state.user = u
                            goto("dashboard")


def page_login():
    _login_form("user", "User Login")


def page_admin_login():
    _login_form("admin", "Admin Login")


def render_analysis(a: dict):
    top = st.columns([3, 1, 1, 1])
    with top[0]:
        st.subheader(f"Analysis — {a['platform']}")
        st.caption(a.get("created_at", datetime.utcnow()).strftime("%Y-%m-%d %H:%M UTC"))
    with top[1]:
        st.metric("Risk Score", f"{a['overall_risk_score']}/10")
    with top[2]:
        if st.button("New Analysis", key=f"new_{a.get('_id','x')}"):
            st.session_state.current_analysis = None
            st.rerun()
    with top[3]:
        if st.button("Print", key=f"print_{a.get('_id','x')}"):
            st.components.v1.html("<script>window.parent.print()</script>", height=0)

    st.markdown("#### Summary")
    st.write(a["summary"])

    st.markdown("#### Cognitive & Emotional Impact")
    st.info(a["impact"])

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(radar_chart(a["metrics"]), use_container_width=True)
    with c2:
        st.plotly_chart(category_donut(a["content_breakdown"]), use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(emotional_trend_bar(a["emotional_trend"]), use_container_width=True)
    with c4:
        st.plotly_chart(engagement_area(a["engagement_pattern"]), use_container_width=True)
    st.plotly_chart(risk_bar(a["risk_factors"]), use_container_width=True)

    st.markdown("#### Preventive Measures")
    for m in a["preventive_measures"]:
        st.markdown(f"- {m}")


def page_dashboard():
    if st.session_state.user is None or st.session_state.user["role"] != "user":
        goto("login")
        return
    st.title("Your Dashboard")
    st.write("Paste a chunk of your social-media history (one post per line) and run the analysis.")

    if st.session_state.current_analysis:
        render_analysis(st.session_state.current_analysis)
        return

    with st.form("analyze_form"):
        platform = st.selectbox("Platform",
                                ["Twitter/X", "Instagram", "TikTok", "YouTube", "Reddit", "Facebook", "Other"])
        sample = st.checkbox("Use sample data", value=False)
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
        content = st.text_area("Content", value=default_text, height=240,
                               placeholder="Paste posts, captions, or watch history (one per line)...")
        submitted = st.form_submit_button("Run Analysis", type="primary")
        if submitted:
            if not content.strip():
                st.error("Please paste some content first.")
            else:
                result = analyze(platform, content)
                result["user_id"] = st.session_state.user["_id"]
                ins = analyses.insert_one(result)
                result["_id"] = ins.inserted_id
                st.session_state.current_analysis = result
                st.rerun()


def page_history():
    if st.session_state.user is None or st.session_state.user["role"] != "user":
        goto("login")
        return
    st.title("Analysis History")
    rows = list(analyses.find({"user_id": st.session_state.user["_id"]}).sort("created_at", -1))
    if not rows:
        st.info("No analyses yet. Run your first one from the Dashboard.")
        return
    for a in rows:
        with st.expander(f"{a['platform']} — risk {a['overall_risk_score']}/10  "
                         f"({a['created_at'].strftime('%Y-%m-%d %H:%M')})"):
            if st.button("Open", key=f"open_{a['_id']}"):
                st.session_state.current_analysis = a
                goto("dashboard")
            st.write(a["summary"])


def page_admin_dashboard():
    if st.session_state.user is None or st.session_state.user["role"] != "admin":
        goto("admin_login")
        return
    st.title("Admin Dashboard")

    total_users = users.count_documents({"role": "user"})
    total_analyses = analyses.count_documents({})
    all_analyses = list(analyses.find({}))
    avg_risk = round(sum(a["overall_risk_score"] for a in all_analyses) / len(all_analyses), 2) \
        if all_analyses else 0.0
    high_risk = sum(1 for a in all_analyses if a["overall_risk_score"] >= 6)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users", total_users)
    c2.metric("Analyses", total_analyses)
    c3.metric("Avg Risk", avg_risk)
    c4.metric("High-Risk Analyses", high_risk)

    st.divider()
    tab1, tab2, tab3 = st.tabs(["Users", "All Analyses", "Platform Stats"])

    with tab1:
        u_rows = list(users.find({"role": "user"}))
        if u_rows:
            df = pd.DataFrame([{
                "Email": u["email"], "Name": u.get("name", ""),
                "Joined": u["created_at"].strftime("%Y-%m-%d"),
                "Analyses": analyses.count_documents({"user_id": u["_id"]}),
            } for u in u_rows])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No users yet.")

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
            st.info("No analyses yet.")

    with tab3:
        if all_analyses:
            df = pd.DataFrame(all_analyses)
            counts = df.groupby("platform").size().reset_index(name="count")
            st.bar_chart(counts, x="platform", y="count", use_container_width=True)
        else:
            st.info("No data yet.")


# ---------- Router ----------
PAGES = {
    "landing": page_landing,
    "login": page_login,
    "admin_login": page_admin_login,
    "dashboard": page_dashboard,
    "history": page_history,
    "admin_dashboard": page_admin_dashboard,
}

PAGES.get(st.session_state.page, page_landing)()
